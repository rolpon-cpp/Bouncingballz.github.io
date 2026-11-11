# Written by Claude Sonnet 5.5
"""Step 6: assemble the final video with ffmpeg.

1. checks every rendered scene against its plan (frame count) and its audio (length)
2. joins the scene videos without re-encoding
3. joins the scene audio (exact lengths) and normalises loudness to about -16 LUFS in two passes
4. burns in the captions (tools/make_captions.py) and encodes output/final.mp4 (H.264 + AAC)
5. writes output/final_report.txt with the measured durations and saves the last frame as a PNG

No music is added unless you give a royalty-free file:  python tools/assemble.py --music path/to/track.mp3
Usage: python tools/assemble.py [--music FILE]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from modkit import config as C
from modkit.audio_io import read_wav, write_wav
from modkit.plans import get_plan

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_captions  # noqa: E402


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def probe(path, entries, stream="v:0"):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", entries, "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return out


def clip_info(n: int):
    clip = C.CLIPS_DIR / f"scene{n}_final.mp4"
    if not clip.exists():
        sys.exit(f"missing {clip}; run tools/render_scenes.py --quality final first")
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames,width,height,r_frame_rate", "-of", "json", str(clip)], capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    return clip, int(s["nb_read_frames"]), int(s["width"]), int(s["height"]), s["r_frame_rate"]


def join_audio() -> Path:
    parts = []
    for n in sorted(C.SCENES):
        x, sr = read_wav(C.SCENE_AUDIO_DIR / f"scene{n}.wav")
        want = C.frames(get_plan(n).total) * C.SAMPLES_PER_FRAME
        if sr != C.SAMPLE_RATE:
            sys.exit(f"scene{n}.wav has sample rate {sr}")
        parts.append(x)
        if len(x) != want:
            sys.exit(f"scene{n}.wav has {len(x)} samples, expected {want}; run tools/mix_scene_audio.py")
    # the scene files are stereo copies of one channel; read_wav averaged them back to mono, so duplicate again
    mono = np.concatenate(parts)
    out = C.AUDIO_DIR / "full_mix.wav"
    write_wav(out, np.stack([mono, mono], axis=1), C.SAMPLE_RATE)
    return out


def add_music(mix_wav: Path, music: Path, total_seconds: float, gain_db: float = -20.0) -> Path:
    """Loop a (royalty-free) music file under the mix, quiet, with a fade in and a fade out."""
    bed = C.AUDIO_DIR / "music_bed.wav"
    af = f"afade=t=in:d=2,afade=t=out:st={total_seconds - 3:.2f}:d=3,volume={gain_db}dB"
    run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", str(music), "-t", f"{total_seconds:.3f}", "-ar", str(C.SAMPLE_RATE),
         "-ac", "2", "-af", af, str(bed)])
    out = C.AUDIO_DIR / "full_mix_music.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(mix_wav), "-i", str(bed), "-filter_complex",
         "[0:a][1:a]amix=inputs=2:duration=first:normalize=0", "-c:a", "pcm_s16le", str(out)])
    return out


def loudnorm(src: Path, dst: Path, target=-16.0, tp=-1.5, lra=11.0):
    """Two-pass loudness normalisation (linear gain, so the mix balance is kept) followed by a peak limiter at -3 dBFS (AAC overshoots by about 2 dB)."""
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
                         f"loudnorm=I={target}:TP={tp}:LRA={lra}:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True, check=True)
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p1.stderr, re.S).group(0))
    af = (f"loudnorm=I={target}:TP={tp}:LRA={lra}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          f"alimiter=limit=0.708:attack=3:release=60:level=disabled")   # the linear gain pushes a few peaks too high; -3 dBFS leaves room for AAC overshoot
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", str(C.SAMPLE_RATE), "-c:a", "pcm_s16le", str(dst)])
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--music", help="optional royalty-free music file to mix in quietly under the narration")
    args = ap.parse_args()
    report = []
    total_frames = 0
    clips = []
    for n in sorted(C.SCENES):
        clip, frames, w, h, rate = clip_info(n)
        want = C.frames(get_plan(n).total)
        ok = frames == want and (w, h) == C.RES_FINAL and rate == f"{C.FPS}/1"
        report.append(f"scene {n}: {frames} frames ({frames / C.FPS:.2f} s), plan {want}, {w}x{h} {rate}: {'OK' if ok else 'MISMATCH'}")
        if not ok:
            sys.exit("\n".join(report))
        total_frames += frames
        clips.append(clip)
    print("\n".join(report))

    out_dir = C.OUTPUT_DIR
    lst = out_dir / "concat_list.txt"
    lst.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))
    nocaps = out_dir / "video_nocaps.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(nocaps)])

    mix = join_audio()
    if args.music:
        mix = add_music(mix, Path(args.music), total_frames / C.FPS)
        report.append(f"music added from {args.music}")
    norm = C.AUDIO_DIR / "full_mix_norm.wav"
    m = loudnorm(mix, norm)
    report.append(f"audio: input {m['input_i']} LUFS, true peak {m['input_tp']} dBTP -> normalised to -16 LUFS")

    make_captions.main()
    final = out_dir / "final.mp4"
    vf = f"ass={(out_dir / 'captions.ass').as_posix()}"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(nocaps), "-i", str(norm), "-vf", vf,
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-r", str(C.FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)])

    fmt = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,r_frame_rate,duration",
                                     "-of", "json", str(final)], capture_output=True, text=True, check=True).stdout)
    durs = {s["codec_name"]: float(s["duration"]) for s in fmt["streams"]}
    report.append(f"final.mp4: {float(fmt['format']['duration']):.2f} s, {int(fmt['format']['size']) / 1e6:.1f} MB, streams {durs}")
    report.append(f"expected duration {total_frames / C.FPS:.2f} s ({int(total_frames / C.FPS // 60)}:{total_frames / C.FPS % 60:04.1f})")
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", str(final), "-frames:v", "1", str(out_dir / "final_last_frame.png")])
    (out_dir / "final_report.txt").write_text("\n".join(report) + "\n")
    print("\n".join(report[-4:]))


if __name__ == "__main__":
    main()

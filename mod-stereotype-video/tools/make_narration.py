# Written by Claude Sonnet 5.5
"""Step 3: one audio file per NARRATOR line, using Piper (free, local text-to-speech).

Every narrator line is split into sentences and each sentence is synthesized on its own, so
sentence boundaries are known exactly (used for captions and visual cues). Output:
    audio/narration/nXX.wav        48 kHz mono 16-bit, one file per NARRATOR line (n01..n16)
    audio/narration/narration.json durations and sentence timings

To use your own voice instead: record each line as audio/narration_custom/nXX.wav and run
    python tools/make_narration.py --source custom
Sentence timings are then estimated from character counts (captions may be a little less exact).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from modkit import config as C
from modkit.audio_io import active_rms, highpass, peak, read_wav, resample, trim_silence, write_wav
from modkit.script_data import narration_lines, sentences


def ensure_voice() -> Path:
    model = C.VOICE_DIR / f"{C.VOICE_NAME}.onnx"
    if not model.exists():
        C.VOICE_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [sys.executable, "-m", "piper.download_voices", C.VOICE_NAME, "--data-dir", str(C.VOICE_DIR)],
            check=True,
        )
    return model


def respell(text: str) -> str:
    for old, new in C.TTS_RESPELL:
        text = text.replace(old, new)
    return text


def synth_clip_piper(voice, syn_cfg, text: str):
    """Return (audio at 48 kHz, [(sentence, start_sample, end_sample)])."""
    pause = np.zeros(int(C.SENTENCE_PAUSE_SEC * C.SAMPLE_RATE), dtype=np.float32)
    parts, spans, cursor = [], [], 0
    sents = sentences(text)
    for i, sent in enumerate(sents):
        chunks = list(voice.synthesize(respell(sent), syn_cfg))
        audio = np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32)
        audio = resample(audio, chunks[0].sample_rate, C.SAMPLE_RATE)
        audio = trim_silence(audio, C.SAMPLE_RATE)
        parts.append(audio)
        spans.append((sent, cursor, cursor + len(audio)))
        cursor += len(audio)
        if i < len(sents) - 1:
            parts.append(pause)
            cursor += len(pause)
    return np.concatenate(parts), spans


def synth_clip_custom(clip_id: str, text: str):
    """Load a user recording and estimate sentence timings from character counts."""
    path = C.NARRATION_CUSTOM_DIR / f"{clip_id}.wav"
    if not path.exists():
        raise FileNotFoundError(f"missing recording {path}")
    x, sr = read_wav(path)
    x = trim_silence(resample(x, sr, C.SAMPLE_RATE), C.SAMPLE_RATE)
    sents = sentences(text)
    total_chars = sum(len(s) for s in sents)
    spans, cursor = [], 0
    for s in sents:
        n = int(len(x) * len(s) / total_chars)
        spans.append((s, cursor, min(len(x), cursor + n)))
        cursor += n
    return x, spans


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=["piper", "custom"], default="piper")
    ap.add_argument("--length-scale", type=float, default=C.VOICE_LENGTH_SCALE, help="Piper pace, > 1 is slower")
    args = ap.parse_args()

    lines = narration_lines()
    voice = syn_cfg = None
    if args.source == "piper":
        from piper import PiperVoice, SynthesisConfig
        voice = PiperVoice.load(str(ensure_voice()))
        syn_cfg = SynthesisConfig(
            length_scale=args.length_scale,
            noise_scale=C.VOICE_NOISE_SCALE,
            noise_w_scale=C.VOICE_NOISE_W_SCALE,
            normalize_audio=False,  # keep natural level differences; one global gain is applied below
        )

    clips = {}
    for line in lines:
        if args.source == "piper":
            audio, spans = synth_clip_piper(voice, syn_cfg, line["text"])
        else:
            audio, spans = synth_clip_custom(line["id"], line["text"])
        clips[line["id"]] = (line, highpass(audio, 70.0), spans)
        print(f"  synthesized {line['id']} ({len(audio) / C.SAMPLE_RATE:5.2f} s)", flush=True)

    # One global gain for all clips keeps sentence-to-sentence loudness natural and consistent.
    all_audio = np.concatenate([a for _, a, _ in clips.values()])
    target_rms = 10 ** (-20.0 / 20.0)          # about -20 dBFS while speaking
    gain = target_rms / max(1e-6, active_rms(all_audio))
    gain = min(gain, 0.89 / max(1e-6, peak(all_audio)))   # never clip
    print(f"global gain {gain:.2f}x, peak after gain {peak(all_audio) * gain:.2f}")

    C.NARRATION_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    tot_words = tot_speech = tot_dur = 0.0
    for clip_id, (line, audio, spans) in clips.items():
        audio = np.clip(audio * gain, -0.95, 0.95)
        write_wav(C.NARRATION_DIR / f"{clip_id}.wav", audio, C.SAMPLE_RATE)
        dur = len(audio) / C.SAMPLE_RATE
        sent_info = [
            {"text": s, "start": round(a / C.SAMPLE_RATE, 4), "end": round(b / C.SAMPLE_RATE, 4)}
            for s, a, b in spans
        ]
        speech = sum(x["end"] - x["start"] for x in sent_info)
        words = len(line["text"].split())
        tot_words += words
        tot_speech += speech
        tot_dur += dur
        out[clip_id] = {
            "scene": line["scene"], "file": f"{clip_id}.wav", "text": line["text"],
            "duration": round(dur, 4), "sentences": sent_info,
        }
        print(f"{clip_id} scene {line['scene']}: {dur:6.2f} s, {words:3d} words, "
              f"{words / speech * 60:4.0f} wpm while speaking")
    meta = {"voice": C.VOICE_NAME if args.source == "piper" else "custom recordings",
            "length_scale": args.length_scale, "sample_rate": C.SAMPLE_RATE, "clips": out}
    C.NARRATION_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"total narration {tot_dur:.1f} s for {int(tot_words)} words "
          f"({tot_words / tot_speech * 60:.0f} wpm speaking, {tot_words / tot_dur * 60:.0f} wpm overall)")


if __name__ == "__main__":
    main()

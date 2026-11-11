# Why Discord Mods Got The Stereotype

A 6 minute 51 second animated YouTube video, built entirely from code out of `script.md`.
Script written by Claude Sonnet 5.5. Video and code made with Claude Sonnet 5.5. All servers and characters are fictional.

## Rebuild everything

From this folder:

```bash
bash run_all.sh            # full build: 1080p, final.mp4, thumbnail, title/description/tags, checks
bash run_all.sh quick      # 480p test render of every scene plus the 10 second Scene 1 clip (about 1 minute)
MUSIC=track.mp3 bash run_all.sh final   # optional: mix in a royalty-free music file (none is used by default)
```

First time only (the script does this for you if `.venv` is missing):

```bash
sudo apt-get install -y ffmpeg libpango1.0-dev libcairo2-dev pkg-config espeak-ng   # ffmpeg needs libass for captions
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Tested with Python 3.13, Manim Community 0.22.1, Piper 1.8.0, Pillow 13, ffmpeg 6.1 on Ubuntu 24.04.

## Step by step

| Step | Command | Output |
|---|---|---|
| 3. Narration (one file per NARRATOR line) | `.venv/bin/python tools/make_narration.py` | `audio/narration/n01.wav` to `n16.wav`, `narration.json` |
| Sound effects (original, synthesized) | `.venv/bin/python tools/make_sfx.py` | `audio/sfx/*.wav` |
| One audio file per scene | `.venv/bin/python tools/mix_scene_audio.py` | `audio/scenes/scene1.wav` to `scene6.wav` |
| 5. Test render (480p) | `.venv/bin/python tools/render_scenes.py --quality test --jobs 4` | `output/scenes/sceneN_test.mp4` |
| 10 second Scene 1 test clip | `.venv/bin/python tools/make_test_clip.py` | `output/test/scene1_test_10s.mp4` |
| 5. Final render (1080p, 30 fps) | `.venv/bin/python tools/render_scenes.py --quality final --jobs 4` | `output/scenes/sceneN_final.mp4` |
| 6. Assemble with captions | `.venv/bin/python tools/assemble.py` | `output/final.mp4`, `captions.srt`, `captions.ass` |
| 7. Thumbnail | `.venv/bin/python tools/make_thumbnail.py` | `output/thumbnail.png` (1280x720) |
| 8. Title, description, tags, pinned comment | `.venv/bin/python tools/make_metadata.py` | `output/title.txt`, `description.txt`, `tags.txt`, `pinned_comment.txt` |
| Rules check | `.venv/bin/python tools/lint_text.py` | pass or fail list |

Quick visual checks: `tools/contact_sheet.py VIDEO OUT.png --every 5` makes a labelled grid of frames.

## Folder layout

```
script.md            the script, exactly as written (the single source of truth)
scenes/              one Manim scene per script scene (scene1_cold_open.py ... scene6_closing.py)
audio/               narration/ (16 files), sfx/, scenes/ (mixed audio per scene), voices/ (downloaded voice model)
output/              scenes/ (rendered clips), final.mp4, thumbnail.png, title/description/tags, captions
modkit/              shared library: theme, icons, characters, chat UI, timing (plan.py, plans/), audio, effects
tools/               the pipeline scripts listed above
run_all.sh           runs everything in order
```

## How the timing works

Narration comes first. `make_narration.py` synthesizes every sentence separately, so the exact start and end of each
sentence is known. Each scene has a cue sheet in `modkit/plans/sceneN.py`. The same cue sheet drives both the animation
(Manim waits until each cue) and the audio mixer (it places the narration and sound effects at the cues). Every duration
is converted to a whole number of frames, so each scene video has exactly as many frames as its audio has samples
(1 frame = 1600 samples at 48 kHz). `render_scenes.py` and `assemble.py` check this and stop if anything is off by a frame.

## Making changes

* **Edit narration or on-screen text**: change `script.md`, then run `bash run_all.sh`. Narration, typed chat lines,
  checklists, loop labels and timeline events are all read from it.
* **Use your own voice**: record each NARRATOR line as `audio/narration_custom/n01.wav` to `n16.wav`, then run
  `.venv/bin/python tools/make_narration.py --source custom` followed by the rest of the steps. Caption timing inside
  a line is then estimated from character counts.
* **Change the voice or pace**: edit `VOICE_NAME` and `VOICE_LENGTH_SCALE` in `modkit/config.py`.
  The current voice, `en_US-ljspeech-high`, is public domain. Check a voice's licence before using another one
  (some Piper voices are non-commercial).
* **Change pacing**: the pauses and holds are in `modkit/plans/sceneN.py`.
* **Add music**: only with a royalty-free file you have the rights to: `python tools/assemble.py --music file.mp3`.

## Rules this project follows (checked by `tools/lint_text.py`)

* Every code file starts with "Written by Claude Sonnet 5.5".
* The last video frame shows "Script and video made with Claude Sonnet 5.5".
* `description.txt` contains "Script written by Claude Sonnet 5.5. All servers and characters shown are fictional."
* Every title option, the description and the pinned comment carry an AI disclosure (YouTube length limits are asserted).
* No em dashes (or en dashes) anywhere in code, script, captions or metadata, so none appear on screen.
* All names are invented. No real logos, servers or users. All art is drawn in code.

## Troubleshooting

* Render each scene with Manim's cache off (`render_scenes.py` already passes `--disable_caching`); stale cache entries
  can show old frames after code changes.
* Parallel renders each use their own media folder (`output/media/<quality>/sceneN`) so they cannot delete each other's
  temporary text files.
* If the burned-in captions use the wrong font, check that `fc-list | grep Inter` finds the Inter font family.

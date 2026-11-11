# Written by Claude Sonnet 5.5
# Rebuild the whole video from script.md.  Run from this folder:   bash run_all.sh
#   bash run_all.sh quick     480p test render, no final assembly (about 1 minute)
#   bash run_all.sh final     1080p render, final.mp4, thumbnail, metadata, checks (about 10 minutes)  [default]
# Add royalty-free music (optional):  MUSIC=path/to/track.mp3 bash run_all.sh final
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi
PY=.venv/bin/python
MODE="${1:-final}"

$PY tools/make_narration.py              # Step 3: one narration file per NARRATOR line (Piper) + measured timings
$PY tools/make_sfx.py                    # original sound effects
$PY tools/mix_scene_audio.py             # one audio file per scene, exactly as long as its video

if [ "$MODE" = "quick" ]; then
  $PY tools/render_scenes.py --quality test --jobs 4        # Step 5: 854x480 test render of every scene
  $PY tools/make_test_clip.py --scene 1 --seconds 10        # the 10 second Scene 1 test clip
  exit 0
fi

$PY tools/render_scenes.py --quality final --jobs 4         # Step 5: 1920x1080, 30 fps
if [ -n "${MUSIC:-}" ]; then
  $PY tools/assemble.py --music "$MUSIC"                    # Step 6: video + narration + captions (+ music)
else
  $PY tools/assemble.py                                     # Step 6: video + narration + burned-in captions
fi
$PY tools/make_thumbnail.py                                 # Step 7
$PY tools/make_metadata.py                                  # Step 8
$PY tools/lint_text.py                                      # rules check
echo "Done. Files are in output/: final.mp4, thumbnail.png, title.txt, description.txt, tags.txt, captions.srt"

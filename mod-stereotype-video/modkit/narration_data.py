# Written by Claude Sonnet 5.5
"""Load the narration timings written by tools/make_narration.py (audio/narration/narration.json)."""
import json
from functools import lru_cache

from .config import NARRATION_JSON


@lru_cache(maxsize=1)
def load_narration() -> dict:
    """Return {clip_id: {scene, text, duration, sentences: [{text, start, end}], file}}."""
    if not NARRATION_JSON.exists():
        raise FileNotFoundError(
            f"{NARRATION_JSON} not found. Run tools/make_narration.py first (see README.md)."
        )
    return json.loads(NARRATION_JSON.read_text(encoding="utf-8"))["clips"]

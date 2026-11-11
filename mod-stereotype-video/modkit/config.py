# Written by Claude Sonnet 5.5
"""Shared constants for the whole pipeline: paths, video format, voice settings, credit lines."""
from pathlib import Path

# ---- identity / required text -------------------------------------------------------------
MODEL_NAME = "Claude Sonnet 5.5"
SIGNATURE = "Written by " + MODEL_NAME
CREDIT_LINE = "Script and video made with " + MODEL_NAME
DESCRIPTION_LINE = "Script written by " + MODEL_NAME + ". All servers and characters shown are fictional."
VIDEO_TITLE = "Why Discord Mods Got The Stereotype"

# ---- paths ---------------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_MD = ROOT / "script.md"
AUDIO_DIR = ROOT / "audio"
NARRATION_DIR = AUDIO_DIR / "narration"
NARRATION_CUSTOM_DIR = AUDIO_DIR / "narration_custom"
SFX_DIR = AUDIO_DIR / "sfx"
SCENE_AUDIO_DIR = AUDIO_DIR / "scenes"
VOICE_DIR = AUDIO_DIR / "voices"
NARRATION_JSON = NARRATION_DIR / "narration.json"
OUTPUT_DIR = ROOT / "output"
MEDIA_DIR = OUTPUT_DIR / "media"
CLIPS_DIR = OUTPUT_DIR / "scenes"
TEST_DIR = OUTPUT_DIR / "test"
SCENES_DIR = ROOT / "scenes"

# ---- video / audio format ----------------------------------------------------------------
FPS = 30
SAMPLE_RATE = 48000
SAMPLES_PER_FRAME = SAMPLE_RATE // FPS  # 1600, so audio and video lengths can match exactly
RES_FINAL = (1920, 1080)
RES_TEST = (854, 480)

# ---- narration (Piper, free local text-to-speech) -----------------------------------------
# Voice licence: public domain (see the voice's MODEL_CARD on Hugging Face, rhasspy/piper-voices).
VOICE_NAME = "en_US-ljspeech-high"
VOICE_LENGTH_SCALE = 1.28       # > 1 is slower; about 137 spoken words per minute
VOICE_NOISE_SCALE = 0.6
VOICE_NOISE_W_SCALE = 0.7
SENTENCE_PAUSE_SEC = 0.55       # silence inserted between sentences of one narrator line
# Words the speech engine mispronounces are respelled for the engine only (captions keep the original).
TTS_RESPELL = [
    ("3 a.m.", "three A M"),
    ("Priya", "Pree-ya"),
]

# ---- scene files ---------------------------------------------------------------------------
SCENES = {
    1: ("scene1_cold_open.py", "ColdOpen", "Cold open"),
    2: ("scene2_job_nobody_applied_for.py", "JobNobodyAppliedFor", "The job nobody applied for"),
    3: ("scene3_stereotype_origins.py", "StereotypeOrigins", "Where the stereotype comes from"),
    4: ("scene4_why_it_keeps_happening.py", "WhyItKeepsHappening", "Why it keeps happening"),
    5: ("scene5_mods_you_never_notice.py", "ModsYouNeverNotice", "The mods you never notice"),
    6: ("scene6_closing.py", "Closing", "Closing"),
}


def frames(seconds: float) -> int:
    """Seconds to a whole number of video frames."""
    return int(round(seconds * FPS))


def snap(seconds: float) -> float:
    """Round a time to the frame grid."""
    return frames(seconds) / FPS

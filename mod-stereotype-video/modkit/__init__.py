# Written by Claude Sonnet 5.5
"""modkit: shared library for the "Why Discord Mods Got The Stereotype" video pipeline.

Modules
-------
config          constants: paths, video format, voice settings, credit lines
script_data     parses script.md (single source of truth for narration and on-screen text)
narration_data  loads the measured narration durations written by tools/make_narration.py
plan            Plan class: per-scene cue sheet shared by the animation and the audio mixer
plans/          one cue sheet per scene (pure Python, no Manim import)
audio_io        small WAV helpers (numpy only)
sfx_lib         original sound effects synthesized with numpy
theme           colors, fonts, text helpers
icons, characters, props, chat_ui   original vector art drawn with Manim primitives
base_scene      TimedScene: frame-accurate scene base class
"""

# Written by Claude Sonnet 5.5
"""Per-scene cue sheets. get_plan(n) builds the Plan for scene n (pure Python, no Manim import)."""
from importlib import import_module


def get_plan(number: int):
    return import_module(f"modkit.plans.scene{number}").build()

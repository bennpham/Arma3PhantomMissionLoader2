"""Locate the SQF payload (functions/ + loadscreen.jpg).

The payload ships embedded inside the package, but users can override it
without touching the app: a ``functions`` folder (and optionally a
``loadscreen.jpg``) placed next to the executable / repo root wins over the
embedded copy. The ``ARMA3PML_PAYLOAD`` environment variable wins over both.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

FUNCTIONS_DIR = "functions"
LOADSCREEN = "loadscreen.jpg"


def _app_dir() -> Path:
    if getattr(sys, "frozen", False):  # PyInstaller bundle
        return Path(sys.executable).resolve().parent
    return Path(sys.argv[0]).resolve().parent


def _embedded_root() -> Path:
    return Path(__file__).resolve().parent / "payload"


def payload_root() -> Path:
    """Directory that contains ``functions/`` and ``loadscreen.jpg``."""
    env = os.environ.get("ARMA3PML_PAYLOAD")
    if env and (Path(env) / FUNCTIONS_DIR).is_dir():
        return Path(env)
    app = _app_dir()
    if (app / FUNCTIONS_DIR).is_dir():
        return app
    return _embedded_root()


def functions_root() -> Path:
    return payload_root() / FUNCTIONS_DIR


def loadscreen_path() -> Path:
    """The loadscreen image; falls back to the embedded one if an override
    payload folder does not carry its own."""
    candidate = payload_root() / LOADSCREEN
    if candidate.is_file():
        return candidate
    return _embedded_root() / LOADSCREEN

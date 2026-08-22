import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from .app import create_app
except ImportError:  # pragma: no cover - fallback for direct execution
    from app import create_app

__all__ = ['create_app']
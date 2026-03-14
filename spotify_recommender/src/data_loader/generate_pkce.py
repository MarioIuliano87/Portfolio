from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    # Allow direct execution: `uv run src/data_loader/generate_pkce.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from data_loader.pipeline import run
else:
    from .pipeline import run

if __name__ == "__main__":
    run()

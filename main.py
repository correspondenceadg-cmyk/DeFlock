import sys
import traceback
from pathlib import Path

_src = Path(__file__).resolve().parent / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))


def _fatal(exc_text):
    for path in ("/sdcard/deflock_fatal.log", str(_src.parent / "deflock_fatal.log")):
        try:
            with open(path, "w") as f:
                f.write(exc_text)
            break
        except Exception:
            continue
    sys.stderr.write(exc_text)


if __name__ == "__main__":
    try:
        from deflock.app import main
        main()
    except Exception:
        _fatal(traceback.format_exc())
        raise

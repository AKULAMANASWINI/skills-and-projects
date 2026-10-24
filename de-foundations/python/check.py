"""Check your Python exercises — works before you've installed anything.

    python python/check.py            # all exercises
    python python/check.py ex03       # one file

The tests in python/tests/ are ordinary pytest tests. Until you install pytest
(lesson 06) this script runs them with a tiny built-in stand-in. Afterwards you can
also run them the real way:  pytest python/tests
"""

import contextlib
import importlib.util
import inspect
import logging
import sys
import tempfile
import traceback
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE / ("solutions" if "--solutions" in sys.argv else "exercises")


def install_pytest_standin() -> None:
    """Provide pytest.raises when real pytest isn't installed."""
    try:
        import pytest  # noqa: F401
        return
    except ImportError:
        pass

    class ExcInfo:
        value = None

    @contextlib.contextmanager
    def raises(exc_type):
        info = ExcInfo()
        try:
            yield info
        except exc_type as e:
            info.value = e
            return
        raise AssertionError(f"expected {exc_type.__name__} to be raised, nothing was")

    sys.modules["pytest"] = types.SimpleNamespace(raises=raises)


class CapLog(logging.Handler):
    """Minimal stand-in for pytest's caplog fixture."""
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)

    @contextlib.contextmanager
    def at_level(self, level):
        root = logging.getLogger()
        old = root.level
        root.setLevel(level)
        root.addHandler(self)
        try:
            yield
        finally:
            root.removeHandler(self)
            root.setLevel(old)


def run_test(fn) -> tuple[str, str]:
    kwargs, cleanup = {}, []
    params = inspect.signature(fn).parameters
    if "tmp_path" in params:
        d = tempfile.TemporaryDirectory()
        cleanup.append(d)
        kwargs["tmp_path"] = Path(d.name)
    if "caplog" in params:
        kwargs["caplog"] = CapLog()
    try:
        fn(**kwargs)
        return "ok", ""
    except NotImplementedError:
        return ".", "not attempted"
    except AssertionError as e:
        tb = traceback.extract_tb(e.__traceback__)
        line = next((f for f in reversed(tb) if "tests" in f.filename), tb[-1])
        detail = str(e) or line.line
        return "x", f"{detail}  (tests/{Path(line.filename).name}:{line.lineno})"
    except Exception as e:  # your code crashed
        tb = traceback.extract_tb(e.__traceback__)
        mine = next((f for f in reversed(tb) if str(CODE_DIR) in f.filename), tb[-1])
        return "x", f"{type(e).__name__}: {e}  (at {Path(mine.filename).name}:{mine.lineno})"
    finally:
        for d in cleanup:
            d.cleanup()


def main(args: list[str]) -> None:
    install_pytest_standin()
    sys.path.insert(0, str(CODE_DIR))
    prefix = next((a for a in args if not a.startswith("--")), "ex")
    test_files = sorted((HERE / "tests").glob(f"test_{prefix}*.py"))
    if not test_files:
        sys.exit(f"No tests match '{prefix}'")
    passed = total = 0
    for tf in test_files:
        print(f"\n{tf.stem.replace('test_', '')}")
        try:
            module = _load(tf)
        except NotImplementedError:
            print("  .  not attempted")
            continue
        except Exception as e:
            print(f"  x  could not import: {type(e).__name__}: {e}")
            continue
        tests = [(n, f) for n, f in vars(module).items() if n.startswith("test_") and callable(f)]
        for name, fn in tests:
            total += 1
            status, msg = run_test(fn)
            passed += status == "ok"
            print(f"  {status}  {name.removeprefix('test_')}" + (f"  — {msg}" if msg and status != "." else ""))
    print(f"\n{passed} / {total} tests passing")


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    main(sys.argv[1:])

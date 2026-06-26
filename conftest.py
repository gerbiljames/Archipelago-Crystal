import os


def pytest_configure(config):
    # AP_TEST_WORLDS implies `-m world` (unless an explicit -m was given) so callers don't repeat it; the
    # actual world scoping lives in worlds/__init__ (loading + AutoWorldRegister.testable_worlds)
    if os.environ.get("AP_TEST_WORLDS") and not config.option.markexpr:
        config.option.markexpr = "world"


def pytest_ignore_collect(collection_path, config):
    # AP_TEST_WORLDS scopes which worlds' own tests are collected: skip worlds/<world>/... for any
    # world not named, so other worlds are never imported
    env = os.environ.get("AP_TEST_WORLDS")
    if not env:
        return None
    selected = {name.strip() for name in env.split(",") if name.strip()}
    parts = str(collection_path).replace("\\", "/").split("/")
    if "worlds" in parts:
        i = parts.index("worlds")
        if i + 1 < len(parts) and parts[i + 1] not in selected:
            return True
    return None


def pytest_collection_modifyitems(items):
    # mark world-iterating tests for `-m world`: classes with `world_iterating = True`, plus anything
    # under worlds/<world>/test
    for item in items:
        parts = item.nodeid.replace("\\", "/").split("/")
        if getattr(getattr(item, "cls", None), "world_iterating", False) or \
                (parts[:1] == ["worlds"] and "test" in parts):
            item.add_marker("world")

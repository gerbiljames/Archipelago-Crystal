import os


class _ScopedWorldTypes(dict):
    """world_types view that scopes iteration to the selected games but keeps key lookup whole, so
    `for ... in world_types` loops scope to AP_TEST_WORLDS without breaking world_types["APQuest"]."""
    selected: set = set()

    def __iter__(self):
        return (k for k in dict.keys(self) if k in self.selected)

    def keys(self):
        return [k for k in dict.keys(self) if k in self.selected]

    def values(self):
        return [dict.__getitem__(self, k) for k in self.keys()]

    def items(self):
        return [(k, dict.__getitem__(self, k)) for k in self.keys()]

    def __len__(self):
        return len(self.keys())


def pytest_configure(config):
    # scope world iteration to AP_TEST_WORLDS so the general suite only iterates the named worlds
    env = os.environ.get("AP_TEST_WORLDS")
    if not env:
        return
    # AP_TEST_WORLDS implies `-m world` (unless an explicit -m was given) so callers don't repeat it
    if not config.option.markexpr:
        config.option.markexpr = "world"
    folders = {name.strip() for name in env.split(",") if name.strip()}
    from worlds.AutoWorld import AutoWorldRegister
    backing = AutoWorldRegister.world_types
    if isinstance(backing, _ScopedWorldTypes):
        return

    def folder_of(world_cls):
        path = getattr(world_cls, "__file__", None)
        return os.path.basename(os.path.dirname(path)) if path else None

    scoped = _ScopedWorldTypes(backing)
    scoped.selected = {game for game, cls in backing.items() if folder_of(cls) in folders}
    AutoWorldRegister.world_types = scoped


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
    # tests under worlds/<world>/test are world-iterating by definition; mark them so `-m world` covers them too
    for item in items:
        parts = item.nodeid.replace("\\", "/").split("/")
        if parts[:1] == ["worlds"] and "test" in parts:
            item.add_marker("world")

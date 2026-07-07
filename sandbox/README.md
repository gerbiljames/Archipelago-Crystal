# Untrusted apworld sandbox

Run the unit tests / fuzzer for a custom apworld you **have not read** without
risking the host. An apworld is arbitrary Python that Archipelago imports and
executes, so the only safe way to run its tests is inside OS-level isolation.
Python-level sandboxing (RestrictedPython, import hooks, AST scans) is bypassable
and is deliberately *not* used here.

## Use

```bash
# First run builds the image (a few minutes); later runs reuse it.
sandbox/test-world.sh ~/Downloads/somebody-elses-world.apworld
```

Pass a source directory instead of a `.apworld` to also run the world's own
`test/` directory:

```bash
sandbox/test-world.sh ./some_world_src/
```

Run an arbitrary command inside the jail (e.g. fuzzing — pass the world's
registered **game name**, not the filename):

```bash
sandbox/test-world.sh foo.apworld -- python fuzz.py -g "My Game" -r 100

# don't know the game name?
sandbox/test-world.sh foo.apworld -- \
  python -c 'from worlds import AutoWorldRegister as R; print(*R.world_types)'
```

Force an image rebuild after changing the Dockerfile: `TARGET_BUILD=1 sandbox/test-world.sh ...`

## What the jail guarantees

The world's code still runs to completion — the container makes that safe by
removing anything worth attacking:

- **`--network=none`** — no exfiltration, no second-stage download. The single
  most important control. A world that "needs" network is a red flag.
- **`--read-only` rootfs** + small `tmpfs` scratch mounts — no host writes, no
  persistence. The world is mounted **`:ro`**; your home and the AP checkout are
  never bind-mounted writable.
- **`--cap-drop=ALL` + `--security-opt=no-new-privileges`** — no privilege
  escalation.
- **`--pids-limit`, `--memory`, `--cpus`** — a fork bomb / memory hog can't take
  the machine down.
- **Non-root user** inside, **`--rm`** — the container is disposable and holds no
  secrets.

## Recommended host hardening: userns-remap

This machine's Docker daemon runs as root without user-namespace remapping, so
the in-container `runner` uid maps 1:1 to a host uid. `network=none` +
`cap-drop=ALL` + `no-new-privileges` already make an escape hard, but enabling
**userns-remap** maps container uids to an unprivileged host range, so even a
container breakout lands as a nobody on the host. Add to `/etc/docker/daemon.json`:

```json
{ "userns-remap": "default" }
```

then `sudo systemctl restart docker` and rebuild the image. For a still-stronger
boundary, install gVisor and add `--runtime=runsc` to the `docker run` in
`test-world.sh`.

## Limits

- Isolation is of the **host**, not the workload: the code does execute. Never
  put credentials or private data in the image.
- The image installs AP's full dependency set the way a real install does
  (`requirements.txt` + `WebHostLib/requirements.txt` + `ModuleUpdate.py`, which
  pulls every bundled world's `worlds/*/requirements.txt`). A custom world
  declaring its own `requirements.txt` won't have those deps unless you rebuild
  after mounting it as a source dir — install ad-hoc deps inside the throwaway
  container, never in your real environment.
- The default run scopes the suite to the world under test with
  **`AP_TEST_WORLDS=<folder>`** (a feature of this branch): only that world plus
  the `generic`/`apquest` fixtures are imported, `-m world` is applied, and other
  worlds' test dirs are skipped. That makes the run fast (~5s for apquest vs ~2m
  unscoped) and means a failure implicates the world under test. Override with
  `-- pytest ...` to run something else, or `-- python fuzz.py -g "<Game>" -r N`
  to fuzz.

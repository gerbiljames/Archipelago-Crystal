# Untrusted APWorld sandbox

Run the unit tests or other scripts for a custom APWorld that is not necessarily trusted without
risking your host.

## Use

```bash
sandbox/test-world.sh ~/Downloads/sus-world.apworld
```

Pass a source directory instead of a `.apworld` to also run the world's own
`test/` directory:

```bash
sandbox/test-world.sh ./sus_world_src/
```

Run an arbitrary command inside the jail:

```bash
sandbox/test-world.sh foo.apworld -- python fuzz.py -g "Sus Game" -r 100
```

Force an image rebuild after changing the Dockerfile: `TARGET_BUILD=1 sandbox/test-world.sh ...`

## What the jail guarantees

The world runs as normal, the container makes that safe by
removing anything worth attacking:

- **`--network=none`**: no exfiltration, no second-stage downloads.
- **`--read-only` rootfs** + small `tmpfs` scratch mounts: no host writes, no
  persistence. The world is mounted **`:ro`**.
- **`--cap-drop=ALL` + `--security-opt=no-new-privileges`**: no privilege
  escalation.
- **`--pids-limit`, `--memory`, `--cpus`**: a fork bomb / memory hog can't take
  the machine down.
- **Non-root user** inside, **`--rm`**: the container is disposable and holds no
  secrets.

## Never rebuild with an untrusted world in the checkout

The image is built from the working tree, and the build runs **as root with
network access**. `ModuleUpdate.py` then `pip install`s every
`worlds/*/requirements.txt` it finds. `custom_worlds/` is excluded from the build
context, but `worlds/` is not: a hostile world copied into `worlds/` before a
rebuild gets its dependencies installed with full privileges on the host's
Docker daemon, which undoes everything above.

Always keep untrusted worlds outside the checkout and let `test-world.sh` mount
them at run time. Before `TARGET_BUILD=1`, check `git status worlds/` shows
nothing you did not write.

## Recommended host hardening: userns-remap

By default, the Docker daemon runs as root without user-namespace remapping, so
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
  pulls every bundled world's `worlds/*/requirements.txt`). A custom world's own
  `requirements.txt` is **not** installed, and must never be auto-installed (see
  above). The jail has no network, so `pip` won't work inside it either. A world
  that needs extra packages can only be tested after you read its
  `requirements.txt` yourself, add the pinned packages to the `pip install` line
  in the `Dockerfile`, and rebuild with the world still outside the checkout.
- The script always sets **`AP_TEST_WORLDS=<folder>`**, AP's own test-suite
  scoping.
- The scoping is **pytest/unittest-only**: `worlds/__init__` ignores
  `AP_TEST_WORLDS` for any other entry point, so a `-- python fuzz.py ...` or
  `-- python -c ...` command loads every bundled world as well.

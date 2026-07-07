#!/usr/bin/env bash
# Run the unit tests / fuzzer for an UNTRUSTED custom apworld inside a locked-down
# Docker container: no network, read-only root fs, all capabilities dropped,
# non-root user, resource-capped, and torn down on exit.
#
# The world's code DOES run to completion inside the jail -- the container exists
# to make sure that when it does, there is nothing on the host to steal, nowhere
# to phone home, and no way out. So: never bake secrets into the image, and treat
# any attempted network egress (which is blocked) as a signal the world is hostile.
#
# Usage:
#   sandbox/test-world.sh <world.apworld | world_dir/> [-- <command...>]
#
#   sandbox/test-world.sh ~/Downloads/foo.apworld
#       -> AP's suite scoped to this world via AP_TEST_WORLDS (imports only it +
#          fixtures, `-m world`); a failure implicates the world, not the image
#
#   sandbox/test-world.sh ./some_world_src/
#       -> also runs the world's own test/ dir (mounted as worlds/<name>/)
#
#   # Fuzz it -- pass the world's registered *game name* (not the filename):
#   sandbox/test-world.sh foo.apworld -- python fuzz.py -g "My Game" -r 100
#
#   # List the game names a world registers, if you don't know it:
#   sandbox/test-world.sh foo.apworld -- python -c \
#     'from worlds import AutoWorldRegister as R; print(*R.world_types)'
#
set -euo pipefail

IMAGE="ap-untrusted-sandbox"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

die() { echo "error: $*" >&2; exit 1; }

[[ $# -ge 1 ]] || die "usage: $0 <world.apworld | world_dir/> [-- <command...>]"

TARGET="$1"; shift
CMD=()
if [[ "${1:-}" == "--" ]]; then shift; CMD=("$@"); fi

[[ -e "$TARGET" ]] || die "no such path: $TARGET"
TARGET="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"

# Decide how to mount the world. `name` is the world's *folder* name -- which is
# exactly what AP_TEST_WORLDS scopes on.
MOUNT_ARGS=()
if [[ -f "$TARGET" && "$TARGET" == *.apworld ]]; then
    name="$(basename "$TARGET" .apworld)"
    # Mount into worlds/ (always scanned), NOT custom_worlds/: with a read-only
    # rootfs AP treats /app as non-writable and never scans custom_worlds.
    # The filename stem must equal the apworld's internal folder id.
    MOUNT_ARGS=(-v "$TARGET:/app/worlds/$name.apworld:ro")
elif [[ -d "$TARGET" ]]; then
    name="$(basename "$TARGET")"
    # Mounting as a real world folder lets the world's own test/ dir run too
    # (pytest can't collect tests from inside an .apworld zip).
    MOUNT_ARGS=(-v "$TARGET:/app/worlds/$name:ro")
else
    die "target must be a .apworld file or a world source directory"
fi

# Default workload: AP's suite scoped to just this world via AP_TEST_WORLDS
# (set below). Scoping imports only this world (+ generic/apquest fixtures),
# auto-applies `-m world`, and skips other worlds' test dirs -- so the run
# exercises the world under test and a failure implicates it, not the image.
# For a source-dir mount this also runs the world's own worlds/<name>/test.
if [[ ${#CMD[@]} -eq 0 ]]; then
    # test/webhost/test_docs.py asserts pre-generated static doc files exist
    # (produced by the webhost build, which we don't run) -- it's not a
    # world-correctness check, so ignore it to avoid false failures.
    CMD=(bash -c "python -m pytest -q -p no:cacheprovider --no-header \
        --continue-on-collection-errors --ignore=test/webhost/test_docs.py")
fi

# Optional extra read-only mounts (space-separated host:container pairs), e.g. to
# inject a live fuzzer file. Read-only only -- keeps the jail's guarantees intact.
EXTRA_MOUNTS=()
if [[ -n "${TW_RO_MOUNTS:-}" ]]; then
    for spec in $TW_RO_MOUNTS; do
        EXTRA_MOUNTS+=(-v "${spec}:ro")
    done
fi

# Build the image if missing (or run with --build to force).
if [[ "${TARGET_BUILD:-}" == "1" ]] || ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo ">> building sandbox image ($IMAGE)..." >&2
    DOCKER_BUILDKIT=1 docker build -f "$REPO_ROOT/sandbox/Dockerfile" -t "$IMAGE" "$REPO_ROOT"
fi

echo ">> running '$name' sandboxed (no network, read-only, capped)..." >&2

# --- The jail ---
exec docker run --rm -i \
    --name "ap-sandbox-$name-$$" \
    --network=none \
    --read-only \
    --cap-drop=ALL \
    --security-opt=no-new-privileges \
    --pids-limit=512 \
    --memory=4g --memory-swap=4g \
    --cpus=4 \
    --tmpfs /tmp:rw,noexec,nosuid,size=1g \
    --tmpfs /app/output:rw,nosuid,size=512m \
    --tmpfs /app/logs:rw,nosuid,size=256m \
    --tmpfs /app/fuzz_output:rw,nosuid,size=512m \
    --tmpfs /app/WebHostLib/static/generated:rw,nosuid,size=256m,mode=1777 \
    -e "AP_TEST_WORLDS=$name" \
    -e HOME=/tmp/home \
    -e XDG_DATA_HOME=/tmp/home/.local/share \
    -e XDG_CONFIG_HOME=/tmp/home/.config \
    -e XDG_CACHE_HOME=/tmp/home/.cache \
    -e PYTHONDONTWRITEBYTECODE=1 \
    -e PYTHONPYCACHEPREFIX=/tmp/pycache \
    "${MOUNT_ARGS[@]}" \
    "${EXTRA_MOUNTS[@]}" \
    --entrypoint "" \
    "$IMAGE" \
    "${CMD[@]}"

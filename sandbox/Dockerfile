# Hardened image for running UNTRUSTED custom apworlds (unit tests + fuzzing).
#
# The trusted Archipelago core is baked in at build time. The untrusted world is
# NOT in this image -- it is mounted read-only at run time by test-world.sh, so
# the same image tests any world without a rebuild and the world code never
# becomes part of the trusted layer.

# The _speedups Cython module is intentionally NOT built: it only accelerates the
# hint server, AP falls back to pure Python without it, and world tests/fuzzing
# don't use it. Skipping it keeps the build fast and free of a C toolchain step.
FROM python:3.13-slim-bookworm AS sandbox
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

# git: needed to install the kivymd git dependency from requirements.txt.
# The rest are runtime/build libs several worlds' deps expect.
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends git gcc g++ libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Root + webhost requirements first for layer caching.
# - setuptools<81 still ships pkg_resources (removed in >=81), which several
#   worlds import and which ModuleUpdate itself needs; without it AP falls into
#   an interactive input() prompt that hangs (or EOFs) with no TTY.
# - WebHostLib deps (flask, ...) are needed because the world-scoped test suite
#   includes world_relevant webhost tests (test/webhost/*) that import WebHostLib.
# - pytest-subtests: the suite reports via unittest subTests (see docs/tests.md).
COPY requirements.txt .
COPY WebHostLib/requirements.txt WebHostLib/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r WebHostLib/requirements.txt \
    pytest pytest-subtests pytest-xdist "setuptools>=75,<81"

# Trusted core. .dockerignore keeps host junk (ROMs, custom_worlds, venvs) out.
COPY . .

# Install every bundled world's own deps the way a real AP install does:
# ModuleUpdate scans worlds/*/requirements.txt (git deps included) and installs
# what's missing. Keeps the world-load baseline clean so any load failure in a
# test run implicates the untrusted world, not a missing image dependency.
RUN python ModuleUpdate.py -y

# git is only needed for the pip install above; drop it from the final image.
RUN apt-get purge -y git && apt-get autoremove -y

# Run as a non-root, low-privilege user. With Docker userns-remap enabled on the
# host (recommended -- see sandbox/README.md) this maps to an unprivileged host
# uid, so even a container escape lands as nobody-on-host.
# custom_worlds/ is the mount point for an untrusted .apworld on a read-only rootfs,
# so it must already exist in the image.
RUN mkdir -p /app/custom_worlds /app/Players && \
    useradd --create-home --uid 10001 runner && \
    chown -R runner:runner /app
USER runner

ENTRYPOINT ["python"]

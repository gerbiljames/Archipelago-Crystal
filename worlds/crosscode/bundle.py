import json
import os
from zipfile import ZIP_DEFLATED, ZipFile
from .common import NAME, APWORLD_VERSION
from ..Files import APWorldContainer

DIRECTORY_EXCLUDES = (
    "pycache",
    "templates",
)

FILE_EXCLUDES = (
    "bundle",
)

def bundle():
    zipfile = ZipFile(f"crosscode.apworld", "w", compression=ZIP_DEFLATED, compresslevel=9)
    for root, _, files in os.walk("worlds/crosscode"):
        if all(e not in root for e in DIRECTORY_EXCLUDES):
            for filename in files:
                if all(e not in filename for e in FILE_EXCLUDES):
                    fullname = f"{root}/{filename}"
                    internal_name = f"{root[7:]}/{filename}"
                    print(f"Compressing {fullname} to {internal_name}")
                    zipfile.write(fullname, internal_name)
    with zipfile.open(f"archipelago.json", "w") as f:
        print(f"Generating manifest")

        container = APWorldContainer()
        container.game = NAME
        container.world_version = APWORLD_VERSION

        f.write(json.dumps(container.get_manifest()).encode())

    zipfile.close()

if __name__ == "__main__":
    bundle()

{{generated_comment | indent("# ", True)}}

from Utils import Version

NAME: str = "CrossCode"
BASE_ID: int = {{base_id}}
DATA_VERSION: str = "{{data_version}}"
APWORLD_VERSION: Version = Version({{version[0]}}, {{version[1]}}, {{version[2]}})

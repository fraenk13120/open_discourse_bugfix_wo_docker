from od_lib.definitions import path_definitions

required_paths = [
    path_definitions.DATA_RAW,
    path_definitions.DATA_CACHE,
    path_definitions.POLITICIANS_STAGE_01,
    path_definitions.ELECTORAL_TERMS
]

for path in required_paths:
    print(f"{'exists' if path.exists() else 'not existant'} {path}")
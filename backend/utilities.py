from pathlib import Path
import yaml
def read_config_file(file_path: Path):
    config = yaml.load(file_path.open(), yaml.FullLoader)
    return config

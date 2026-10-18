import os
from pathlib import Path

import yaml
from box import ConfigBox

from ResearchSummarizer.logging import logger


def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Load a YAML file as a ConfigBox (attribute-style access).

    Raises:
        ValueError: if the file is empty.
    """
    with open(path_to_yaml, encoding="utf-8") as yaml_file:
        content = yaml.safe_load(yaml_file)
    if not content:
        raise ValueError(f"YAML file is empty: {path_to_yaml}")
    logger.info(f"Loaded YAML file: {path_to_yaml}")
    return ConfigBox(content)


def create_directories(path_to_directories: list, verbose: bool = True) -> None:
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {path}")

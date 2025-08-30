import os
import yaml
from pathlib import Path
from typing import Any
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from src.ResearchSummarizer.logging import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read a YAML file and return its content as ConfigBox.
    
    Args:
        path_to_yaml (Path): Path to the YAML file.
    
    Raises:
        ValueError: If the YAML file is empty.
        Exception: For other unexpected errors.
    
    Returns:
        ConfigBox: Parsed YAML content as a ConfigBox object.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if not content:
                raise ValueError("YAML file is empty")
            logger.info(f"YAML file loaded successfully: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty or invalid")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"ceated dictionary at : {path}")
    
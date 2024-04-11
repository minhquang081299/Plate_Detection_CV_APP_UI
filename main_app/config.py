import os
from os.path import dirname
import yaml


ROOT = dirname(dirname(os.path.abspath(__file__))) # pointer to outside of virtual_fence module

CONFIG_PATH = os.path.join(ROOT, "resources", "config", "config.yaml")

def read_yaml_file(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data

CONFIG_DATA = read_yaml_file(CONFIG_PATH)


# config model
FOLDER_SAVE = CONFIG_DATA["FOLDER_SAVE"]

TESSERACT_PATH = CONFIG_DATA["TESSERACT_PATH"]



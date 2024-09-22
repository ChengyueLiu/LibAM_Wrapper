import json
import os

from Interface import BinProject
from tools import load_libraries


def main():
    bin_feature_extracted_libraries_json_path = ""
    bin_feature_dir = ""

    libraries = load_libraries(bin_feature_extracted_libraries_json_path)
    for lib in libraries:
        if not lib.is_valid:
            continue

        feature_json_file_name = f"{lib.id}.json"
        feature_json_file_path = os.path.join(bin_feature_dir, feature_json_file_name)
        if not os.path.exists(feature_json_file_path):
            continue

        # load feature
        bin_project = BinProject.init_from_dict(json.load(open(feature_json_file_path)))
        for elf_path in bin_project.elf_paths:
            print(elf_path)

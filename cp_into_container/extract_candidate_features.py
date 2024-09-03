import shutil
import sys, os
from settings import *

sys.path.append("code/anchor_detection/semantic_anchor_detection")
sys.path.append("code/binary_preprocess")
sys.path.append("code/embeddings_generate")
sys.path.append("code/anchor_reinforcement/anchor_alignment")
sys.path.append("code/reuse_area_exploration/Embeded-GNN")
sys.path.append("code/reuse_area_exploration/TPL_detection")
sys.path.append("code/reuse_area_exploration/reuse_area_detection")

import binary_preprocess as binary_preprocess_module


def cli():
    print("start generate candidate feature......")

    # candidate dir
    candidate_dir = os.path.join(DATA_PATH, "candidate")

    # children dir
    time_cost_dir = os.path.join(candidate_dir, "timecost")
    candidate_binary_dir_path = os.path.join(candidate_dir, "binaries")
    candidate_feature_dir_path = os.path.join(candidate_dir, "features")

    # clean the candidate_feature_dir_path, if not clean, these dir ends with "_" will cause errors.
    if os.path.exists(candidate_binary_dir_path):
        for item in os.listdir(candidate_binary_dir_path):
            item_path = os.path.join(candidate_binary_dir_path, item)
            if item.endswith("_") and os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)

    # extract feature
    binary_preprocess_module.getAllFiles(time_cost_dir,
                                         candidate_binary_dir_path,
                                         candidate_feature_dir_path, mode="1")

    print(f"ALl Done! feature saved in {candidate_feature_dir_path}")


if __name__ == "__main__":
    cli()

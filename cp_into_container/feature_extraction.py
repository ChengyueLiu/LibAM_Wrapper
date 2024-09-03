import sys, os
# import click
from settings import *

sys.path.append("code/anchor_detection/semantic_anchor_detection")
sys.path.append("code/binary_preprocess")
sys.path.append("code/embeddings_generate")
sys.path.append("code/anchor_reinforcement/anchor_alignment")
sys.path.append("code/reuse_area_exploration/Embeded-GNN")
sys.path.append("code/reuse_area_exploration/TPL_detection")
sys.path.append("code/reuse_area_exploration/reuse_area_detection")

import all_func_compare_isrd as anchor_detection_module
import binary_preprocess as binary_preprocess_module
import Generate_func_embedding as embeddings_generate_module
import get_tainted_graph as anchor_reinforcement_module
import fcg_gnn_score as embeded_gnn_module
import get_final_score_multi as TPL_detection_module1
import get_final_result_dict as TPL_detection_module2
import cal_result as TPL_detection_module3
import adjust_area as area_adjustment_module
import compare_area as reuse_area_detection_module


def cli():

    print("start generate candidate feature......")

    # candidate 信息文件夹
    candidate_dir = os.path.join(DATA_PATH, "candidate")

    # 子目录
    time_cost_dir = os.path.join(candidate_dir, "timecost")
    candidate_binary_dir_path = os.path.join(candidate_dir, "binaries")
    candidate_feature_dir_path = os.path.join(candidate_dir, "features")

    # 提取特征
    binary_preprocess_module.getAllFiles(time_cost_dir,
                                         candidate_binary_dir_path,
                                         candidate_feature_dir_path, mode="1")

    print(f"ALl Done! feature saved in {candidate_feature_dir_path}")


if __name__ == "__main__":
    cli()

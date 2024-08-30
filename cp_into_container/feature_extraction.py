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
    print("hello libAE")

    # 1. get feature and fcg
    print("start bianry preprocess......")
    feature_save_path =  DATA_PATH + "3_candidate/"
    binary_preprocess_module.getAllFiles(DATA_PATH + "3_candidate/timecost", DATA_PATH + "1_binary/candidate",
                                         feature_save_path, mode="1")

    print(f"ALl Done! feature saved in {feature_save_path}")

if __name__ == "__main__":
    cli()

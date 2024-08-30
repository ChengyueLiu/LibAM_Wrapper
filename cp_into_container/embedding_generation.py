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
    binary_preprocess_module.getAllFiles(DATA_PATH + "3_candidate/timecost", DATA_PATH + "1_binary/candidate",
                                         DATA_PATH + "3_candidate/", mode="1")

    # # # 2. get embedding
    print("generate in9 bl5 embedding......")
    embeddings_generate_module.subfcg_embedding(DATA_PATH+"4_embedding/timecost",
                                                DATA_PATH+"3_candidate/feature",
                                                DATA_PATH+"4_embedding/candidate_in9_bl5_embedding.json",
                                                model_path=WORK_PATH + "/code/embeddings_generate/gnn-best.pt")

    print("generate in9 embedding......")
    embeddings_generate_module.generate_afcg(DATA_PATH+"4_embedding/cdd_afcg",
                                            os.path.join(DATA_PATH, "3_candidate/fcg"),
                                            DATA_PATH+"4_embedding/candidate_in9_embedding.json",
                                            model_path=os.path.join(WORK_PATH, "code/reuse_area_exploration/Embeded-GNN/fcg_gnn-best-0.01.pt"))

    print("generate subgraph......")
    embeddings_generate_module.generate_subgraph(DATA_PATH+"4_embedding/cdd_subgraph",
                                            os.path.join(DATA_PATH, "3_candidate/fcg"),
                                            DATA_PATH+"4_embedding/candidate_in9_embedding.json",
                                            model_path=os.path.join(WORK_PATH, "code/reuse_area_exploration/Embeded-GNN/fcg_gnn-best-0.01.pt"))

    print(f"ALL Done! embedding saved in {DATA_PATH}4_embedding/")

if __name__ == "__main__":
    cli()

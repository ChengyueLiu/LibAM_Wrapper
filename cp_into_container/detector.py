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
    print(f"start detection!")

    # model path
    subfcg_model_path = os.path.join(WORK_PATH, "code/embeddings_generate/gnn-best.pt")
    afcg_model_path = os.path.join(WORK_PATH, "code/reuse_area_exploration/Embeded-GNN/fcg_gnn-best-0.01.pt")

    # target dir
    target_dir = os.path.join(DATA_PATH, "target")

    # time cost
    time_cost_dir = os.path.join(target_dir, "timecost")
    
    # 1. extract raw features
    target_raw_features_dir_path = os.path.join(target_dir, "raw_features")
    target_fcg_dir_path = os.path.join(target_raw_features_dir_path, "fcg")
    target_feature_dir_path = os.path.join(target_raw_features_dir_path, "feature")

    print("1. extract feature")
    binary_preprocess_module.getAllFiles(time_cost_dir,
                                         target_raw_features_dir_path, mode="1")

    # 2. generate embeddings
    # embedding
    target_embedding_dir_path = os.path.join(target_dir, "embeddings")
    target_in9_bl5_embedding_json_path = os.path.join(target_embedding_dir_path,
                                                         "target_in9_bl5_embedding.json")
    target_in9_embedding_json_path = os.path.join(target_embedding_dir_path, "target_in9_embedding.json")

    # acfg
    target_afcg_dir_path = os.path.join(target_dir, "afcg")

    # subgraph
    target_subgraph_dir_path = os.path.join(target_dir, "subgraph")

    # generate candidate embeddings
    print("2.1. generate in9 bl5 embedding......")
    embeddings_generate_module.subfcg_embedding(TIME_PATH=time_cost_dir,
                                                test_gemini_feat_paths=target_feature_dir_path,
                                                savePath=target_in9_bl5_embedding_json_path,
                                                model_path=subfcg_model_path)

    print("2.2. generate in9 embedding......")
    embeddings_generate_module.generate_afcg(fcg_path=target_fcg_dir_path,
                                             func_embedding_path=target_in9_embedding_json_path,
                                             save_path=target_afcg_dir_path,
                                             model_path=afcg_model_path)

    print("2.3. generate subgraph......")
    embeddings_generate_module.generate_subgraph(fcg_path=target_fcg_dir_path,
                                                 func_embedding_path=target_in9_embedding_json_path,
                                                 save_path=target_subgraph_dir_path,
                                                 model_path=afcg_model_path)

    # 3. function_compare
    # embedding annoy
    candidate_dir = os.path.join(DATA_PATH, "candidate")
    embedding_annoy_dir_path = os.path.join(candidate_dir, "embedding_annoy")

    function_compare_result_dir = os.path.join(DATA_PATH, "func_compare_result")
    function_compare_result_score_dir = os.path.join(function_compare_result_dir, "score")
    function_compare_result_score_top50_dir = os.path.join(function_compare_result_dir, "score_top50")

    print("3. function comparing......")
    anchor_detection_module.func_compare_annoy_fast_multi(
        target_in9_embedding_json_path,
        target_in9_embedding_json_path,
        function_compare_result_score_dir,
        function_compare_result_score_top50_dir,
        function_compare_result_dir,
        embedding_annoy_dir_path)

    # 4. TPL detection
    print("start fast TPL detection......")
    # candidate
    candidate_raw_features_dir_path = os.path.join(candidate_dir, "raw_features")
    candidate_fcg_dir_path = os.path.join(candidate_raw_features_dir_path, "fcg")
    candidate_feature_dir_path = os.path.join(candidate_raw_features_dir_path, "feature")
    candidate_afcg_dir_path = os.path.join(candidate_dir, "afcg")
    candidate_subgraph_dir_path = os.path.join(candidate_dir, "subgraph")
    candidate_embedding_dir_path = os.path.join(candidate_dir, "embeddings")
    candidate_in9_bl5_embedding_json_path = os.path.join(candidate_embedding_dir_path,
                                                         "candidate_in9_bl5_embedding.json")
    candidate_in9_embedding_json_path = os.path.join(candidate_embedding_dir_path, "candidate_in9_embedding.json")

    # results
    detection_result_dir_path = os.path.join(DATA_PATH, "tpl_detection_result")
    tpl_fast_result_dir_path = os.path.join(detection_result_dir_path, "tpl_fast_result")
    tpl_fast_area_dir_path = os.path.join(detection_result_dir_path, "tpl_fast_area")
    tpl_fast_time_dir_path = os.path.join(detection_result_dir_path, "tpl_fast_time")
    sim_func_list_dir_path = os.path.join(detection_result_dir_path, "sim_func_list")

    # detection
    anchor_reinforcement_module.tpl_detection_fast_annoy(
        tar_fcg_path=target_fcg_dir_path,
        cdd_fcg_path=candidate_fcg_dir_path,
        func_path=function_compare_result_score_dir,
        feature_save_path=tpl_fast_result_dir_path,
        area_save_path=tpl_fast_area_dir_path,
        time_path=tpl_fast_time_dir_path,
        tar_in9_embedding_json_path = target_in9_embedding_json_path,
        cdd_in9_embedding_json_path=candidate_in9_embedding_json_path,
        sim_funcs_path=sim_func_list_dir_path,
        obj_func_embeddings_path=target_in9_bl5_embedding_json_path,
        cdd_func_embeddings_path=target_in9_bl5_embedding_json_path,
        gnn_model_path=afcg_model_path,
        tar_afcg_path=target_afcg_dir_path,
        cdd_afcg_path=candidate_afcg_dir_path,
        tar_subgraph_path=target_subgraph_dir_path,
        cdd_subgraph_path=candidate_subgraph_dir_path)



    # TPL_detection_module2.get_result_json(os.path.join(DATA_PATH, save_path + "tpl_fast_result"),
    #                                       os.path.join(DATA_PATH, save_path + "tpl_fast_result.json"))

    # TODO 文件需要平铺，所以需要先建立这种映射关系。
    # TODO 文件到library的映射关系。

    print(f"ALL DONE, results saved in {DATA_PATH}6_tpl_fast_result/")


if __name__ == "__main__":
    cli()

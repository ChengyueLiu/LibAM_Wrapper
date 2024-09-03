# 1. all_func_compare_isrd.py
替换：`code/libam/code/anchor_detection/semantic_anchor_detection/all_func_compare_isrd.py`
修改人：思远
修改内容：生成candidate的向量数据库，修改了并发数量等。


# 2. get_tainted_graph.py
替换：`code/anchor_reinforcement/anchor_alignment/get_tainted_graph.py`
修改人：诚悦
修改内容：
    1227行：`def tpl_detection_fast_annoy(tar_fcg_path, cdd_fcg_path, func_path, feature_save_path, area_save_path, time_path, com_funcs_path, sim_funcs_path, obj_func_embeddings_path, cdd_func_embeddings_path, gnn_model_path, tar_afcg_path, cdd_afcg_path, tar_subgraph_path, cdd_subgraph_path):

    1. 修改函数参数，删除：com_funcs_path, 增加cdd_in9_embedding, tar_in9_embedding
    2. 替换原来的路径合并为这两个参
    3. 优化了多进程处理
`
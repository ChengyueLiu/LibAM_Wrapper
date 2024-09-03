# docker

## Quick Start
## pull image
`docker pull ivoryseeker/libam-img:latest`

## up container
`docker run -it -v /home/chengyue/projects/LibAM/data:/work/libam/data --name libam --gpus all ivoryseeker/libam-img:latest /bin/bash`

## re-up container(if needed)
`docker start libam && docker exec -it libam /bin/bash`

## cp files
`docker cp cp_into_container/*:/work/libam`

## use
edit the demo funciton in LibAM.py

`python LibAM.py`

# change:
1. cp feature_extraction.py, embedding_generation.py into /work/libam
1. all_func_compare_isrd.py ---> /work/libam/code/anchor_detection/semantic_anchor_detection

# pytorch
# uninstall old pytorch
`pip uninstall torch torchvision torchaudio`

# install pytorch 11.8 which is match to our cuda version
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`


# TODO rebuild image
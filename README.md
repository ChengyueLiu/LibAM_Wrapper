# docker
## pull image
`docker pull ivoryseeker/libam-img:latest`

## up container
`docker run -it -v /home/chengyue/projects/LibAM/data:/work/libam/data --name libam --gpus all ivoryseeker/libam-img:latest /bin/bash`

## re-up container
`docker start libam && docker exec -it libam /bin/bash`


# change:
1. cp feature_extraction.py, embedding_generation.py into /work/libam


# pytorch
# uninstall old pytorch
`pip uninstall torch torchvision torchaudio`

# install pytorch 11.8 which is match to our cuda version
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`


# TODO rebuild image
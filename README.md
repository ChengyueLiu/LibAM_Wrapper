# docker

## Requirements

1. pull image
   `docker pull ivoryseeker/libam-img:latest`

2. up container
   `docker run -it -v /home/chengyue/projects/LibAM/data:/work/libam/data --name libam --gpus all ivoryseeker/libam-img:latest /bin/bash`

3. put the files in `cp_into_container` into `/work/libam`

4. replace the files under `replace_files` into the container, the path is written in `Note.md`

## Frequently Use command:

1. re-up container(if needed)
   `docker start libam && docker exec -it libam /bin/bash`

2. cp files(if needed)
   `docker cp cp_into_container/*:/work/libam`

## Usage under container

### cd workspace

1. `cd container`
2. `cd /work/libam`

### prepare candidate

1. put candidate binaries under /data/dataset2/candidate/binaries
2. extract candidate raw features: `python3 extract_candidate_features.py`
3. genearate candidate embeddings: `python3 generate_candidate_embeddings.py`

### prepare target

1. put target binaries under /data/dataset2/target/binaries
2. run detector: `python3 detector.py`
3. check the result in `/data/dataset2/tpl_detection_result/tpl_detection_result.json`

### Usage by Wrapper(On Going)

`python LibAM.py`

# Changes

# Reinstall pytorch(if the installed pytorch is not match to the cuda version)

1. uninstall old pytorch
   `pip uninstall torch torchvision torchaudio`

2. install pytorch 11.8 which is match to our cuda version
   `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

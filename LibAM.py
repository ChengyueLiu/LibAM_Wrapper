import os
import shutil
import subprocess
import time


class LibAM:

    def __init__(self, data_dir_in_host):
        # paths
        self.data_dir = data_dir_in_host
        self.target_dir = os.path.join(self.data_dir, "target")
        self.target_binary_dir = os.path.join(self.target_dir, "binaries")
        self.result_dir = os.path.join(self.data_dir, "tpl_detection_result")
        self.result_json_file = os.path.join(self.result_dir, "tpl_fast_result.json")

        # commands
        # start container
        self.start_container_command = "docker start libam && docker exec -it libam /bin/bash"
        # cd workspace
        self.basic_command = "docker exec -it libam /bin/bash -c 'cd /work/libam && '"
        # extract feature
        self.extract_candidate_features_command = self.basic_command + "python3 extract_candidate_features.py'"
        # generate embeddings
        self.generate_candidate_embeddings_command = self.basic_command + "python3 generate_candidate_embeddings.py'"
        # detect
        self.detect_command = self.basic_command + "python3 detector.py'"

    def run_system_command(self, command):
        return subprocess.run(command, shell=True, capture_output=True, text=True)

    def start_container(self):
        """
        Make sure the container has been created with command: docker run -it -v /home/chengyue/projects/LibAM/data:/work/libam/data --name libam --gpus all ivoryseeker/libam-img:latest /bin/bash

        Use this function to up in the next time
        :return:
        """
        return self.run_system_command(self.start_container_command)

    def extract_candidate_features(self):
        """
        generate features for all candidate libraries

        :return:
        """
        return self.run_system_command(self.extract_candidate_features_command)

    def generate_candidate_embeddings(self):
        """
        generate embeddings for all candidate libraries

        :return:
        """
        return self.run_system_command(self.generate_candidate_embeddings_command)

    def detect(self, binary_path: str, result_path: str):
        """
        1. clean dirs
        2. copy target binary to target dir
        3. run scan
        4. copy out result

        :param binary_path:
        :param result_path:
        :return:
        """
        start_at = time.perf_counter()
        # clean dirs
        # copy target binary to target dir
        print("Copying target binary to target dir...")
        # shutil.copy(binary_path, self.target_binary_dir)

        # run scan
        print("Running scan...")
        self.run_system_command(self.detect_command)

        # copy out result
        print("Copying result...")
        shutil.copytree(self.result_json_file, result_path)

        scan_duration = time.perf_counter() - start_at
        print(f"ALL DONE in {scan_duration}s! Result saved in {result_path}")

        return result_path


def demo():
    data_dir_in_host = "/home/chengyue/projects/LibAM/data/dataset2"
    binary_path = "/home/chengyue/projects/LibAM/data/backup/binaries/bzip2"
    result_path = "/home/chengyue/projects/LibAM/demo_result.json"

    detector = LibAM(data_dir_in_host)
    # detector.start_container()
    # detector.extract_candidate_features()
    # detector.generate_candidate_embeddings()

    detector.detect(binary_path, result_path)


if __name__ == '__main__':
    demo()

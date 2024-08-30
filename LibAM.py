import os
import shutil
import subprocess
import time


class LibAM:

    def __init__(self, data_dir_in_host="/home/chengyue/projects/LibAM/data/dataset2"):
        self.data_dir_in_host = data_dir_in_host

        self.target_binary_dir_in_host = os.path.join(data_dir_in_host, "1_binary/target")
        self.target_info_dir_in_host = os.path.join(data_dir_in_host, "2_target")
        self.function_compare_result_dir_in_host = os.path.join(data_dir_in_host, "5_func_compare_result")
        self.tpl_fast_result_dir_in_host = os.path.join(data_dir_in_host, "6_tpl_fast_result")
        self.raw_detect_result_json_file_path = os.path.join(self.tpl_fast_result_dir_in_host, "tpl_fast_result.json")

        self.start_container_command = "docker start libam && docker exec -it libam /bin/bash"
        # 生成之前需要先删除之前的结果，否则会出现异常
        self.feature_generation_command = "docker exec -it libam /bin/bash -c 'cd /work/libam && rm -rf /work/libam/data/dataset2/1_binary/candidate/*_ && python3 feature_extraction.py'"
        self.embedding_generation_command = "docker exec -it libam /bin/bash -c 'cd /work/libam && python3 embedding_generation.py'"
        self.run_scan_command = "docker exec -it libam /bin/bash -c 'cd /work/libam && python3 detector.py'"

    def run_system_command(self, command):
        return subprocess.run(command, shell=True, capture_output=True, text=True)

    def start_container(self):
        """
        Make sure the container has been created with command: docker run -it -v /home/chengyue/projects/LibAM/data:/work/libam/data --name libam --gpus all ivoryseeker/libam-img:latest /bin/bash

        Use this function to up in the next time
        :return:
        """
        return self.run_system_command(self.start_container_command)

    def run_feature_generation(self):
        """
        generate features for all candidate libraries

        :return:
        """
        return self.run_system_command(self.feature_generation_command)

    def run_embedding_generation(self):
        """
        generate embeddings for all candidate libraries

        :return:
        """
        return self.run_system_command(self.embedding_generation_command)

    def run_scan(self):
        """
        scan the target binary

        :return:
        """
        return self.run_system_command(self.run_scan_command)

    def clean_dirs(self):
        """
        clean the directories to avoid unexpected exceptions

        :return:
        """
        # remove target files
        shutil.rmtree(self.target_binary_dir_in_host, ignore_errors=True)
        os.mkdir(self.target_binary_dir_in_host, ignore_errors=True)

        shutil.rmtree(self.target_info_dir_in_host, ignore_errors=True)
        shutil.rmtree(self.function_compare_result_dir_in_host, ignore_errors=True)
        shutil.rmtree(self.tpl_fast_result_dir_in_host, ignore_errors=True)

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
        print("Cleaning directories...")
        self.clean_dirs()

        # copy target binary to target dir
        print("Copying target binary to target dir...")
        shutil.copy(binary_path, self.target_binary_dir_in_host)

        # run scan
        print("Running scan...")
        self.run_scan()

        # copy out result
        print("Copying result...")
        shutil.copytree(self.raw_detect_result_json_file_path, result_path)

        scan_duration = time.perf_counter() - start_at
        print(f"ALL DONE in {scan_duration}s! Result saved in {result_path}")

        return result_path


def demo():
    data_dir_in_host = "/home/chengyue/projects/LibAM/data/dataset2"

    libam_detector = LibAM(data_dir_in_host)
    # libam_detector.start_container()
    # libam_detector.run_feature_generation()
    # libam_detector.run_embedding_generation()

    binary_path = "/home/chengyue/projects/LibAM/data/dataset2/1_binary_backup/target/bzip2"
    result_path = "/home/chengyue/projects/LibAM/data/demo_result.json"
    libam_detector.detect(binary_path, result_path)


if __name__ == '__main__':
    demo()

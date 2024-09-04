import json
import time
import argparse

from LibAM import LibAM


def main():
    parser = argparse.ArgumentParser(description='Run Arthas detection')
    parser.add_argument('binary_path', type=str, help='Path to the binary file')
    parser.add_argument('result_file_path', type=str, help='Path to save the result file')
    args = parser.parse_args()

    start_at = time.perf_counter()
    print(f"Detecting ...")
    data_dir_in_host = "/home/chengyue/projects/LibAM/data/dataset2"

    libam_detector = LibAM(data_dir_in_host)
    libam_detector.detect(args.binary_path, args.result_file_path)

    end_at = time.perf_counter()
    duration = round(end_at - start_at, 2)
    print(f"All done, duration: {duration} seconds.")


if __name__ == '__main__':
    main()

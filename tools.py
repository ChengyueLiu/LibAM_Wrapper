import csv
import json
import multiprocessing
import subprocess

from typing import List

import git
import yaml
from timeout_decorator import timeout
from tqdm import tqdm

from Interface import Library

import requests
import os


def load_libraries(file_path):
    """
    从json文件中加载Library对象

    :param file_path:
    :return:
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    for item in tqdm(data,"load libraries"):
        try:
            Library.init_from_dict(item)
        except Exception as e:
            print(f"Error in {item}: {e}")
    libraries = [Library.init_from_dict(item) for item in data]
    return libraries


def dump_libraries(libraries: List[Library], file_path):
    """
    保存Library对象到json文件

    :param libraries:
    :param file_path:
    :return:
    """
    libraries = [lib.customer_serialize() for lib in libraries]

    with open(file_path, 'w') as f:
        json.dump(libraries, f, indent=4)


def csv_to_list_of_dicts(file_path):
    """
    Read a csv file and return a list of dictionaries
    :param file_path:
    :return:
    """
    result = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    return result


def list_of_dicts_to_csv(data, file_path):
    """
    Write a list of dictionaries to a csv file
    :param data:
    :param file_path:
    :return:
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def load_libraries_from_csv(file_path: str):
    """
    从csv文件中加载Library对象
    headers:
        id
        library name
        library vendor
        is valid
        note
        source code link
        binary name
        binary homepage
        binary link

    :param file_path:
    :return:
    """
    library_dict_list = csv_to_list_of_dicts(file_path)

    libraries = []
    for library_dict in library_dict_list:
        library = Library(
            id=int(library_dict['id']),
            name=library_dict['library name'],
            vendor=library_dict['library vendor'],
            is_valid=True if library_dict['is valid'] == "True" else False,
            note=library_dict['note'],
            source_code_url=library_dict['source code link'],
            binary_name=library_dict['binary name'],
            binary_homepage=library_dict['binary homepage'],
            binary_pacakge_url=library_dict['binary link'],
            test_case_url=library_dict['binary link'],
        )
        libraries.append(library)
    return libraries


def dump_libraries_to_csv(libraries: List[Library], file_path: str):
    library_dict_list = []
    for library in libraries:
        library_dict = {
            # basic info
            'id': library.id,
            'library name': library.name,
            'library vendor': library.vendor,

            # is valid
            'is valid': "True" if library.is_valid else "False",
            'is src valid': "True" if library.is_src_feature_extracted else "False",
            'is bin valid': "True" if library.is_bin_feature_extracted else "False",
            'note': library.note,

            # source check
            "has_src": "True" if library.source_code_url else "False",
            "has_bin": "True" if library.binary_homepage else "False",
            "has_src_and_bin"" ": "True" if (library.source_code_url and library.binary_homepage) else "False",

            # src links
            'sources': "| ".join(library.sources) if len(library.sources) != 1 else library.sources[0],
            'source code link': library.source_code_url,

            # bin links
            'binary homepage': library.binary_homepage,
            "binary package count": len(library.binary_packages) if library.binary_packages else 0,
            "binary names": "| ".join(
                [pkg.file_name.strip() for pkg in library.binary_packages]) if library.binary_packages else "",
        }
        library_dict_list.append(library_dict)

    list_of_dicts_to_csv(library_dict_list, file_path)


def parse_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Parse the YAML file
            data = yaml.safe_load(file)
            return data
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return None


def clone_git_repository(url, to_path, depth=1):
    """
    Clone a git repository to the specified path
    """
    try:
        git.Repo.clone_from(url, to_path, depth=depth)
        return True
    except Exception as e:
        print(f"error when git clone {url}: {e}")
        return False


def clone_git_repository_wrap(args):
    return clone_git_repository(*args)


def download_file(url, to_path):
    try:
        # 发送GET请求到URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果请求不成功则抛出异常

        # 确保目标目录存在
        os.makedirs(os.path.dirname(to_path), exist_ok=True)

        # 以二进制写模式打开文件
        with open(to_path, 'wb') as file:
            # 逐块写入文件
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            return True
    except Exception as e:
        print(f"error when download {url}: {e}")
        return False


@timeout(60)
def download_file_wrap(args):
    try:
        return download_file(*args)
    except Exception as e:
        print(f"exception :{e}")
        return False


def multiprocess_download(links: List[str], save_dir: str):
    # make dir
    os.makedirs(save_dir, exist_ok=True)

    # generate tasks
    tasks = []
    for link in links:
        file_name = os.path.basename(link)
        to_path = os.path.join(save_dir, file_name)

        if not os.path.exists(to_path):
            tasks.append((link, to_path))
        else:
            print(f"Skip {file_name} as it already exists in {to_path}.")

    # download
    with multiprocessing.Pool(os.cpu_count() - 4) as pool:
        results = list(tqdm(pool.imap_unordered(download_file_wrap, tasks),
                            total=len(tasks),
                            desc="Downloading Libraries Binary Packages"))

    # check
    succeed_list = []
    failed_list = []
    for link, to_path in tasks:
        if os.path.exists(to_path):
            succeed_list.append((link, to_path))
        else:
            print(f"Download {link} failed!")
            failed_list.append((link, to_path))

    print(f"All Done, Succeed num: {len(succeed_list)}, Failed num: {len(failed_list)}.")

    return succeed_list, failed_list


@timeout(10)
def is_elf_file(file_path):
    if " " in file_path:
        return False
    if file_path.endswith(
            (".html", ".txt", ".c", ".cpp", ".xml", ".png", ".h", ".class", ".o", ".version", ".webp", ".ttf", ".go")):
        return False
    if "/usr/share/doc/" in file_path:
        return False
    if not ("bin" in file_path or "lib" in file_path):
        return False

    # 使用 file 命令判断输出是否包含ELF
    try:
        output = subprocess.check_output(f"file {file_path}", shell=True).decode()
        return file_path if "ELF" in output else False
    except Exception as e:
        print(e)
        return False


def find_files(dir_path, check_func):
    target_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                continue
            if check_func(file_path):
                target_files.append(file_path)
    return target_files


@timeout(2000)
def find_elf_files(dir_path, process_num=1, show_log=False):
    if show_log:
        print(f"load all file paths for finding elf files.")

    # 先找到所有的文件路径
    file_paths = []
    children_dirs = list(os.listdir(dir_path))
    children_dir_paths = [os.path.join(dir_path, child_dir_name) for child_dir_name in children_dirs]
    if show_log:
        children_dir_paths = tqdm(children_dir_paths, desc=f"load all file paths for finding elf files.")
    for child_dir_path in children_dir_paths:
        for root, dirs, files in os.walk(child_dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.islink(file_path):
                    continue
                file_paths.append(file_path)

    # 然后多进程找ELF文件
    target_files = []
    if process_num == 1:
        if show_log:
            print(f"load finished, start checking")
            file_paths = tqdm(file_paths, f"finding elf files")
        for path in file_paths:
            if is_elf_file(path):
                target_files.append(path)
    elif process_num > 1:
        with multiprocessing.Pool(process_num) as pool:
            if show_log:
                check_results = list(
                    tqdm(pool.imap_unordered(is_elf_file, file_paths), total=len(file_paths), desc=f"finding files"))
            else:
                check_results = list(pool.imap_unordered(is_elf_file, file_paths))
        for path in check_results:
            if path:
                target_files.append(path)

    if show_log:
        print(f"find finished, find {len(target_files)} elf files")
    return target_files

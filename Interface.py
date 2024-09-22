import dataclasses
from dataclasses import dataclass, asdict, fields
from enum import Enum
from typing import Dict, Type, Any, List


@dataclass
class Serializable:
    def customer_serialize(self) -> Dict[str, Any]:
        # 使用 asdict 来序列化所有实例属性，包括那些带默认值的
        serialized_data = asdict(self)
        # 额外处理复杂类型，例如含有 customer_serialize 方法的属性
        for field in fields(self):
            value = getattr(self, field.name)
            if hasattr(value, 'customer_serialize'):
                serialized_data[field.name] = value.customer_serialize()
            elif isinstance(value, list) and value and hasattr(value[0], 'customer_serialize'):
                serialized_data[field.name] = [item.customer_serialize() for item in value]
        return serialized_data

    @classmethod
    def init_from_dict(cls: Type['Serializable'], data: Dict[str, Any]) -> 'Serializable':
        init_args = {}
        for field in fields(cls):
            field_value = data.get(field.name)
            if hasattr(field.type, 'init_from_dict') and isinstance(field_value, dict):
                init_args[field.name] = field.type.init_from_dict(field_value)
            elif (isinstance(field_value, list) and
                  field.type.__args__ and
                  hasattr(field.type.__args__[0], 'init_from_dict') and
                  all(isinstance(i, dict) for i in field_value)):
                init_args[field.name] = [field.type.__args__[0].init_from_dict(item) for item in field_value]
            else:
                init_args[field.name] = field_value
        return cls(**init_args)


@dataclass
class LibrarySource(Enum):
    awesome_cpp = 'awesome_cpp'
    awesome_modern_cpp = 'awesome_modern_cpp'
    awesome_c = 'awesome_c'
    meson = "meson"
    clibs = 'clibs'
    spack = 'spack'
    xmake = 'xmake'
    hunter = 'hunter'
    github = 'github'
    gnu = 'gnu'
    nvd = 'nvd'
    vcpkg = 'vcpkg'
    conan = 'conan'
    manual_label = 'manual_label'
    debian = 'debian'


@dataclass
class DebianPackage(Serializable):
    """
    example:
        {
            "library_name": "openssl",
            "version_number": "1.1.1n",
            "ls_lr": "20231227T085326Z",
            "library_path": "pool/main/o/openssl",
            "component_name": "libssl1.1",
            "file_name": "libssl1.1_1.1.1n-0+deb10u3_amd64.deb"
        }

    walk:
        library_name
        version_number
        component_name
        file_name
    """
    id: int
    library_name: str
    version_number: str
    ls_lr: str
    library_path: str
    component_name: str
    file_name: str
    is_new_version: bool = True
    architecture: str = "all"
    is_valid: bool = True
    note: str = None

    # 对应的library的信息
    src_library_id: int = None
    src_library_name: str = None
    src_library_link: str = None

    def get_homepage_url(self):
        homepage_url = f"https://snapshot.debian.org/archive/debian/{self.ls_lr}/{self.library_path}/"
        return homepage_url

    def get_download_url(self):
        download_url = f"https://snapshot.debian.org/archive/debian/{self.ls_lr}/{self.library_path}/{self.file_name}"
        return download_url

    def download_to(self, save_dir):
        import os
        import requests
        download_url = self.get_download_url()
        file_path = os.path.join(save_dir, self.file_name)
        with open(file_path, 'wb') as f:
            response = requests.get(download_url)
            f.write(response.content)
        return file_path


@dataclass
class Library(Serializable):
    """
    library， 务必保证： TPLCorpus, Arthas, BinarySCA-TestSuite 三个项目中的Interface中的Library类属性相同, 方法允许有差别。

    """

    """library id"""
    id: int
    """原始名称(以源代码位置)"""
    name: str
    """binary name(以debian包为准)"""
    binary_name: str = None
    """别名"""
    alias: str = None
    """供应商"""
    vendor: str = None
    """官网"""
    homepage: str = None

    """源码地址"""
    source_code_url: str = None
    """二进制包主页"""
    binary_homepage: str = None
    """二进制包"""
    binary_packages: List[DebianPackage] = dataclasses.field(default_factory=list)
    """二进制包地址"""
    binary_pacakge_url_list: List[str] = dataclasses.field(default_factory=list)

    """其他homepages"""
    candidate_homepages: List[str] = dataclasses.field(default_factory=list)
    """其他候选地址"""
    candidate_source_code_urls: List[str] = dataclasses.field(default_factory=list)

    """描述"""
    description: str = None
    """收集来源"""
    sources: List[LibrarySource] = dataclasses.field(default_factory=list)

    """许可证(目前只是粗略收集，不可靠)"""
    licenses: List[str] = dataclasses.field(default_factory=list)
    """置信度"""
    confidence: int = None
    """出现次数"""
    occurrence: int = None
    """是否同时成功生成了源代码和二进制特征库 = is_src_feature_extracted & is_bin_feature_extracted"""
    is_valid: bool = True
    """是否成功生成了源代码特征库"""
    is_src_feature_extracted: bool = True
    """是否成功生成了二进制特征库"""
    is_bin_feature_extracted: bool = True
    """备注信息"""
    note: str = ""

    def __hash__(self):
        return hash((self.name, self.vendor))

    def __eq__(self, other: 'Library'):
        return self.get_uu_name() == other.get_uu_name() and self.vendor == other.vendor

    def __repr__(self):
        return f"{self.name}, {self.vendor}/{self.name}: {self.source_code_url} {self.occurrence}"

    def get_uu_name(self):
        """正规化名称，目前只是将名称转为小写"""
        return self.name.lower()


@dataclass
class SrcFunction(Serializable):
    name: str
    start_line: int
    end_line: int
    file_path: str
    source_codes: List[str]
    string_literals: List[str]


@dataclass
class SrcFile(Serializable):
    name: str
    extension: str
    path: str
    file_size_kb: float
    functions: List[SrcFunction]
    strings_not_in_functions: List[str]
    extraction_succeed = True
    extraction_log = None


@dataclass
class SrcProject(Serializable):
    name: str
    project_size_mb: float
    src_files: List[SrcFile]  # succeed extracted files

    # 提取统计摘要
    file_count: int = 0  # 所有的源代码文件数量，无论提取成功失败
    extraction_failed_file_count: int = 0  # 提取失败的文件数量
    function_count: int = 0  # 提取到的函数数量
    distinct_string_count: int = 0  # 提取到的字符串去重后的数量

    def __repr__(self):
        return f"project name: {self.name}, c/cpp file count: {len(self.src_files)}, c/cpp file size: {self.project_size_mb} mb."


@dataclass
class BinFile(Serializable):
    name: str
    extension: str
    path: str
    file_size_kb: float
    strings: List[str]


@dataclass
class BinPackage(Serializable):
    name: str
    bin_files: List[BinFile]

    vendor: str = None
    distinct_string_count: int = 0


@dataclass
class BinProject(Serializable):
    name: str
    bin_packages: List[BinPackage]

    package_count: int = 0
    elf_paths: List[str] = dataclasses.field(default_factory=list)

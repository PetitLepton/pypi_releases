from typing import Dict, List, Tuple
import pathlib
import requests
import yaml


def read_conda_file(file_path: str) -> str:
    """Returns the content of a conda environment file.
    
    Parameters
    ----------

    file_path: str
        Path to the conda environment file
        
    Returns
    -------

    str
        Content of the file"""

    if not isinstance(file_path, str):
        raise TypeError("The path to the conda file should be a string.")
    return pathlib.Path(file_path).read_text()


def extract_package_name_and_version(line: str) -> Tuple[str, str]:
    """Returns the name and the version of the package. If the version is not
    provided, it is set to Not provided.
    
    Parameters
    ----------

    package_line: str
        Line extracted from the conda environment file of the form package=version or package==version
            
    Returns
    -------

    Tuple[str, str] 
        Name and version of the package"""

    split_line = line.split("=")
    name = split_line[0]
    # It is mandatory to use the last element of the list
    # for the version as pip packages are written name==version
    version = split_line[-1] if len(split_line) > 1 else "Not provided"

    return (name, version)


def extract_all_packages_names_and_versions(file_content: str) -> List:
    """Returns the list of packages names and version from a conda environment
    file.

    Parameters
    ----------

    file_content: str 
        Content of the environment file

    Returns
    -------

    List[Tuple[str, str]]
        List of the names and versions of the packages"""

    parsed_content = yaml.safe_load(file_content)
    dependencies = parsed_content["dependencies"]

    packages_names_and_versions = []

    for p in dependencies:

        # Catch the conda packages
        if isinstance(p, str):
            packages_names_and_versions += [p]

        # Catch the pip packages
        if isinstance(p, dict):
            packages_names_and_versions += p["pip"]

    return packages_names_and_versions


def get_latest_version(package_name: str) -> str:
    """Get the latest release version of a package on PyPi by using the PyPi
    API.

    Parameters
    ----------

    package_name: str
        Name of the package

    Returns
    -------

    str
        Latest version of the package"""

    response = requests.get(url=f"https://pypi.org/pypi/{package_name}/json")

    if response.ok:
        content = response.json()
        return content.get("info").get("version")
    else:
        raise requests.ConnectionError()


def get_all_latest_versions(packages_names_and_versions: List[Tuple[str, str]]) -> List:
    """Returns the latest releases for a list of given packages
    
    Parameters
    ----------

    packages_names_and_versions: List[Tuple[str, str]]
        List of the tuples (name, version) of the packages
        
    Returns 
    -------

    List[Tuple[str, str, str]]
        List of the tuples (name, version, latest_version)"""

    new_releases = []
    for name, version in packages_names_and_versions:
        latest_version = get_latest_version(package_name=name)
        if latest_version != version:
            new_releases.append((name, version, latest_version))

    return new_releases


class CondaEnvironment:
    """Class conveniently wrapping the steps to extract the latest versions of
    the packages for a given conda environment file.

    Attributes
    ----------
    file_path: str
        Path to the conda environment file

    Methods
    -------

    get_all_latest_versions()
        Returns the latest versions of all the packages in the environment file
        if those are different from the current ones
    
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.packages = []

        file_content = read_conda_file(file_path=self.file_path)

        for line in extract_all_packages_names_and_versions(file_content=file_content):
            name, version = extract_package_name_and_version(line=line)
            # Do not add python as a package
            if name != "python":
                self.packages.append((name, version))

    def __repr__(self):
        versions = ";".join(
            [f"\n- {name}: {version}" for name, version in self.packages]
        )
        return f"List of packages in the environment file:{versions}."

    def get_all_latest_versions(self):
        return get_all_latest_versions(packages_names_and_versions=self.packages)

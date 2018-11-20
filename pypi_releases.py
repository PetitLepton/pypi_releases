import requests
import yaml


def packages_from_conda_env_file(conda_file_name):
    """Extract the packages from a YAML Conda environment
    file.
    See https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file"""
    with open(conda_file_name, "r") as f:
        content = yaml.load(f)

    dependencies = content["dependencies"]
    packages = list()
    for p in dependencies:
        if type(p) == str:
            name = p.split("=")[0]
            version = p.split("=")[-1]
            if name != "python":
                packages.append((name, version))
        if type(p) == dict:
            pip_dependencies = p["pip"]
            packages += [(p.split("=")[0], p.split("=")[-1]) for p in pip_dependencies]

    return dict(packages)


def get_latest_release(package):
    """Get the latest release version and date of a package
    on Pypi by using the PyPi API. The version date corresponds
    to the latest upload.

    Args:
        package (str): name of the pacckage
    Returns:
        dict(version=(str), verion_date=str())"""

    url = "https://pypi.org/pypi/{0}/json".format(package)
    response = requests.get(url=url)

    if response.ok:
        content = response.json()
        version = content.get("info").get("version")
        releases = content.get("releases")
        version_date = max(
            (list(upload["upload_time"] for upload in releases[version]))
        )
        latest_release = dict(version=version, version_date=version_date)
    else:
        latest_release = None
    return latest_release


def get_updates(packages):
    """"""
    updates = list()
    for package in packages.keys():
        version = packages[package]
        release = get_latest_release(package=package)
        if release:
            release_version = release["version"]
            if version != release_version:
                updates.append((package, version, release_version))

    return updates

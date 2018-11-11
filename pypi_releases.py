import json
import requests


def get_latest_release(package):
    """Get the latest release version and date of a package
    on Pypi by using the PyPi API. The version date corresponds
    to the latest upload.

    Args:
        package (str): name of the pacckage
    Returns:
        dict(version=(str), verion_date=str())"""

    url = f"https://pypi.org/pypi/{package}/json"
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


def store_latest_releases(packages):
    """"""
    latest_releases_file_name = "latest_releases.json"

    try:
        with open(latest_releases_file_name, "r") as latest_releases_file:
            pypi_releases = json.load(latest_releases_file)
    except FileNotFoundError:
        pypi_releases = dict()

    new_releases = list()
    for package in packages:
        release = get_latest_release(package=package)
        if package in pypi_releases.keys():
            current_version_date = pypi_releases[package].get("version_date")
            latest_version_date = release.get("version_date")
            if current_version_date < latest_version_date:
                pypi_releases[package] = release
                new_releases.append((package, release["version"]))
        else:
            pypi_releases[package] = release
            new_releases.append((package, release["version"]))

    with open(latest_releases_file_name, "w") as latest_releases_file:
        json.dump(pypi_releases, latest_releases_file, indent=2)

    return new_releases

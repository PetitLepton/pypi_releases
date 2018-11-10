import json
import requests
from bs4 import BeautifulSoup


def get_latest_release(package):
    """Get the latest release version and date of a package
    on Pypi. by scraping the pypi.org/project/{package}/#history.

    Args:
        package (str): name of the pacckage
    Returns:
        dict(version=(str), verion_date=str())"""

    url = f"https://pypi.org/project/{package}/#history"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    versions = [
        p.text.replace("\n", "").replace(" ", "")
        for p in soup.find_all("p", {"class": "release__version"})
    ]
    versions_dates = [
        list(p.children)[0]["datetime"]
        for p in soup.find_all("p", {"class": "release__version-date"})
    ]

    releases = list()
    for (version, version_date) in zip(versions, versions_dates):
        releases.append(dict(version=version, version_date=version_date))

    sorted_releases = list(
        sorted(releases, key=lambda d: d["version_date"], reverse=True)
    )

    if sorted_releases:
        latest_release = sorted_releases[0]
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

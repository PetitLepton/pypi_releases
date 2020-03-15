from pypi_releases import (
    extract_package_name_and_version,
    extract_all_packages_names_and_versions,
)


def test_extract_package_name_and_version():

    package = "request=1.0.0"
    expected_name, expected_version = "request", "1.0.0"
    output_name, output_version = extract_package_name_and_version(package)
    assert output_name == expected_name
    assert output_version == expected_version

    package = "request==1.0.0"
    expected_name, expected_version = "request", "1.0.0"
    output_name, output_version = extract_package_name_and_version(package)
    assert output_name == expected_name
    assert output_version == expected_version

    package = "request"
    expected_name, expected_version = "request", "Not provided"
    output_name, output_version = extract_package_name_and_version(package)
    assert output_name == expected_name
    assert output_version == expected_version


def test_extract_all_packages_names_and_versions():

    file_content = """
    name: env
    channels:
        - conda-forge
        - defaults
    dependencies:
        - python=3.8.0
    """

    expected = ["python=3.8.0"]
    output = extract_all_packages_names_and_versions(file_content)
    assert output == expected

    file_content = """
    name: env
    channels:
        - conda-forge
        - defaults
    dependencies:
        - pip:
            - request==1.0.0
    """

    expected = ["request==1.0.0"]
    output = extract_all_packages_names_and_versions(file_content)
    assert output == expected

    file_content = """
    name: env
    channels:
        - conda-forge
        - defaults
    dependencies:
        - python=3.8.0
        - pip=20.0.0
        - pip:
            - request==1.0.0
    """

    expected = ["python=3.8.0", "pip=20.0.0", "request==1.0.0"]
    output = extract_all_packages_names_and_versions(file_content)
    assert output == expected

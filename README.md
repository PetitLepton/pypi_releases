The following script allows to extract the packages from a conda environment file like
```yaml
name: analytics
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.6.6
  - jupyter=1.0.0
  - notebook=5.4.1
  - pandas=0.23.4
  - pip:
    - plotly==3.4.0
    - datasheets==0.1.0
```
and check if potential updates for the packages are available on PyPi. The code below shows an example of usage
```python
from pypi_releases import packages_from_conda_env_file, get_updates

if __name__ == "__main__":
    packages = packages_from_conda_env_file(conda_file_name="analytics.yml")
    updates = get_updates(packages=packages)
    versions = ";".join(
        [
            f"\n- {package}: {version} \u2192 {new_version}"
            for package, version, new_version in updates
        ]
    )
    print(f"These new PyPi versions have been released: {versions}.")

```

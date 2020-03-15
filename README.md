The following module allows to extract the packages from a conda environment file like
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
from pypi_releases import CondaEnvironment

conda_environment = CondaEnvironment(file_path="./analytics.yml")
latest_versions = conda_environment.get_all_latest_versions()
versions = ";".join(
    [
        f"\n- {package}: {version} \u2192 {new_version}"
        for package, version, new_version in latest_versions
    ]
)
print(f"These new PyPi versions have been released: {versions}.")
```
leading to
```
These new PyPi versions have been released: 
- notebook: 5.4.1 → 6.0.3;
- pandas: 0.23.4 → 1.0.2;
- plotly: 3.4.0 → 4.5.4;
- datasheets: 0.1.0 → 0.3.0.
```

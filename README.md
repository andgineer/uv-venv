<img align="left" width="200" src="uv-python.png" />

# uv-venv

Github Action to install [uv](https://github.com/astral-sh/uv) and create a virtual environment.

Compatible with Unix and Windows.

<br clear="left"/>

### Why
This action prevents Windows installation errors that occur when using uv without a virtual environment:

```shell
error: failed to remove file `C:\hostedtoolcache\windows\Python\3.10.11\x64\Lib\site-packages\../../Scripts/uv.exe`
  Caused by: Access is denied. (os error 5)
```

The error occurs because uv attempts to modify the global Python environment, which is restricted in GitHub Actions.

## Usage

```yaml
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Setup uv
      uses: andgineer/uv-venv@v2

    - name: Install dependencies
      run: uv pip install -r requirements.dev.txt
```

### Examples
* [andginee/opensearch-log](https://github.com/andgineer/opensearch-log/blob/0d1060c57a6adac85d3559b52ec714c931f3b671/.github/workflows/ci.yml#L44)
* [cookiecutter template](https://github.com/andgineer/cookiecutter-python-package)
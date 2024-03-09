<img align="left" width="200" src="uv-python.png" />

# uv-venv

Github Action to install [uv](https://github.com/astral-sh/uv) and create a virtual environment.

It works on both Unix and Windows.

<br clear="left"/>

This action is necessary because if you try to use uv in a GitHub Action without virtual environment, 
you will get an error on Windows like this:

```shell
error: failed to remove file `C:\hostedtoolcache\windows\Python\3.10.11\x64\Lib\site-packages\../../Scripts/uv.exe`
  Caused by: Access is denied. (os error 5)
```

This happens because, without a virtual environment, it tries to 
modify the global one, which is not allowed.

## Usage

```yaml
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Setup uv
      uses: andgineer/uv-venv@v1

    - name: Install dependencies
      run: uv pip install -r requirements.dev.txt
```

Example usage: [andginee/opensearch-log](https://github.com/andgineer/opensearch-log/blob/0d1060c57a6adac85d3559b52ec714c931f3b671/.github/workflows/ci.yml#L44).

It is also included to my [cookiecutter template](https://github.com/andgineer/cookiecutter-python-package)
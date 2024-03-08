<br/><br/>
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
    - name: Install uv environment
      uses: andgineer/uv-venv@v1
```

Example usage: [andginee/opensearch-log](https://github.com/andgineer/opensearch-log/blob/499da83c7f63786da43e5663140b0e20660d6f42/.github/workflows/ci.yml#L44).

# MP-Kiosk-Viewer
A small multi page kiosk browser. Written in python3 with the help of GTK and WebKit2. It has the ability to inject Javascritp code on successfull page load to handle e.g. automatic login as well as automatic http basic authentication.

## Requirements
- python3
- make¹
- zip¹

_¹ build dependency which is not needed for execution_<br>
_(If you have make already installed on an debian based distro you can quickly install the rest by executing `'sudo make requirements'`)_

## Configuration
The config of the software is done in the `config.py` python file. To set the pages of the mpkv add a `PAGES` array to the config file and fill it with 5 entry touples. The Elements of the touples are structured as follows:

| Element | Name | Description                                                                                                                        |
|:-------:| ---- | ---------------------------------------------------------------------------------------------------------------------------------- |
|    0    | name | The name of the tab which will be displayed to the user on the select button.                                                      |
|    1    | uri  | The uri of the page which should be loaded. Do NOT forget to prefix a url with `http://` or `https://`.                            |
|    2    | jsic | This is treated as javascript code which is always injected on successfull page load. This can be used to keep the user on a specific page or do automatic login. Use an empty string if you wish to not use it. |
|    3    | user | This is the username used to answer a http basic auth requests from the webserver. Set it to None to pass the request to the user. |
|    4    | pass | This is the password used to answer a http basic auth requests from the webserver.                                                 |

### Example
```python
PAGES = [
	("Google", "https://google.com/", "", None, None),
	("DuckDuckGo", "https://duckduckgo.com/", "", None, None)
]
```

## Building a executable
Building the software is not strictly neccesary it is possible if you want to test your settings or want to work on the system to run the `webview.py` file with python.
> `python3 webview.py`

If you want to build it you get one singe executable file which also bakes the configuration to itself so the settings can't be easily changed. The build command is:
> `make`

After the executable is made you can either use it as is anywhere on a system where `python3` is installed or you can install it into `~/.local/bin` with:
> `make install`

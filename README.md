# MP-Kiosk-Viewer
A small multi page kiosk browser. Written in python3 with the help of GTK and WebKit2. It has the ability to inject Javascritp code on successfull page load to handle e.g. automatic login as well as automatic http basic authentication.

## Requirements
- python3
- make
- zip

_(If you have make already installed you can quickly install the rest by executing `'sudo make requirements'`)_

## Config
The config of the software is done in the `config.py` python file. To set the pages of the mpkv add a `PAGES` array to the config file and fill it with 5 entry touples. The Elements of the touples are structured as follows:

| Element | Name | Description                                                                                                                        |
|:-------:| ---- | ---------------------------------------------------------------------------------------------------------------------------------- |
|    0    | name | The name of the tab which will be displayed to the user on the select button.                                                      |
|    1    | uri  | The uri of the page which should be loaded. Do NOT forget to prefix a url with `http://` or `https://`.                            |
|    2    | jsic | This is treated as javascript code which is always injected on successfull page load. This can be used to keep the user on a specific page or do automatic login. Use an empty string if you wish to not use it. |
|    3    | user | This is the username used to answer a http basic auth requests from the webserver. Set it to None to pass the request to the user. |
|    4    | pass | This is the password used to answer a http basic auth requests from the webserver.                                                 |

### Example
```
PAGES = [
	("Google", "https://google.com/", "", None, None),
	("DuckDuckGo", "https://duckduckgo.com/", "", None, None)
]
```

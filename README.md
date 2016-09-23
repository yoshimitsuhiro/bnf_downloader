## bnf_downloader

This is a python script for downloading books automatically from Bibliothèque nationale de France (BnF) Gallica digital library.

This script will download all pages of a selected book in the highest quality jpgs available.

Please note that sending too many requests to the library's server at once will both slow the server down and get your IP blocked temporarily. For this reason, I have added a timer to wait between downloads. Please be considerate and do not set the time interval too low.

This script requres the libraries [requests] (http://docs.python-requests.org/en/master/) and [regex] (https://bitbucket.org/mrabarnett/mrab-regex) to run.

When using this script in Windows, depending on your system locale, you may experience encoding errors in command prompt. This is a Windows problem and there is nothing that can be done to fix it in the code. To work around this issue, try changing the code table of command prompt to Code Page 850 using the following command: `chcp 850`.

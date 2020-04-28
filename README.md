# ig-dler_cli

A CLI tool which you can use to download DP, highlights, stories, posts of an instagram
profile without using the official instagram API

## __Prerequisites__

> python >3.7
> A Terminal of course xD

## __Requirements__

Before running the script you need the following installed.

Packages|
:---:|
request|
lxml|
pickle|
bs4|

## How to

```
git clone https://github.com/TH3-MA3STRO/ig-dler_cli
cd ig-dler_cli
pip install -r requirements.txt
python cli.py
```

then follow the on-screen instructions

## Detailed instructions for termux

1. Install [termux](https://play.google.com/store/apps/details?id=com.termux)
2. Open termux and type the following commands

    ```bash
    termux-setup-storage
    apt-get install python
    pkg install libxml2 libxslt git
    ```

3. Now change your current directory and clone this repository by entering the following command in termux

    ```bash
    cd storage/downloads
    git clone https://github.com/TH3-MA3STRO/ig-dler_cli.git
    cd ig-dler_cli
    ```

4. Now install the required packages using ```pip install -r requirements.txt```
5. Now the scripts is ready to use! To download private posts/stories/highlights of accounts you follow use

    ```shell
    python cli.py --login
    ```

    or use

    ```shell
    python cli.py
    ```

    to download public media

### Author: **Satyam Jha _[TH3-MA3STRO]_** (ig: @th3_ma3stro)

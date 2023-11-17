from setuptools import setup

setup(
    name="ymcli",
    version="0.2",
    description="Music player for yandex music",
    author="hikaary",
    author_email="hikary.local@gmail.com",
    packages=[
        "ymcli",
        "ymcli.ui",
        "ymcli.logs",
        "ymcli.ui.widgets",
    ],
    install_requires=[
        "aiofiles==23.2.1",
        "aiohttp==3.8.6",
        "aiosignal==1.3.1",
        "altgraph==0.17.4",
        "async-timeout==4.0.3",
        "attrs==23.1.0",
        "certifi==2023.7.22",
        "charset-normalizer==3.3.2",
        "frozenlist==1.4.0",
        "idna==3.4",
        "importlib-metadata==6.8.0",
        "linkify-it-py==2.0.2",
        "markdown-it-py==3.0.0",
        "mdit-py-plugins==0.4.0",
        "mdurl==0.1.2",
        "multidict==6.0.4",
        "packaging==23.2",
        "Pygments==2.16.1",
        "pyinstaller-hooks-contrib==2023.10",
        "PySocks==1.7.1",
        "python-vlc==3.0.20123",
        "requests==2.31.0",
        "rich==13.7.0",
        "setuptools==68.2.2",
        "textual==0.41.0",
        "typing_extensions==4.8.0",
        "uc-micro-py==1.0.2",
        "urllib3==2.1.0",
        "wheel==0.41.2",
        "yandex-music==2.1.1",
        "yarl==1.9.2",
        "zipp==3.17.0",
    ],
    entry_points={
        "console_scripts": [
            "ymcli=ymcli.__main__:main",
        ],
    },
)

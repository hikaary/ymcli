from setuptools import setup

setup(
    name="ymcli",
    version="1.0",
    description="Music player for yandex music",
    author="hikaary",
    author_email="hikary.local@gmail.com",
    packages=[
        "ymcli",
        "ymcli.ui",
        "ymcli.logs",
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
        "multidict==6.0.4",
        "npyscreen==4.10.5",
        "packaging==23.2",
        "PySocks==1.7.1",
        "python-vlc==3.0.20123",
        "requests==2.31.0",
        "setuptools==68.2.2",
        "urllib3==2.0.7",
        "wheel==0.41.2",
        "yandex-music==2.1.1",
        "yarl==1.9.2",
    ],
    entry_points={
        "console_scripts": [
            "ymcli=ymcli.__main__:main",
        ],
    },
)

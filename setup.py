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
        "yandex-music",
        "npyscreen",
        "python-vlc",
    ],
    entry_points={
        "console_scripts": [
            "ymcli=ymcli.__main__:main",
        ],
    },
)

from setuptools import setup

setup(
    name="ymcli",
    version="1.0",
    description="Music player for yandex music",
    author="hikaary",
    author_email="hikary.local@gmail.com",
    packages=["ymcli"],
    install_requires=[
        "yandex-music",
        "npyscreen",
        "python-vlc",
    ],
    scripts=["ymcli/ymcli.py"],
)

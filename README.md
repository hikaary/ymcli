<h3>Ymcli: open source Yandex.Music client / music player</h3>
  Uses <a href="https://github.com/MarshalX/yandex-music-api">unoffical Yandex.Music Api</a> 
</p>

<!-- ![Screenshot]()   -->

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/Version-0.0.1-x.svg?style=flat-square&logoColor=white&color=blue">
  <img alt="Stable" src="https://img.shields.io/badge/Stable-0.0.1-x.svg?style=flat-square&logoColor=white&color=blue">
</p>

## Installation 
* See [releases](https://github.com/hikaary/ymcli/releases)

* AUR (from source code), see [package](https://aur.archlinux.org/packages/ymcli)
  ```sh
  yay -S ymcli 
  ```

* Compile for Linux (from source code)
    ```sh
    #Install system dependencies
    sudo pacman -S vlc python pip 
    ```

    ```sh 
    git clone https://github.com/hikaary/ymcli
    cd ymcli 
    python setup.py install
    ```
* Use poetry
    ```sh
    git clone https://github.com/hikaary/ymcli
    cd ymcli 
    poetry install && poetry shell
    poetry run python -m ymcli
    ```

## First run
A token will be requested at the first startup.
You can get the token here by clicking this [link](https://yandex-music.readthedocs.io/en/main/token.html)


# Config & Logs
* Config file - `~/.config/ymcli/config.ini`
* Log file - `~/.local/ymcli/ymcli.log`

## Key actions 

| Key | Action |
| ------------- | ------------- |
| K | Move cursor up |
| J | Move cursor down |
| ENTER | Select |
| Space | Play/Pause |
| ESC | Got to playlists |
| UP | Volume up |
| DOWN | Volume down | 
| RIGHT | Fast forward the track by 5 seconds |
| LEFT | Rewind the track back 5 seconds |
| R | Repeat track |
| N | Skip track |
| P | Previous track |
| L | Like now playing track |
| D | Dislike now playing track | 

## Dependencies (excluding python dependencies)
* python 3.11
* vlc 3.0.20


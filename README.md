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
  sudo pacman -S vlc python pip
  git clone https://github.com/hikaary/ymcli
  cd ymcli 
  python setup.py install --root=ymcli
  ```
## Key actions 

| Key | Action |
| ------------- | ------------- |
| Space | Play/Pause |
| ESC | Got to playlists |
| UP | Volume up |
| DOWN | Volume down | 
| RIGHT | Fast forward the track by 5 seconds |
| LEFT | Rewind the track back 5 seconds |
| R | Repeat track |
| N | Skip track |
| P | Previous track |

## Dependencies
* python 3.11
* vlc 3.0.20


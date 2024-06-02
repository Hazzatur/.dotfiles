# .dotfiles

Welcome to my personal dotfiles repository! These configuration files are tailored for my EndeavourOS setup without a
desktop environment. This repository automates the installation and setup process for my preferred packages and
configurations.

## Installation

To set up your system using these dotfiles, follow these steps:

1. **Fresh Install of EndeavourOS**: Start with a clean installation of EndeavourOS without a desktop environment.

2. **Run the Setup Script**:
    ```sh
    python <(curl -s https://raw.githubusercontent.com/hazzatur/.dotfiles/main/scripts/.setup/install.py)
    ```

   This script will:
    - Install all the packages I use.
    - Clone this dotfiles repository.
    - Run the `./stow.sh` script to set up the configuration files.
    - Apply my settings and start LightDM.

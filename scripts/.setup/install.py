#!/usr/bin/env python3

import json
import os
import subprocess

home_dir = os.path.expanduser("~")


def print_bold(text):
    print(f"\033[1m{text}\033[0m")


def setup_dotfiles():
    dotfiles_path = f"{home_dir}/Personal/.dotfiles"
    print_bold("Checking if dotfiles exist")

    if not os.path.exists(dotfiles_path):
        print_bold("Cloning dotfiles")
        subprocess.run(["git", "clone", "https://github.com/Hazzatur/.dotfiles.git", dotfiles_path], check=True)

        print_bold("Changing remote URL to use SSH")
        subprocess.run(["git", "remote", "set-url", "origin", "git@github.com:Hazzatur/.dotfiles.git"],
                       cwd=dotfiles_path, check=True)
    else:
        print_bold("Dotfiles already exist. Skipping cloning.")

    print_bold("Setting up dotfiles")
    subprocess.run([f"{dotfiles_path}/stow.sh"], cwd=dotfiles_path, check=True)


def update_system():
    print_bold("Updating system with yay")
    subprocess.run(["yay", "-Syu"], check=True)


def check_package_exists(package, installer='yay'):
    command = ["pacman", "-Si", package] if installer == 'pacman' else ["yay", "-Si", package]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def install_packages(packages, installer='yay'):
    packages_to_install = []
    missing_packages = []
    print_bold(f"Checking if the packages exist...")
    for package in packages:
        if check_package_exists(package, installer):
            packages_to_install.append(package)
        else:
            missing_packages.append(package)

    if missing_packages:
        print_bold(f"The following packages were not found and will be skipped: {', '.join(missing_packages)}")

    if packages_to_install:
        if installer == 'pacman':
            cmd = ["sudo", "pacman", "-S"] + packages_to_install
        elif installer == 'yay':
            cmd = ["yay", "-S"] + packages_to_install
        else:
            print_bold("Unknown installer. Skipping package installation.")
            return

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print_bold("An error occurred while installing packages.")
            print_bold(f"Error details: {e}")


def configure_system():
    print_bold("Configuring system...")

    wallpaper = f"{home_dir}/.wallpaper/disperse01.jpg"

    if os.uname().nodename == "RED":
        subprocess.run([f"{home_dir}/.setup/fix_hp_screen.sh"], check=True)
    elif os.uname().nodename == "REDL":
        wallpaper = f"{home_dir}/.wallpaper/disperse02.jpg"

    subprocess.run([f"{home_dir}/.setup/deckboard.sh"], check=True)

    script_path = f"{home_dir}/.setup/configure_system.sh"
    subprocess.run(["bash", script_path, home_dir, wallpaper], check=True)


def main():
    update_system()

    packages_file = 'packages.json'
    if not os.path.exists(packages_file):
        print_bold("Downloading package list...")
        subprocess.run(["curl", "-s", "-o", "/tmp/packages.json",
                        "https://raw.githubusercontent.com/Hazzatur/.dotfiles/main/scripts/.setup/packages.json"],
                       check=True)
        packages_file = "/tmp/packages.json"

    try:
        with open(packages_file, 'r') as file:
            config = json.load(file)
    except Exception as e:
        print_bold(f"Failed to read configuration file: {e}")
        return

    for group_name, group_content in config.items():
        if not isinstance(group_content, dict):
            print_bold(
                f"Warning: Group '{group_name}' format is not valid and was skipped. It must specify 'pacman' or 'yay'.")
            continue

        response = input(
            f"\033[1mWould you like to install the apps in {group_name}? [Y/n]: \033[1m").strip().lower()
        if response in ('y', 'yes', ''):
            for installer, packages in group_content.items():
                install_packages(packages, installer='pacman' if installer == 'pacman' else 'yay')

    setup_dotfiles()
    configure_system()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_bold("User aborted the operation.")

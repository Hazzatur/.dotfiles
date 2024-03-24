#!/usr/bin/env python3

import json
import subprocess


def print_bold(text):
    print(f"\033[1m{text}\033[0m")


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


def main():
    update_system()

    try:
        with open('packages.json', 'r') as file:
            config = json.load(file)
    except Exception as e:
        print_bold(f"Failed to read configuration file: {e}")
        return

    for group_name, group_content in config.items():
        if not isinstance(group_content, dict):
            print_bold(
                f"Warning: Group '{group_name}' format is not valid and was skipped. It must specify 'pacman' or 'yay'.")
            continue

        response = input(f"\033[1mWould you like to install the apps in {group_name}? [Y/n]: \033[1m").strip().lower()
        if response in ('y', 'yes', ''):
            for installer, packages in group_content.items():
                install_packages(packages, installer='pacman' if installer == 'pacman' else 'yay')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_bold("User aborted the operation.")

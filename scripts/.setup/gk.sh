#!/usr/bin/env bash
#
# This script fetches the latest GitKraken CLI (gk) release from GitHub,
# saves it in ~/.local/bin, and makes it executable.

set -e

REPO_OWNER="gitkraken"
REPO_NAME="gk-cli"
INSTALL_DIR="$HOME/.local/bin"
ZSH_CUSTOM_COMPLETIONS="$HOME/.oh-my-zsh-custom/completions"

# Create the install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$ZSH_CUSTOM_COMPLETIONS"

echo "==> Fetching the latest release information from GitHub..."
LATEST_RELEASE_JSON=$(curl -s "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest")
LATEST_GK_URL=$(echo "$LATEST_RELEASE_JSON" |
  grep "browser_download_url" |
  grep "Linux_x86_64.zip" |
  cut -d '"' -f 4)

if [ -z "$LATEST_GK_URL" ]; then
  echo "Error: Could not find a download URL for gk in the latest release."
  exit 1
fi

FILENAME=$(basename "$LATEST_GK_URL")
DESTINATION="$INSTALL_DIR/$FILENAME"

echo "==> Download URL found: $LATEST_GK_URL"
echo "==> Downloading GitKraken CLI (gk) into $DESTINATION..."
wget -c "$LATEST_GK_URL" -O "$DESTINATION"

echo "==> Extracting the archive..."
unzip -o "$DESTINATION" -d "$INSTALL_DIR"
rm "$DESTINATION"

# Move the binary and make it executable
chmod +x "$INSTALL_DIR/gk"

echo "==> Moving completion file to ZSH custom completions..."
mv -f "$INSTALL_DIR/completions/_gk" "$ZSH_CUSTOM_COMPLETIONS/_gk"

# Remove the completions folder
rm -rf "$INSTALL_DIR/completions"

echo "==> GitKraken CLI (gk) has been installed in:"
echo "    $INSTALL_DIR/gk"
echo "==> Completion file has been moved to:"
echo "    $ZSH_CUSTOM_COMPLETIONS/_gk"

#!/usr/bin/env bash
#
# This script fetches the latest Deckboard AppImage from GitHub releases,
# saves it in ~/.local/bin, and makes it executable.

set -e

REPO_OWNER="rivafarabi"
REPO_NAME="deckboard"
INSTALL_DIR="$HOME/.local/bin"
FILENAME="deckboard.appimage"
DESTINATION="$INSTALL_DIR/$FILENAME"

# Create the install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

echo "==> Fetching the latest release information from GitHub..."
LATEST_APPIMAGE_URL=$(curl -s "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest" \
  | grep "browser_download_url" \
  | grep "AppImage" \
  | cut -d '"' -f 4)

if [ -z "$LATEST_APPIMAGE_URL" ]; then
  echo "Error: Could not find an AppImage URL in the latest release."
  exit 1
fi

echo "==> Download URL found: $LATEST_APPIMAGE_URL"
echo "==> Downloading Deckboard AppImage into $DESTINATION..."
wget -c "$LATEST_APPIMAGE_URL" -O "$DESTINATION"

echo "==> Making the AppImage executable..."
chmod +x "$DESTINATION"

echo "==> Deckboard AppImage has been saved to:"
echo "    $DESTINATION"

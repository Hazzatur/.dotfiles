#!/usr/bin/env python3

import json
import sys

from PyQt5 import QtWidgets, QtCore


class KeyChordInfoWindow(QtWidgets.QWidget):
    def __init__(self, _key_chord_info):
        super().__init__()
        self.key_chord_info = _key_chord_info
        self.init_ui()

    def init_ui(self):
        # Set window title and flags
        self.setWindowTitle(self.key_chord_info.get("name", "KeyChord Info"))
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )

        # Apply stylesheet for a modern, dark-themed look with rounded corners and padding
        self.setStyleSheet("""
            QWidget {
                background-color: "#1e1e2e";
                color: #94e2d5;
                border-radius: 16px;
            }
            QLabel {
                font-size: 12px;
                padding: 2px;
            }
            QLabel#title {
                font-size: 14px;
                font-weight: bold;
                padding: 4px;
            }
        """)

        # Create a vertical layout with centered alignment, margins, and spacing
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Title label (centered and styled)
        title = self.key_chord_info.get("name", "KeyChord Info")
        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("title")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Iterate over the keys and create labels for each entry
        for key_entry in self.key_chord_info.get("keys", []):
            key_text = key_entry.get("key", "")
            desc_text = key_entry.get("desc", "")
            entry_label = QtWidgets.QLabel(f"{key_text}: {desc_text}")
            entry_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(entry_label)

        self.setLayout(layout)
        self.adjustSize()
        self.center_on_screen()

    def center_on_screen(self):
        # Center the window on the primary screen
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("chord_info")

    if len(sys.argv) > 1:
        try:
            key_chord_info = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
            key_chord_info = {"name": "Invalid KeyChord", "keys": []}
    else:
        key_chord_info = {"name": "Default KeyChord", "keys": []}

    window = KeyChordInfoWindow(key_chord_info)
    window.show()
    sys.exit(app.exec_())

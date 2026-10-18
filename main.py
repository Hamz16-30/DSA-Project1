"""
Main Application Entry Point for CS200 Project 1 Desktop Application.
Initializes the PyQt6 graphical runtime, sets theme styles, and runs event loop.
"""
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from core.storage import StorageManager
from ui.main_window import MainWindow


def main() -> None:
    # Initialize Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("CS200-Restaurant-Analytics")
    app.setOrganizationName("UET-CS200")

    # Set default modern font
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)

    # Global stylesheet for clean, modern desktop aesthetics
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8fafc;
        }
        QWidget {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            color: #1e293b;
        }
        QPushButton {
            background-color: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #e2e8f0;
            border-color: #94a3b8;
        }
        QPushButton:pressed {
            background-color: #cbd5e1;
        }
        QLineEdit, QComboBox, QSpinBox {
            background-color: white;
            border: 1px solid #cbd5e1;
            padding: 5px 8px;
            border-radius: 4px;
            selection-background-color: #0284c7;
        }
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border: 1px solid #0284c7;
        }
        QStatusBar {
            background-color: #f1f5f9;
            color: #475569;
            font-size: 11px;
            border-top: 1px solid #e2e8f0;
        }
        QScrollBar:vertical {
            border: none;
            background: #f1f5f9;
            width: 10px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #cbd5e1;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background: #94a3b8;
        }
    """)

    # Initialize SQLite persistence
    storage = StorageManager("restaurants.db")

    # Launch Main Window
    window = MainWindow(storage)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

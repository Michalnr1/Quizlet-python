from PyQt6.QtGui import QIcon


def setColours(object):
    object.setWindowIcon(QIcon("icon.png"))
    object.setStyleSheet("""
                                QWidget {
                                    font-size: 14px;
                                }

                                QMainWindow {
                                    background-color: #f0f0f0;
                                }

                                QTreeWidget {
                                    background-color: #ffffff;
                                    border: 1px solid #c0c0c0;
                                    border-radius: 4px;
                                    font-size: 14px;
                                }

                                QPushButton {
                                    background-color: #007bff;
                                    color: #ffffff;
                                    border: none;
                                    padding: 8px 16px;
                                    border-radius: 4px;
                                    font-size: 14px;
                                }

                                QPushButton:hover {
                                    background-color: #0056b3;
                                }

                                QLineEdit {
                                    border: 1px solid #c0c0c0;
                                    border-radius: 4px;
                                    padding: 4px;
                                }

                                QLabel {
                                    font-size: 16px;
                                    font-weight: bold;
                                }

                                QPushButton#editButton {
                                    background-color: none;
                                    color: none;
                                    border: none;
                                }

                                QPushButton#editButton:hover {
                                    background-color: #007bff;
                                }
                            """)

import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStyleFactory,
    QStyleOptionComboBox,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph Plotter")
        self.init_ui()

    def init_ui(self):
        # Set dark theme style
        self.set_style()

        # Create labels
        self.x_label = QLabel("X Axis:")
        self.y_label = QLabel("Y Axis:")

        # Create combo boxes for selecting columns
        self.x_combo = QComboBox()
        self.y_combo = QComboBox()

        # Create button for opening file
        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file)

        # Create plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_graph)

        # Create layout for the labels and combo boxes
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.x_label)
        top_layout.addWidget(self.x_combo)
        top_layout.addWidget(self.y_label)
        top_layout.addWidget(self.y_combo)

        # Create layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.plot_button)

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)

        # Create central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def set_style(self):
        # Set dark theme style
        app.setStyle(QStyleFactory.create("Fusion"))

        # Set palette colors
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

        # Apply palette to the application
        QApplication.instance().setPalette(palette)

    def open_file(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )

        if filename:
            self.load_data(filename)

    def load_data(self, filename):
        self.data = pd.read_csv(filename, index_col=False)

        self.data.iloc[:, 0] = pd.to_datetime(self.data.iloc[:, 0], errors="coerce")

        # Set float data type for other columns and replace empty strings with NaN
        self.data.iloc[:, 1:] = self.data.iloc[:, 1:].apply(
            pd.to_numeric, errors="coerce"
        )

        # Populate combo boxes with column names
        self.x_combo.clear()
        self.y_combo.clear()
        self.x_combo.addItems(self.data.columns)
        self.y_combo.addItems(self.data.columns)

    def plot_graph(self):
        x_col = self.x_combo.currentText()
        y_col = self.y_combo.currentText()

        if x_col and y_col:
            sns.set(style="whitegrid")
            plt.figure(figsize=(10, 6))

            # Plot scatter plot with connecting lines
            sns.lineplot(
                data=self.data,
                x=x_col,
                y=y_col,
                marker="o",
                markersize=4,
                color="b",
                linewidth=2,
            )

            # Add grid
            plt.grid(True)

            # Set axis labels
            plt.xlabel(x_col, fontname="Times New Roman", fontsize=14)
            plt.ylabel(y_col, fontname="Times New Roman", fontsize=14)

            # Set graph title
            plt.title(
                "Graph Title",
                fontname="Times New Roman",
                fontsize=16,
                weight="bold",
                loc="center",
            )

            # Show the plot
            plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

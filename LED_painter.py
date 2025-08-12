# Standard
import sys
import json
from argparse import Namespace

# Third Party
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QColorDialog,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QImage, QPixmap, QPen, QAction, QPainter, QColor
from PySide6.QtCore import Qt, QPoint

# Local
from display_to_LEDs_from_file import display_to_LEDs
from LED_array_indices import LED_array_indices
from turn_off_LEDs import turn_off_LEDs


# window class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("RasQberry Two LED Painter")

        # setting geometry to main window
        self.setGeometry(100, 100, 960, 320)

        # creating image object (8x24)
        self.image = QImage(24, 8, QImage.Format_RGB32)

        # Scale factor
        self.scaleFactor = self.frameGeometry().width() / self.image.width()

        # making image color to white
        self.image.fill(Qt.black)

        # variables
        self.drawing = False  # drawing flag
        self.brushSize = 1  # default brush size
        self.brushColor = Qt.white  # default color
        self.lastPoint = QPoint()

        # creating menu bar
        mainMenu = self.menuBar()

        # creating file menu for save and clear action
        fileMenu = mainMenu.addMenu("File")

        # Adding sub-menus
        brushSizeMenu = mainMenu.addMenu("Brush Size")

        brushColorMenu = mainMenu.addMenu("Brush Color")

        displayMenu = mainMenu.addMenu("Display")

        # creating save action
        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        # creating clear action
        clearAction = QAction("Clear", self)
        clearAction.setShortcut("Ctrl + C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        # creating options for brush sizes
        size1 = QAction("1px", self)
        brushSizeMenu.addAction(size1)
        size1.triggered.connect(self.brushSize1)

        size2 = QAction("2px", self)
        brushSizeMenu.addAction(size2)
        size2.triggered.connect(self.brushSize2)

        # creating options for brush color
        colorWheel = QAction("Open Color Wheel", self)
        brushColorMenu.addAction(colorWheel)
        colorWheel.triggered.connect(self.colorWheel)

        displayToLEDs = QAction("Display this image on the LEDs", self)
        displayMenu.addAction(displayToLEDs)
        displayToLEDs.triggered.connect(self.displayToLEDs)

        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap.fromImage(self.image))

        layout = QVBoxLayout()
        layout.addWidget(imageLabel)
        self.show()

    # method for checking mouse clicks
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            painter = QPainter(self.image)
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            scaled_pos = self.scalePosition(event.pos())
            painter.drawPoint(scaled_pos)
            self.lastPoint = scaled_pos
            self.update()

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
        if (bool(event.buttons()) & bool(Qt.LeftButton)) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            scaled_pos = self.scalePosition(event.pos())
            painter.drawLine(self.lastPoint, scaled_pos)
            self.lastPoint = scaled_pos
            self.update()

    # method for mouse left button release
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    # paint event - scale the image to fit the window size
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # method for saving canvas
    def save(self):
        index_counter = 0
        pixel_dict = {}
        for y in range(self.image.height()):
            for x in range(self.image.width()):
                pixel_color = QColor(self.image.pixelColor(x, y)).getRgb()[:-1]
                new_index = LED_array_indices[index_counter]
                pixel_dict[new_index] = list(pixel_color)
                index_counter += 1

        # Write to file
        fileTypes = "JSON (*.json) ;; Plain Text (*.txt)"
        file_name = QFileDialog.getSaveFileName(self, "Save File", "", filter=fileTypes)
        file = open(file_name[0], "w")
        json.dump(pixel_dict, file, ensure_ascii=False, indent=4)
        file.close()

        # Display success message if saved
        if file:
            fileSavedDialog = QMessageBox(self)
            fileSavedDialog.setWindowTitle("File Saved Successfully")
            fileSavedDialog.setText(f"File saved to: \n{file.name}")
            fileSavedDialog.exec()

    # method for clearing everything on canvas
    def clear(self):
        self.image.fill(Qt.black)
        self.update()

        # Clear LEDs
        turn_off_LEDs()

    # methods for changing pixel sizes
    def brushSize1(self):
        self.brushSize = 1

    def brushSize2(self):
        self.brushSize = 2

    def colorWheel(self):
        newColor = QColorDialog.getColor(self.brushColor)
        self.brushColor = newColor

    # Helper function to scale the mouse position from window size to canvas size (8x24)
    def scalePosition(self, pos):
        scaled_x = pos.x() / self.scaleFactor
        scaled_y = pos.y() / self.scaleFactor
        # Ensure the coordinates are within the bounds of the canvas
        return QPoint(min(scaled_x, 31), min(scaled_y, 7))

    def displayToLEDs(self):
        # Get image data
        index_counter = 0
        pixel_dict = {}
        for y in range(self.image.height()):
            for x in range(self.image.width()):
                pixel_color = QColor(self.image.pixelColor(x, y)).getRgb()[:-1]
                new_index = LED_array_indices[index_counter]
                pixel_dict[new_index] = list(pixel_color)
                index_counter += 1

        # Clear LEDs before displaying new image, helps reduce issues
        turn_off_LEDs()

        display_to_LEDs(pixel_dict, Namespace(brightness=1.0, console=False))


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

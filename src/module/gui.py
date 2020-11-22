import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton, QLabel


class StartWindow(QMainWindow):
    def __init__(self, camera, logger=None):
        super().__init__()

        self.camera = camera
        self.logger = logger
        if self.logger is not None:
            self.logger.info("Created Camera")

        self.central_widget = QWidget()

        # Widgets: Buttons, Sliders, ...
        self.button_start = QPushButton("Start", self.central_widget)
        self.button_stop = QPushButton("Stop", self.central_widget)
        self.button_clear_qr = QPushButton("Clear Result", self.central_widget)
        self.image_view = QLabel()
        self.qrcode_label = QLabel()

        # Signals
        self.button_start.clicked.connect(self.start)
        self.button_stop.clicked.connect(self.stop)
        self.button_clear_qr.clicked.connect(self.clear_qrcode)

        # Timer for acquiring images at regular intervals
        self.acquisition_timer = QTimer()
        self.acquisition_timer.timeout.connect(self.update_image)

        # Widgets layout
        self.layout = QGridLayout(self.central_widget)
        self.layout.setColumnStretch(0, 10)
        self.layout.setColumnStretch(1, 1)
        self.layout.addWidget(self.button_start, 0, 1)
        self.layout.addWidget(self.button_stop, 1, 1)
        self.layout.addWidget(self.button_clear_qr, 2, 1)
        self.layout.addWidget(self.image_view, 0, 0, 10, 1)
        self.layout.addWidget(self.qrcode_label, 11, 0)

        self.setCentralWidget(self.central_widget)

    def start(self, update_interval=30):
        if not self.camera.is_initialized():
            self.camera.initialize()
        while self.camera.get_frame() is None:
            pass
        self.acquisition_timer.start(update_interval)

    def stop(self):
        self.camera.close_camera()
        self.image_view.clear()

    def update_image(self):
        frame = self.camera.get_frame()
        if frame is not None:
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self.image_view.setPixmap(pix)
            self.update_qrcode(frame)
        if self.logger is not None:
            self.logger.info("Updated frame with Maximum in frame: {}, Minimum in frame: {}".format(np.max(frame),
                                                                                                    np.min(frame)))

    def update_qrcode(self, frame):
        data = self.camera.read_qrcode(frame)
        if data != "":
            self.qrcode_label.setText(data)

    def clear_qrcode(self):
        self.qrcode_label.clear()

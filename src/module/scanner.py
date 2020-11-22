from cv2 import VideoCapture, QRCodeDetector, cvtColor, COLOR_BGR2RGB

# scanner module


class Camera(object):
    def __init__(self, cam_num=0):
        self.cam_num = cam_num
        self.cap = None
        self.initialized = False
        self.last_frame = None
        self.data = ""

    def initialize(self):
        self.cap = VideoCapture(self.cam_num)
        if not self.cap.isOpened():
            raise Exception("Could not open video device")
        self.initialized = True

    def is_initialized(self):
        return self.initialized

    def get_frame(self):
        _, self.last_frame = self.cap.read()
        if self.last_frame is not None:
            cvtColor(self.last_frame, COLOR_BGR2RGB, self.last_frame)
        return self.last_frame

    def read_qrcode(self, frame):
        detector = QRCodeDetector()
        self.data, _, _ = detector.detectAndDecode(frame)
        return self.data

    def close_camera(self):
        self.cap.release()
        self.initialized = False

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

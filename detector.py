"Insert docstring"
import cv2

class Detector:
    """
    Used to perform detections using a system camera
    """
    def __init__(self, config):
        self.config = config
        self.cascade = cv2.CascadeClassifier(config["cascade"])
        self.camera = cv2.VideoCapture(config["camera"])
        self.camera.set(6, cv2.VideoWriter_fourcc(*config["codec"]))
        self.camera.set(3, config["cameraResolution"][0]) # Camera heigth
        self.camera.set(4, config["cameraResolution"][1]) # Camera width
        self.fullScreen = config["fullScreen"]
        self.detectResolution = config["detectResolution"]

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def detect_image(self):
        """
        Performs a single detection with the camera and return the image
        """
        if not self.camera.isOpened():
            raise IOError("No camera")
        
        _, image = self.camera.read()
        faces = self.cascade.detectMultiScale(
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
            scaleFactor=self.config["scaleFactor"],
            minNeighbors=self.config["minNeighbors"],
            minSize=self.config["minSize"],
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (_x, _y, _w, _h) in faces:
            cv2.rectangle(image, (_x, _y), (_x+_w, _y+_h), (0, 255, 0), 2)

        return image


    def detect_video(self):
        """
        Starts a video capture and detects all objects
        """
        if not self.camera.isOpened():
            raise IOError("No camera")

        while True:
            _, image = self.camera.read()

            small_img = cv2.resize(image, self.detectResolution)
            gray = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            scale = self.config["scaleFactor"]
            neighbors = self.config["minNeighbors"]
            minS = self.config["minSize"]
            maxS = self.config["maxSize"]
            faces = self.cascade.detectMultiScale(
                gray,
                scaleFactor=scale,
                minNeighbors=neighbors,
                minSize=minS,
                maxSize=maxS,
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            scaleX = image.shape[0] / small_img.shape[0]
            scaleY = image.shape[1] / small_img.shape[1]
            for (_x, _y, _w, _h) in faces:
                _x = int(_x * scaleX)
                _y = int(_y * scaleY)
                _w = int(_w * scaleX)
                _h = int(_h * scaleY)
                cv2.rectangle(image, (_x, _y), (_x+_w, _y+_h), (0, 255, 0), 2)

            winName = "Detector de objetos"
            if self.fullScreen:
                cv2.namedWindow(winName, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(winName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            cv2.imshow(winName, image)

            # ESC to exit
            if cv2.waitKey(1) == 27:
                break

if __name__ == "__main__":
    print("Video test:")
    config = {
        "cascade": "data\\datasets\\lbpcascades\\lbpcascade_frontalface.xml",
        "camera": 0,
        "fullScreen": 0,
        "detectResolution": (480, 360)
    }
    det = Detector(config)
    det.detect_video()

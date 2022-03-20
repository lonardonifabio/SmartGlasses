
import cv2
import vlc
import pytesseract
from gtts import gTTS
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.rotation = 270

rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("s"):
                img = cv2.resize(image, None, fx=0.5, fy=0.5)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
                config = "--psm 3"
                text = pytesseract.image_to_string(adaptive_threshold, config=config)
                print(text)
                tts = gTTS(text, lang='en')
                tts.save('text.mp3')
                p = vlc.MediaPlayer("text.mp3")
                p.play()
                cv2.imshow("Frame", image)
                cv2.waitKey(0)
                break

cv2.destroyAllWindows()
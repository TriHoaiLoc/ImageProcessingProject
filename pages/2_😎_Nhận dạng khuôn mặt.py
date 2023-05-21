import streamlit as st
import numpy as np
import cv2 as cv
import joblib

class face_recogn():
    def __init__(self):
        self.FRAME_WINDOW = st.image([])
        self.cap = cv.VideoCapture(0)
        self.press = st.empty()
        self.tm = cv.TickMeter()
        self.svc = joblib.load('model/svc.pkl')
        self.mydict = ['BanKiet', 'BanNghia', 'BanThanh', 'SangSang', 'ThayDuc', 'TriHoaiLoc']
        self.detector = cv.FaceDetectorYN.create(
            'model/face_detection_yunet_2022mar.onnx',
            "",
            (320, 320),
            0.9,
            0.3,
            5000)
        self.recognizer = cv.FaceRecognizerSF.create(
            'model/face_recognition_sface_2021dec.onnx',"")

    @staticmethod
    def visualize_cam(input, faces, fps, thickness=2):
        if faces[1] is not None:
            for idx, face in enumerate(faces[1]):
                coords = face[:-1].astype(np.int32)
                cv.rectangle(input, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
                cv.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
                cv.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
                cv.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
                cv.circle(input, (coords[10], coords[11]), 2, (255, 0, 255), thickness)
                cv.circle(input, (coords[12], coords[13]), 2, (0, 255, 255), thickness)
        cv.putText(input, 'FPS: {:.2f}'.format(fps), (1, 16), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    @staticmethod
    def visualize_img(input, faces, thickness=2):
        if faces[1] is not None:
            for idx, face in enumerate(faces[1]):
                coords = face[:-1].astype(np.int32)
                cv.rectangle(input, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
                cv.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
                cv.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
                cv.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
                cv.circle(input, (coords[10], coords[11]), 2, (255, 0, 255), thickness)
                cv.circle(input, (coords[12], coords[13]), 2, (0, 255, 255), thickness)

    @staticmethod
    def checkname(self, faces, frame):
        if faces[1] is not None:
                face_align = self.recognizer.alignCrop(frame, faces[1][0])
                face_feature = self.recognizer.feature(face_align)
                test_predict = self.svc.predict(face_feature)
                result = self.mydict[test_predict[0]]
                cv.putText(frame,result,(1,50),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def main_cam(self):
        if 'stop' not in st.session_state:
            st.session_state.stop = False
            stop = False
        
        if self.press:
            if st.session_state.stop == False:
                st.session_state.stop = True
                self.cap.release()
                self.press.button("Start")
            else:
                st.session_state.stop = False
                self.press.button("Stop")
        
        if 'frame_stop' not in st.session_state:
            frame_stop = cv.imread('img\webcam-not-working.jpg')
            st.session_state.frame_stop = frame_stop

        if st.session_state.stop == True:
            self.FRAME_WINDOW.image(st.session_state.frame_stop, channels='BGR')

        st.subheader('Nhận dạng khuôn mặt bằng camera')

        frameWidth = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.detector.setInputSize([frameWidth, frameHeight])

        while True:
            hasFrame, frame = self.cap.read()
            if not hasFrame:
                break

            frame = cv.resize(frame, (frameWidth, frameHeight))  
            
            self.tm.start()
            faces = self.detector.detect(frame) # faces is a tuple
            self.tm.stop()
            
            self.checkname(self, faces, frame)

            # Draw results on the input image
            self.visualize_cam(frame, faces, self.tm.getFPS())

            # Visualize results
            self.FRAME_WINDOW.image(frame, channels='BGR')
        cv.destroyAllWindows()

    def main_img(self):
        fileimg = st.file_uploader("Chọn 1 hình ảnh...", type=["jpg", "jpeg", "png","tif", "bmp"])
        st.subheader('Nhận dạng khuôn mặt bằng hình ảnh')

        if fileimg:
            img_color = cv.imdecode(np.frombuffer(fileimg.read(), np.uint8), cv.IMREAD_COLOR)
            img = cv.cvtColor(img_color , cv.COLOR_BGR2RGB)
            
            frameHeight, frameWidth = img.shape[:2]
            self.detector.setInputSize([frameWidth, frameHeight])

            faces = self.detector.detect(img) # faces is a tuple

            self.checkname(self, faces, img)

            # Draw results on the input image
            self.visualize_img(img, faces)

            # Visualize results
            self.FRAME_WINDOW.image(img, channels='RGB')
             
if __name__=='__main__':
    st.header("Nhận dạng khuôn mặt")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    option = st.sidebar.radio('Nhận dạng khuôn mặt: ',['Bằng hình ảnh','Bằng camera'])
    
    face = face_recogn()
    
    if option == "Bằng camera":
        face.main_cam()
    else:
        face.main_img()
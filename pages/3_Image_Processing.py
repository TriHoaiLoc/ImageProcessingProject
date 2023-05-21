import cv2 as cv
import streamlit as st
import numpy as np
import lib.Chapter03 as ch3
import lib.Chapter04 as ch4
import lib.Chapter05 as ch5
import lib.Chapter09 as ch9

def openGrey(fileimg):
    img_Grey = cv.imdecode(np.frombuffer(fileimg.read(), np.uint8), cv.IMREAD_GRAYSCALE)
    return img_Grey

def openColor(fileimg):
    img_color = cv.imdecode(np.frombuffer(fileimg.read(), np.uint8), cv.IMREAD_COLOR)
    img = cv.cvtColor(img_color , cv.COLOR_BGR2RGB)
    return img

def DenoisesMotion(imgin):
    img = cv.medianBlur(imgin, 8)
    return ch5.DenoiseMotion(img)

def default_process():
    return cv.imread('img/no-img.jpg')

def ImgProcessing(option, imgin):
    options = {
        #chapter 3
        '1. Negative': ch3.Negative,
        '2. Logarit': ch3.Logarit,
        '3. Power': ch3.Power,
        '4. Piecewise Linear': ch3.PiecewiseLinear, 
        '5. Histogram': ch3.Histogram, 
        '6. Histogram Equalization': ch3.HistEqual,
        '7. Histogram Equalization Color': ch3.HistEqualColor, 
        '8. Local Histogram': ch3.LocalHist, 
        '9. Histogram Statistic': ch3.HistStat, 
        '10. Box Filter': ch3.BoxFilter, 
        '11. Gaussian Filter': ch3.GaussFilter,
        '12. Threshold': ch3.Threshold, 
        '13. Median Filter': ch3.MedianFilter, 
        '14. Sharpen': ch3.Sharpen, 
        '15. Gradient': ch3.Gradient,
        #chapter 4
        '1. Spectrum': ch4.Spectrum, 
        '2. Highpass Filter': ch4.FrequencyFilter, 
        '3. Draw Notch Reject Filter': ch4.DrawNotchRejectFilter, 
        '4. Remove Moire': ch4.RemoveMoire,
        #chapter 5
        '1. Tạo nhiễu chuyển động': ch5.CreateMotionNoise, 
        '2. Gỡ nhiễu của ảnh có ít nhiễu': ch5.DenoiseMotion, 
        '3. Gỡ nhiễu của ảnh có nhiều nhiễu': DenoisesMotion,
        #chapter 9
        '1. Connected Component': ch9.ConnectedComponent, 
        '2. Count Rice': ch9.CountRice,

    }

    imgout = options.get(option, default_process)(imgin)
    return imgout

if __name__=="__main__":
    st.header("Xử lý ảnh")
    st.markdown("<hr>", unsafe_allow_html=True)

    nameChapter = ('CHƯƠNG 3', 'CHƯƠNG 4', 'CHƯƠNG 5', 'CHƯƠNG 9')
    nameChapter3 = ('1. Negative', '2. Logarit', '3. Power', '4. Piecewise Linear', '5. Histogram', '6. Histogram Equalization',
                    '7. Histogram Equalization Color', '8. Local Histogram', '9. Histogram Statistic', '10. Box Filter', '11. Gaussian Filter',
                    '12. Threshold', '13. Median Filter', '14. Sharpen', '15. Gradient')
    nameChapter4 = ('1. Spectrum', '2. Highpass Filter', '3. Draw Notch Reject Filter', '4. Remove Moire')
    nameChapter5 = ('1. Tạo nhiễu chuyển động', '2. Gỡ nhiễu của ảnh có ít nhiễu', '3. Gỡ nhiễu của ảnh có nhiều nhiễu')
    nameChapter9 = ('1. Connected Component', '2. Count Rice')

    option1 = st.selectbox('Chương:', nameChapter)

    if option1 == nameChapter[0]:
        option2 = st.sidebar.radio(option1, nameChapter3)
    elif option1 == nameChapter[1]:
        option2 = st.sidebar.radio(option1, nameChapter4)
    elif option1 == nameChapter[2]:
        option2 = st.sidebar.radio(option1, nameChapter5)
    else:
        option2 = st.sidebar.radio(option1, nameChapter9)

    st.write('Bạn đang chọn:', '<span style="color: yellow;">'+option1+'</span>', unsafe_allow_html=True)
    st.write('Phương pháp xử lý ảnh đang chọn là: ', '<span style="color: yellow;">'+option2+'</span>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    fileimg = st.file_uploader("Chọn 1 hình ảnh...", type=["jpg", "jpeg", "png","tif"])
    st.markdown("<hr>", unsafe_allow_html=True)

    if fileimg:
        if option2 == nameChapter3[6]:
            imgin = openColor(fileimg)
        else:
            imgin = openGrey(fileimg)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Trước")
            FRAME_WINDOW_INPUT = st.image([])
            FRAME_WINDOW_INPUT.image(imgin)

        with col2:
            run = st.button("Run")
            if run:
                imgout = ImgProcessing(option2, imgin)

        with col3:
            st.header("Sau")
            FRAME_WINDOW_OUTPUT = st.image([])
            if run:
                FRAME_WINDOW_OUTPUT.image(imgout)

import streamlit as st

#Thông tin
def main():
    # Tạo tiêu đề cho trang
    st.set_page_config(
        page_title="Xử lý ảnh", 
        page_icon="📷",
    )
    st.header("CHÀO MỪNG TỚI TRANG WEB")
    st.write("**Sinh viên:** Trì Hoài Lộc - 20133063")
    st.write("**GVHD:** Trần Tiến Đức")
    st.write("**Mã lớp học:** DIPR430685_22_2_10")
    st.markdown(
        """
        ## Đây là đồ án của môn học xử lý ảnh 
        ### Gồm 3 phần:
        1. Phát hiện khuôn mặt
        2. Nhận dạng khuôn mặt
        3. Xử lý ảnh
        
        ### Link
        - Github: **https://github.com/TriHoaiLoc/ImageProcessingProject**
        - Deploy: **https://trihoailoc-imageprocessingproject-home-e1mf0s.streamlit.app/**
        <br><br>
        <div style="text-align: right;">Thành phố Hồ Chí Minh, tháng 5 năm 2023</div>
        """, unsafe_allow_html=True
    )
    

if __name__=='__main__':
    main()

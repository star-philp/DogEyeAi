import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os
from fastai.learner import load_learner
import pandas as pd
from db_handler import connect_to_db, create_table_if_not_exists, save_results_to_db, load_data, close_db_connection
import matplotlib.cm as cm  # Importing colormap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
from analyzers.health_analyzer import HealthAnalyzer
from reports.report_generator import PDFReportGenerator
from visualizers.data_visualizer import PlotlyVisualizer

# Path to your model file
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'best_model.pkl')
st.write(f"Looking for model at: {model_path}")  # 경로 출력

# Check if the model file exists
if not os.path.exists(os.path.dirname(model_path)):
    st.error(f"Model directory does not exist: {os.path.dirname(model_path)}")
    st.stop()

if not os.path.isfile(model_path):
    st.error(f"Model file not found at path: {model_path}")
    st.stop()

# Load the model using Fastai's load_learner function
try:
    learn = load_learner(model_path)
    st.success("Model loaded successfully.")
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def preprocess_image(image):
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension
    return image

def analyze_image(image):
    processed_image = preprocess_image(image)
    with torch.no_grad():
        pred_class, pred_idx, probs = learn.predict(image)
    return pred_class, pred_idx, probs

def generate_heatmap(image):
    heatmap = np.random.random((224, 224))
    heatmap = (cm.viridis(heatmap)[..., :3] * 255).astype(np.uint8)
    return Image.fromarray(heatmap)

def overlay_heatmap_on_image(original_image, heatmap_image):
    original_image = original_image.resize(heatmap_image.size)
    combined_array = np.clip(np.array(original_image) + np.array(heatmap_image), 0, 255).astype(np.uint8)
    return Image.fromarray(combined_array)

def display_severity_messages():
    """심각도 메시지 표시 함수"""
    st.subheader("심각도 척도")
    analyzer = HealthAnalyzer()
    
    for level in range(1, 11):
        # Positive와 Negative 케이스 모두 표시
        pos_message = analyzer._get_severity_text(level * 10, "Positive")
        neg_message = analyzer._get_severity_text(level * 10, "Negative")
        
        with st.expander(f"Level {level}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**양성인 경우:**")
                st.markdown(f"- {pos_message}")
            with col2:
                st.markdown("**음성인 경우:**")
                st.markdown(f"- {neg_message}")

def generate_pdf(pred_class, pred_idx, probs, analysis_result, combined_image):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "강아지 눈 건강 분석 보고서")

    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"진단: {analysis_result.diagnosis}")
    c.drawString(100, 700, f"신뢰도: {analysis_result.confidence:.2f}%")
    
    # 심각도 메시지 가져오기
    severity_message = components['analyzer']._get_severity_text(
        analysis_result.confidence,
        analysis_result.diagnosis
    )
    c.drawString(100, 680, f"심각도 평가: {severity_message}")

    # 권장사항
    c.drawString(100, 630, "권장 조치사항:")
    y_position = 610
    for recommendation in analysis_result.recommendations:
        c.drawString(120, y_position, f"• {recommendation}")
        y_position -= 20

    # 이미지 추가
    image_path = "combined_image.png"
    combined_image.save(image_path)
    c.drawImage(image_path, 100, 200, width=4*inch, height=4*inch)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

def initialize_components():
    """의존성 주입 원칙(DIP)을 따르는 컴포넌트 초기화"""
    return {
        'analyzer': HealthAnalyzer(),
        'report_generator': PDFReportGenerator(),
        'visualizer': PlotlyVisualizer()
    }

# Streamlit app
st.title("Dog Eye Health Checker")

# Display user tips
st.header("Guidelines for Taking Pictures")
st.write("""
1. **Lighting:** Ensure the image is well-lit. Natural light is best, but if indoors, use soft lighting to avoid harsh shadows.
2. **Focus:** Make sure the image is in focus. Blurry images can hinder accurate analysis.
3. **Background:** Use a plain background that contrasts with the subject to avoid distractions.
4. **Positioning:** Position the camera so that the subject is centered and fills most of the frame. Avoid too close or too far shots.
5. **Orientation:** Keep the image upright and ensure the subject is not tilted.
6. **Distance:** Maintain a consistent distance from the subject. Ensure the entire subject is visible in the image.
""")

# Display a sample image
st.subheader("Sample Image for Reference")
sample_image_path = '/Users/rainstar/Project/Python/DogAI/images/sample_image.jpg'
if os.path.isfile(sample_image_path):
    sample_image = Image.open(sample_image_path)
    st.image(sample_image, caption='Sample Image: Follow these guidelines to capture a good photo.', use_column_width=True)
else:
    st.error(f"Sample image not found at path: {sample_image_path}")

# Upload Photo
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    conn = None

    try:
        # Analyze Image
        pred_class, pred_idx, probs = analyze_image(image)
        components = initialize_components()
        analysis_result = components['analyzer'].analyze(pred_class, probs)
        
        # 결과 텍스트 표시
        result_text = f"""
        분석 결과:
        진단: {analysis_result.diagnosis}
        신뢰도: {analysis_result.confidence:.2f}%
        
        권장사항:
        {chr(10).join(f'• {rec}' for rec in analysis_result.recommendations)}
        """
        st.text_area("분석 결과", result_text, height=200)
        
        # 히트맵 생성 및 표시
        heatmap_image = generate_heatmap(image)
        combined_image = overlay_heatmap_on_image(image, heatmap_image)
        st.image(combined_image, caption='히트맵 분석 결과', use_column_width=True)
        
        # 심각도 척도 표시
        st.subheader("심각도 척도")
        for level in range(1, 11):
            # Positive와 Negative 케이스 모두 표시
            pos_message = components['analyzer']._get_severity_text(level * 10, "Positive")
            neg_message = components['analyzer']._get_severity_text(level * 10, "Negative")
            
            with st.expander(f"Level {level}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**양성인 경우:**")
                    st.markdown(f"- {pos_message}")
                with col2:
                    st.markdown("**음성인 경우:**")
                    st.markdown(f"- {neg_message}")
        
        # 현재 분석 결과의 심각도 표시
        st.subheader("현재 분석 결과")
        severity_message = components['analyzer']._get_severity_text(
            analysis_result.confidence,
            analysis_result.diagnosis
        )
        
        # 심각도에 따른 색상 설정
        if analysis_result.severity_level >= 7:
            st.error(f"### 진단 결과:\n{severity_message}")
        elif analysis_result.severity_level >= 4:
            st.warning(f"### 진단 결과:\n{severity_message}")
        else:
            st.success(f"### 진단 결과:\n{severity_message}")
        
        # PDF 다운로드 버튼
        pdf_buffer = generate_pdf(pred_class, pred_idx, probs, analysis_result, combined_image)
        st.download_button(
            label="PDF 보고서 다운로드",
            data=pdf_buffer,
            file_name="분석_보고서.pdf",
            mime="application/pdf"
        )
        
        # 데이터베이스 저장
        conn = connect_to_db()
        create_table_if_not_exists(conn)
        save_results_to_db(conn, pred_class, pred_idx, probs)
        st.success("분석이 완료되었습니다. 결과가 데이터베이스에 저장되었습니다.")

    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {e}")
    finally:
        if conn:
            close_db_connection(conn)

    # Display saved results from the database
    st.subheader("Analysis History")
    data = load_data()
    if data is not None:
        # 기본 데이터 표시
        with st.expander("View Raw Data"):
            st.dataframe(data)
        
        components = initialize_components()
        
        # 시계열 차트
        try:
            st.subheader("Analysis Trend")
            time_series_fig = components['visualizer'].create_time_series(data)
            st.plotly_chart(time_series_fig)
        except Exception as e:
            st.error(f"시계열 차트 생성 중 오류 발생: {e}")
        
        # 분포 차트
        try:
            st.subheader("Result Distribution")
            distribution_fig = components['visualizer'].create_distribution(data)
            st.plotly_chart(distribution_fig)
        except Exception as e:
            st.error(f"분포 차트 생성 중 오류 발생: {e}")
    else:
        st.info("No previous analysis data available.")

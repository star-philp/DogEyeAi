from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

def generate_pdf(pred_class, pred_idx, probs, severity_message, combined_image):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # PDF 제목
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Dog Eye Health Analysis Report")
    
    # 분석 결과
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Class: {pred_class}")
    c.drawString(100, 700, f"Index: {pred_idx}")
    c.drawString(100, 680, f"Probabilities: {probs}")
    c.drawString(100, 660, f"Severity Message: {severity_message}")
    
    # Recommended Actions
    c.drawString(100, 630, "Recommended Actions:")
    if "위급" in severity_message or "긴급" in severity_message:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.red)
        c.drawString(120, 610, "Immediate emergency care is required.")
    else:
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(120, 610, "Monitor the symptoms and consult a veterinarian if necessary.")
    /Users/rainstar/Project/Python/DogAI/analysis_report.pdf
    # 이미지 삽입
    image_path = "combined_image.png"
    combined_image.save(image_path)
    
    # Adjust image size and placement
    image_width = 4 * inch
    image_height = 4 * inch
    image_x = 100
    image_y = 400
    
    c.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)
    
    # Adding a line to separate image and text
    c.line(50, 580, 550, 580)  # Horizontal line just above the image
    
    # 페이지 넘김
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

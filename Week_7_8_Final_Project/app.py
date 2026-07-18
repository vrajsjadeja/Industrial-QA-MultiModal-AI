import streamlit as st
from PIL import Image
from ultralytics import YOLO
import ollama
import datetime
import os

st.set_page_config(page_title="Industrial QA System", layout="wide")
st.title("🏭 AI-Powered Industrial Quality Assurance")
st.write("Upload a steel surface image to detect defects and generate an AI maintenance report.")


model_path = "best.pt"
if os.path.exists(model_path):
    model = YOLO(model_path)
else:
    st.error("⚠️ Error: 'best.pt' not found. Please place your trained YOLO weights in the same folder.")
    st.stop()


uploaded_file = st.file_uploader("Upload Steel Surface Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Uploaded Image")
        st.image(image, use_container_width=True)
        
    with st.spinner("Analyzing surface for defects..."):
       
        results = model.predict(image)
        result_img = results[0].plot() # Draws bounding boxes
        
        with col2:
            st.subheader("Defect Detection")
            st.image(result_img, use_container_width=True, channels="BGR")
            
        
        detected_classes = []
        names = model.names
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0]) * 100
            class_name = names[class_id].replace("_", " ").title()
            detected_classes.append(f"• {class_name} ({conf:.0f}%)")
            
   
    st.divider()
    st.subheader("📄 AI Inspection Report")
    
    if len(detected_classes) == 0:
        st.success("No defects detected. Surface quality is optimal.")
    else:
        defects_text = "\n".join(detected_classes)
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        
        
        prompt = f"""
        You are an expert industrial quality assurance AI. Based on the following detected defects, generate a professional inspection report matching this EXACT format. Do not add any conversational filler.

        Inspection Report

        Inspection Date: {current_date}

        Detected Defects:
        {defects_text}

        Summary:
        [Write a 2-3 sentence summary explaining the findings and potential impact on surface quality]

        Severity:
        [Classify as Low, Medium, or High based on the types of defects]

        Recommended Action:
        [Provide 3-4 bullet points of recommended actions for the floor manager]
        """
        
        with st.spinner("Generating professional report via local Llama 3.2..."):
            try:
               
                response = ollama.generate(
                    model='llama3.2', 
                    prompt=prompt
                )
                
               
                st.markdown(response['response'])
                
            except Exception as e:
                st.error(f"Failed to connect to Ollama. Is the Ollama app running in the background? Error: {e}")
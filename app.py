import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Chef Global", page_icon="🍳", layout="centered")

API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Anahtarı bulunamadı! Secrets ayarlarını kontrol edin.")
    st.stop()

client = genai.Client(api_key=API_KEY)

GLOBAL_PROMPT = """
Analyze the ingredients in this refrigerator photo.
1. List the identified ingredients.
2. Provide 3 creative recipes (Breakfast, Lunch, Dinner).
3. Respond in the same language as the user's request.
4. Format with emojis and bold text.
"""

st.title("👨‍🍳 Global AI Chef v3")
st.write("Fotoğraf yükle, yeni nesil Gemini 3 ile tarifleri al!")

uploaded_file = st.file_uploader("Bir fotoğraf seç...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button('Tarifleri Oluştur'):
        with st.spinner('Şef Gemini 3 ile analiz ediyor...'):
            try:
                # Model ismini gemini-3-flash olarak güncelledik
                response = client.models.generate_content(
                    model="gemini-3-flash", 
                    contents=[GLOBAL_PROMPT, image]
                )
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")

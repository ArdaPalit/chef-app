import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Chef Global v3", page_icon="🍳", layout="centered")

API_KEY = st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

client = genai.Client(api_key=API_KEY)


AVAILABLE_MODEL = "gemini-1.5-flash" 

GLOBAL_PROMPT = """
Analyze the ingredients in this refrigerator photo.
1. List the identified ingredients.
2. Provide 3 creative recipes (Breakfast, Lunch, Dinner).
3. Respond in the same language as the user's request.
4. Format with emojis and bold text.
"""

st.title("👨‍🍳 Global AI Chef")
st.write("Yeni API anahtarınızla güvenli modda çalışıyor.")

uploaded_file = st.file_uploader("Bir fotoğraf seç...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button('Tarifleri Oluştur'):
        with st.spinner('Şef analiz ediyor...'):
            try:
                response = client.models.generate_content(
                    model=AVAILABLE_MODEL, 
                    contents=[GLOBAL_PROMPT, image]
                )
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Hata: {e}")
                st.info("İpucu: Eğer 404 hatası alıyorsanız, kodun içindeki AVAILABLE_MODEL ismini 'gemini-1.5-flash' olarak değiştirmeyi deneyin.")

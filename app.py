import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Chef Global", page_icon="🍳", layout="centered")

# Secrets kontrolü
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit Cloud 'Secrets' ayarlarını kontrol edin.")
    st.stop()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Client başlatılamadı: {e}")
    st.stop()

GLOBAL_PROMPT = """
Analyze the ingredients in this refrigerator photo.
1. List the identified ingredients.
2. Provide 3 creative recipes (Breakfast, Lunch, Dinner).
3. Detect the language of the user's request and respond in that same language.
4. Format the output nicely with emojis and bold text.
"""

st.title("👨‍🍳 Global AI Chef")
st.write("Fotoğraf yükle, kendi dilinde tarifleri al!")

uploaded_file = st.file_uploader("Bir fotoğraf seç...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button('Tarifleri Oluştur'):
        with st.spinner('Şef düşünüyor...'):
            try:
                # Model ismini 'gemini-1.5-flash' olarak teyit ediyoruz
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=[GLOBAL_PROMPT, image]
                )
                if response.text:
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.warning("Yapay zeka bir yanıt üretemedi. Lütfen farklı bir fotoğraf deneyin.")
            except Exception as e:
                st.error(f"Hata detayı: {e}")
                # Hata 404 devam ederse, alternatif olarak 'gemini-1.5-pro' denenebilir.

import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Chef Global", page_icon="🍳", layout="centered")

API_KEY = st.secrets.get("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=API_KEY)
except:
    st.error("API Anahtarı bulunamadı!")

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
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[GLOBAL_PROMPT, image]
                )
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Hata: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Uygulama yayında!")

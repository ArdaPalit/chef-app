import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- KONFİGÜRASYON ---
st.set_page_config(page_title="Dolapta Ne Var?", page_icon="🍳")

# API Anahtarınızı buraya tırnak içine yazın veya Environment Variable kullanın
os.environ["GOOGLE_API_KEY"] = "BURAYA_API_KEYINIZI_YAZIN"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- ARAYÜZ ---
st.title("🍳 Dolapta Ne Var?")
st.subheader("Fotoğrafı yükleyin, yapay zeka şefimiz tarifleri hazırlasın.")

uploaded_file = st.sidebar.file_uploader("Buzdolabının içini gösteren bir foto seç...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Mevcut Malzemeler', use_container_width=True)
    
    submit = st.button("Şef, Ne Pişirebilirim?")

    if submit:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Daha profesyonel sonuçlar için Prompt Mühendisliği
        input_prompt = """
        Sen yaratıcı ve profesyonel bir şefsin. Sana gönderilen buzdolabı fotoğrafındaki malzemeleri analiz et:
        1. Önce gördüğün tüm malzemeleri liste halinda yaz.
        2. Bu malzemelerle yapılabilecek 3 farklı yemek önerisi sun (Öğle yemeği, Akşam yemeği ve Atıştırmalık şeklinde).
        3. Her tarif için: Hazırlanış süresini, zorluk derecesini ve adım adım tarifi belirt.
        4. Evde bulunabilecek temel malzemeleri (tuz, karabiber, yağ, su) kullanabilirsin.
        Dilin samimi ve iştah açıcı olsun.
        """
        
        with st.spinner('Şef malzemeleri inceliyor ve tarifleri oluşturuyor...'):
            try:
                response = model.generate_content([input_prompt, image])
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
else:
    st.info("Lütfen sol taraftaki menüden bir buzdolabı fotoğrafı yükleyerek başlayın.")
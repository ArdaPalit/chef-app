import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Global AI Chef v3", page_icon="🍳", layout="centered")

API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit Cloud Secrets ayarlarını yapın.")
    st.stop()

client = genai.Client(api_key=API_KEY)

PREFERRED_MODEL = "gemini-3-flash-preview" 

GLOBAL_PROMPT = """
Sen profesyonel bir şefsin. Bu buzdolabı fotoğrafındaki malzemeleri analiz et:
1. Gördüğün tüm malzemeleri liste halinde yaz.
2. Bu malzemelerle yapılabilecek 3 farklı yaratıcı tarif sun (Kahvaltı, Öğle, Akşam).
3. Kullanıcının dilini tespit et ve yanıtı o dilde ver.
4. Çıktıyı emojiler ve kalın metinlerle görselleştir.
"""

st.title("👨‍🍳 Global AI Chef v3")
st.write("Fotoğraf yükle, yeni nesil Gemini 3 ile tarifleri al!")

with st.sidebar:
    st.header("Sistem Bilgisi")
    if st.checkbox("Desteklenen Modelleri Göster"):
        try:
            models = client.models.list()
            supported = [m.name.replace("models/", "") for m in models if "generateContent" in m.supported_methods]
            st.write(supported)
        except Exception as e:
            st.error(f"Liste alınamadı: {e}")

uploaded_file = st.file_uploader("Bir fotoğraf seç...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button('Tarifleri Oluştur'):
        with st.spinner('Şef malzemeleri inceliyor...'):
            try:
                response = client.models.generate_content(
                    model=PREFERRED_MODEL, 
                    contents=[GLOBAL_PROMPT, image]
                )
                if response.text:
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.warning("Görüntü analiz edilemedi. Lütfen daha net bir fotoğraf deneyin.")
            except Exception as e:
                st.error(f"Hata Oluştu: {e}")
                st.info(f"İpucu: Eğer 404 alıyorsanız, yan menüden model ismini kontrol edip kodu güncelleyin.")

st.sidebar.markdown("---")
st.sidebar.info("Güvenli Mod: API Anahtarı gizli tutuluyor.")

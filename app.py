import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageEnhance
import io
import base64

st.title("Editor de Imagens com Streamlit")

def exibir_imagem_html(img_np): ## função necessário para extrapolar o frame do streamlit
    # Converte a imagem para base64
    img_pil = Image.fromarray(img_np)
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    base64_img = base64.b64encode(byte_im).decode()

    # HTML para exibir imagem no tamanho original
    html = f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{base64_img}" style="max-width: none;" />
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Função para capturar imagem da webcam
def capturar_webcam():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, caption="Imagem capturada", use_container_width=True)
        return frame_rgb
    else:
        st.error("Erro ao acessar a webcam.")
        return None

## Transformações
# Escala
def aplicar_escala(img, escala):
    return cv2.resize(img, None, fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)
# Rotação
def aplicar_rotacao(img, angulo):
    centro = (img.shape[1] // 2, img.shape[0] // 2)
    matriz_rot = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    return cv2.warpAffine(img, matriz_rot, (img.shape[1], img.shape[0]))
#Cisalhamento
def aplicar_cisalhamento(img, h, v):
    matriz = np.float32([[1, h, 0], [v, 1, 0]])
    return cv2.warpAffine(img, matriz, (img.shape[1], img.shape[0]))
#Brilho e contraste
def ajustar_brilho_contraste(img, brilho, contraste):
    imagem_pil = Image.fromarray(img)
    imagem_pil = ImageEnhance.Brightness(imagem_pil).enhance(brilho)
    imagem_pil = ImageEnhance.Contrast(imagem_pil).enhance(contraste)
    return np.array(imagem_pil)
#Intensidade Logaritmica e Gama
def aplicar_transformacao_intensidade(img, tipo, gama=1.0):
    if tipo == "Logarítmica":
        img = np.log1p(img.astype(np.float32))
        img = np.clip((img / np.max(img)) * 255, 0, 255).astype(np.uint8)
    elif tipo == "Gama":
        img = np.power(img / 255.0, gama)
        img = np.clip(img * 255, 0, 255).astype(np.uint8)
    return img
# Efeito negativo
def aplicar_negativo(img):
    return 255 - img

## Parte principal do programa
# Upload ou captura
imagem = None
opcao = st.radio("Escolha a origem da imagem:", ("Upload", "Webcam"))

if opcao == "Upload":
    arquivo = st.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])
    if arquivo:
        imagem = Image.open(arquivo).convert("RGB")
elif opcao == "Webcam":
    if st.button("Capturar da Webcam"):
        img_array = capturar_webcam()
        if img_array is not None:
            st.session_state.imagem = Image.fromarray(img_array)

    if 'imagem' in st.session_state:
        imagem = st.session_state.imagem

if imagem:
    st.subheader("Imagem Original")
    st.image(imagem, use_container_width=True)

    # Ajustes
    st.sidebar.header("Ajustes Geométricos")
    rotacao = st.sidebar.slider("Rotação (graus)", -180, 180, 0)
    escala = st.sidebar.slider("Escala", 0.1, 3.0, 1.0)
    cisalhamento_h = st.sidebar.slider("Cisalhamento Horizontal", -1.0, 1.0, 0.0)
    cisalhamento_v = st.sidebar.slider("Cisalhamento Vertical", -1.0, 1.0, 0.0)

    st.sidebar.header("Ajustes de Intensidade")
    brilho = st.sidebar.slider("Brilho", 0.1, 3.0, 1.0)
    contraste = st.sidebar.slider("Contraste", 0.1, 3.0, 1.0)
    tipo_transformacao = st.sidebar.selectbox("Transformação de Intensidade", ["Nenhuma", "Logarítmica", "Gama"])
    gama = st.sidebar.slider("Valor de Gama", 0.1, 5.0, 1.0) if tipo_transformacao == "Gama" else 1.0

    negativo = st.sidebar.checkbox("Aplicar Filtro Negativo")

    # Aplicar transformações
    img_np = np.array(imagem)
    img_np = aplicar_escala(img_np, escala)
    img_np = aplicar_rotacao(img_np, rotacao)
    img_np = aplicar_cisalhamento(img_np, cisalhamento_h, cisalhamento_v)
    img_np = ajustar_brilho_contraste(img_np, brilho, contraste)
    img_np = aplicar_transformacao_intensidade(img_np, tipo_transformacao, gama)
    if negativo:
        img_np = aplicar_negativo(img_np)

    st.subheader("Imagem Editada")
    exibir_imagem_html(img_np)


    # Download
    img_editada = Image.fromarray(img_np)
    buf = io.BytesIO()
    img_editada.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("Baixar imagem editada", data=byte_im, file_name="imagem_editada.png", mime="image/png")

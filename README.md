# Editor de Imagens com Streamlit
O aplicativo permite ao usuário carregar uma imagem ou capturá-la diretamente da webcam, aplicar diversas transformações geométricas e ajustes de intensidade, visualizar o resultado e fazer o download da imagem editada.

### Funcionalidades desenvolvidas:
- Upload ou captura via webcam

- Transformações geométricas:
    - Escala
    - Rotação
    - Cisalhamento horizontal e vertical

- Ajustes de intensidade:
    - Brilho
    - Contraste

- Transformações logarítmica e gama
- Filtro negativo
- Visualização da imagem original e editada
- Download da imagem editada

### Tecnologias utilizadas
- Python
- Streamlit
- OpenCV
- PIL (Pillow)
- NumPy

### Como rodar localmente
Pré-requisitos
Python 3.8 ou superior
Pip (gerenciador de pacotes)

#### Passos
- Crie e ative um ambiente virtual (opcional, mas recomendado):
- Instale as dependências que estão no arquivo requirements.txt
- Execute o aplicativo pelo terminal:
    streamlit run app.py
- Acesse no navegador:
    O Streamlit abrirá automaticamente o navegador. Caso não abra, acesse manualmente:
        http://localhost:8501

Nessa etapa, você já conseguirá utilizar o aplicativo desenvolvido.

### Estrutura do projeto
atividade2/
├── app.py               # Código principal do aplicativo
├── README.md            # Este arquivo
└── requirements.txt     # Lista de dependências
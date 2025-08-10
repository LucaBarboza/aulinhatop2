import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🗺️ Input em Formato de Mapa")
st.markdown("Clique em um local no mapa para obter suas coordenadas de latitude e longitude.")

# --- DADOS INICIAIS DO MAPA ---
# Usando coordenadas centradas no Brasil
initial_location = [-14.2350, -51.9253]
initial_zoom = 4

# --- CRIAÇÃO DO MAPA ---
# 1. Criar um objeto de mapa Folium
m = folium.Map(location=initial_location, zoom_start=initial_zoom)

# Adicionar um marcador no centro (opcional)
folium.Marker(
    initial_location,
    popup="Centro do Brasil",
    tooltip="Clique aqui!"
).add_to(m)


# --- RENDERIZAÇÃO E CAPTURA DO INPUT ---
# 2. Renderizar o mapa no Streamlit e capturar o output
# A função st_folium retorna um dicionário com os dados da interação do usuário
output = st_folium(m, width=1200, height=600)

st.divider()

# --- EXIBIÇÃO DOS DADOS CAPTURADOS ---
st.header("Dados Retornados pelo Mapa:")

# O dicionário 'output' contém várias informações úteis
st.write("Dicionário completo retornado:")
st.write(output)

# Extraindo e mostrando a informação mais comum: o último clique
st.subheader("📍 Último Ponto Clicado")
if output.get("last_clicked"):
    lat = output["last_clicked"]["lat"]
    lng = output["last_clicked"]["lng"]
    
    st.write(f"**Latitude:** `{lat}`")
    st.write(f"**Longitude:** `{lng}`")
    
    # Você pode usar essas variáveis para qualquer outra lógica no seu app
    # Por exemplo, buscar a previsão do tempo para essa coordenada.
    if st.button("Buscar informações para esta coordenada"):
        st.info(f"Buscando dados para Lat: {lat}, Lon: {lng}...")
else:
    st.info("Nenhum ponto foi clicado no mapa ainda.")

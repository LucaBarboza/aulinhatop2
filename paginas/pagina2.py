import streamlit as st
import folium
import requests
import json
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🗺️ Seletor de Países Interativo")
st.markdown("Passe o mouse sobre um país para ver o nome e clique para selecioná-lo.")

# --- 1. CARREGAR OS DADOS GEOGRÁFICOS DOS PAÍSES ---
# URL para um arquivo GeoJSON com os polígonos dos países.
# Este arquivo é a "mágica" que nos permite desenhar e interagir com os países.
url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json"

# Faz o download dos dados e carrega como um dicionário Python
try:
    response = requests.get(url)
    response.raise_for_status()  # Lança um erro se a requisição falhar
    geo_data = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Erro ao baixar os dados geográficos: {e}")
    st.stop()
except json.JSONDecodeError:
    st.error("Erro ao decodificar os dados geográficos. O arquivo pode estar corrompido.")
    st.stop()


# --- 2. CRIAR O MAPA COM UM TEMA MAIS BONITO ---
# Usamos o "tile" (fundo do mapa) 'CartoDB positron', que é limpo e minimalista.
# Outras opções: 'CartoDB dark_matter' (escuro), 'Stamen Toner' (preto e branco).
m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')


# --- 3. ADICIONAR A CAMADA DE PAÍSES INTERATIVOS (GeoJson) ---

# Criamos a camada GeoJson, que é o coração da interatividade
geojson_layer = folium.GeoJson(
    geo_data,
    # Estilo padrão dos países
    style_function=lambda feature: {
        'fillColor': '#D3D3D3', # Cinza claro
        'color': 'black',      # Cor da borda
        'weight': 1,           # Espessura da borda
        'fillOpacity': 0.7,
    },
    # Estilo quando o mouse passa por cima (efeito "botão")
    highlight_function=lambda feature: {
        'fillColor': '#FFFF00', # Amarelo
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.9,
    },
    # Adiciona um tooltip que mostra o nome do país ao passar o mouse
    tooltip=folium.GeoJsonTooltip(
        fields=['name'],
        aliases=['País:'],
        localize=True,
        sticky=False
    )
).add_to(m)


# --- 4. RENDERIZAR O MAPA E CAPTURAR O CLIQUE ---

st.write("### Mapa Interativo")
output = st_folium(m, width=1200, height=600, returned_objects=['last_object_clicked'])

st.divider()

# --- 5. EXIBIR O PAÍS SELECIONADO ---
st.header("País Selecionado:")

# Acessa o dicionário de forma segura usando .get()
clicked_info = output.get("last_object_clicked")

# Verifica se 'clicked_info' não é nulo e se a chave 'id' existe dentro dele
if clicked_info and clicked_info.get("id"):
    clicked_country_id = clicked_info["id"]

    # Encontrar o nome do país no nosso 'geo_data' usando o ID
    country_name = "Não encontrado"
    for feature in geo_data["features"]:
        if feature["id"] == clicked_country_id:
            country_name = feature["properties"]["name"]
            break

    st.success(f"Você selecionou: **{country_name}** (ID: {clicked_country_id})")

    if st.button(f"Gerar roteiro para {country_name}"):
        st.info("Aqui você colocaria a lógica para gerar o roteiro...")
else:
    st.info("Nenhum país foi selecionado ainda.")

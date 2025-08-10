import streamlit as st
import folium
import requests
import json
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🌎 Roteiros de Viagem IA")
st.markdown("Selecione um país no mapa para começar a planejar sua próxima aventura.")

# --- 1. INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
# Este é o "cérebro" do nosso app. Ele vai lembrar:
# - Qual país está selecionado.
# - As coordenadas para dar zoom no país (bounds).
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
if "map_bounds" not in st.session_state:
    st.session_state.map_bounds = None
if "geo_data" not in st.session_state:
    try:
        url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json"
        response = requests.get(url)
        response.raise_for_status()
        st.session_state.geo_data = response.json()
    except Exception as e:
        st.error(f"Não foi possível carregar os dados do mapa. Tente recarregar a página. Erro: {e}")
        st.stop()

geo_data = st.session_state.geo_data

# --- 2. LAYOUT COM COLUNAS ---
# Dividimos a tela: 3/4 para o mapa, 1/4 para as informações.
map_col, info_col = st.columns([3, 1])

# --- 3. LÓGICA DE ESTILO E INTERAÇÃO ---
def get_style(feature):
    """Define o estilo de cada país no mapa."""
    if st.session_state.selected_country == feature["id"]:
        # Estilo para o país selecionado
        return {
            'fillColor': '#007BFF',  # Azul vibrante
            'color': '#FFFFFF',      # Borda branca
            'weight': 2,
            'fillOpacity': 0.8,
        }
    else:
        # Estilo padrão para os outros países
        return {
            'fillColor': '#D3D3D3',
            'color': '#333333',
            'weight': 1,
            'fillOpacity': 0.7,
        }

def get_highlight_style(feature):
    """Define o estilo ao passar o mouse (hover)."""
    # Não vamos destacar o país que já está selecionado
    if st.session_state.selected_country == feature["id"]:
        return get_style(feature)
    return {
        'fillColor': '#FFC107',  # Amarelo/Laranja
        'color': '#333333',
        'weight': 2,
        'fillOpacity': 0.9,
    }

# --- 4. CRIAÇÃO E EXIBIÇÃO DO MAPA ---
with map_col:
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

    # Se tivermos um 'bound' (zoom) salvo, aplicamos ao mapa
    if st.session_state.map_bounds:
        m.fit_bounds(st.session_state.map_bounds)

    geojson_layer = folium.GeoJson(
        geo_data,
        style_function=get_style,
        highlight_function=get_highlight_style,
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['País:']),
    ).add_to(m)

    output = st_folium(m, key="mapa_interativo", width=1100, height=600, returned_objects=['last_object_clicked'])

# --- 5. PROCESSAMENTO DO CLIQUE E ATUALIZAÇÃO DO ESTADO ---
# Este bloco executa quando o usuário clica em um país
if output and output.get("last_object_clicked"):
    clicked_id = output["last_object_clicked"]["id"]
    
    # Se clicou num país novo, atualizamos o estado
    if st.session_state.selected_country != clicked_id:
        st.session_state.selected_country = clicked_id
        
        # Encontra o polígono do país clicado para calcular o zoom (bounds)
        for feature in geo_data["features"]:
            if feature["id"] == clicked_id:
                # Criamos uma camada temporária só com esse país para pegar seus limites
                temp_layer = folium.GeoJson(feature)
                st.session_state.map_bounds = temp_layer.get_bounds()
                break
        
        # st.rerun() é a chave para a mágica! Ele recarrega o script
        # com os novos valores no st.session_state, redesenhando o mapa.
        st.rerun()

# --- 6. EXIBIÇÃO DAS INFORMAÇÕES E AÇÕES NA COLUNA LATERAL ---
with info_col:
    st.header("Informações")
    if st.session_state.selected_country:
        country_name = "N/A"
        for feature in geo_data["features"]:
            if feature["id"] == st.session_state.selected_country:
                country_name = feature["properties"]["name"]
                break
        
        st.success(f"País selecionado: **{country_name}**")
        st.markdown("O que você deseja fazer?")
        
        if st.button(f"✈️ Gerar roteiro para {country_name}", use_container_width=True):
            st.info(f"Gerando um roteiro incrível para sua viagem à {country_name}...")
            # Aqui entraria a chamada para a sua IA

        if st.button("🗑️ Limpar seleção", use_container_width=True):
            # Lógica para limpar o estado e resetar o mapa
            st.session_state.selected_country = None
            st.session_state.map_bounds = None
            st.rerun()
    else:
        st.info("Nenhum país selecionado. Clique em um local no mapa.")

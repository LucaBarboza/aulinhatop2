import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.title("Exemplos CRUD - Firebase")

# Conectar Firebase
@st.cache_resource
def conectar_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = conectar_firebase()
colecao = 'usuarios2'

# CREATE - Criar documento
st.header("CREATE")
nome = st.text_input("Nome")
if st.button("Criar"):
    # Usa email do usuário como ID
    db.collection(colecao).add({'nome': nome})
    st.write(f"Criado com ID: {st.user.email}")

st.info(f"O ID do documento é o próprio email do usuário logado na coleção '{colecao}'")

# READ - Ler documentos  
st.header("READ")
if st.button("Listar todos"):
    docs = db.collection(colecao).stream()
    for doc in docs:
        st.write(f"{doc.id}: {doc.to_dict()}")

# UPDATE - Atualizar documento
st.header("UPDATE")
doc_id = st.text_input("ID do documento")
novo_nome = st.text_input("Novo nome")
if st.button("Atualizar"):
    db.collection(colecao).document(doc_id).update({'nome': novo_nome})
    st.write("Atualizado!")

# DELETE - Deletar documento
st.header("DELETE")  
id_deletar = st.text_input("ID para deletar")
if st.button("Deletar"):
    db.collection(colecao).document(id_deletar).delete()
    st.write("Deletado!")

st.header("📚 Outros métodos úteis do Firebase")

# CONTADOR - Sistema simples de contagem
st.subheader("🔢 Contador Pessoal")
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Incrementar"):
        user_ref = db.collection(colecao).document(st.user.email)
        doc = user_ref.get()
        dados = doc.to_dict() if doc.exists else {}
        contador_atual = dados.get('contador', 0)
        dados['contador'] = contador_atual + 1
        user_ref.set(dados)
        st.rerun()

with col2:
    if st.button("🔍 Ver contador"):
        doc = db.collection(colecao).document(st.user.email).get()
        dados = doc.to_dict() if doc.exists else {}
        total = dados.get('contador', 0)
        st.metric("Seu contador", total)

# NOTAS - Sistema de anotações
st.subheader("📝 Notas Rápidas")
nova_nota = st.text_input("Nova nota")
if st.button("💾 Salvar nota"):
    from datetime import datetime
    user_ref = db.collection(colecao).document(st.user.email)
    doc = user_ref.get()
    dados = doc.to_dict() if doc.exists else {}
    
    if 'notas' not in dados:
        dados['notas'] = []
    
    dados['notas'].append({
        'texto': nova_nota,
        'horario': datetime.now().strftime('%d/%m %H:%M')
    })
    user_ref.set(dados)
    st.success("Nota salva!")

if st.button("📋 Ver minhas notas"):
    doc = db.collection(colecao).document(st.user.email).get()
    dados = doc.to_dict() if doc.exists else {}
    notas = dados.get('notas', [])
    
    if notas:
        for nota in notas:  
            st.write(f"📝 {nota['horario']}: {nota['texto']}")
    else:
        st.info("Nenhuma nota ainda")

# ESTATÍSTICAS - Análise simples
st.subheader("📊 Estatísticas")
if st.button("Total de usuários"):
    docs = list(db.collection(colecao).stream())
    st.metric("Total de usuários", len(docs))

import streamlit as st

st.set_page_config(
    page_title="FriKI — Fritz Compliance Scanner",
    page_icon="🇩🇪",
    layout="centered"
)

st.title("🇩🇪 FriKI — Fritz Compliance Scanner")
st.subheader("Die KI für den deutschen Mittelstand")

st.info("MVP v0.1 | Upload → Analyse → Report")

uploaded_file = st.file_uploader(
    "Dokument hochladen (PDF oder DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file is not None:
    st.success(f"Dokument '{uploaded_file.name}' erfolgreich hochgeladen!")
    st.write("Analyse-Engine wird initialisiert...")
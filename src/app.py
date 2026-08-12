import streamlit as st
from io import BytesIO

# --- CONFIG ---
st.set_page_config(
    page_title="FKI — Fritz Compliance Scanner",
    page_icon="🇩🇪",
    layout="centered"
)

# --- HEADER ---
st.title("🇩🇪 FKI — Fritz Compliance Scanner")
st.subheader("Die KI für den deutschen Mittelstand")
st.caption("MVP v0.1 | Upload → Extraktion → Vorschau")

st.divider()

# --- UPLOAD ---
uploaded_file = st.file_uploader(
    "📄 Dokument hochladen (PDF oder DOCX)",
    type=["pdf", "docx"],
    help="Lade einen Vertrag, eine DSGVO-Erklärung oder ein anderes Dokument hoch."
)

# --- EXTRACTION LOGIC ---
def extract_text_pdf(file_bytes):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return f"[FEHLER PDF] {str(e)}"

def extract_text_docx(file_bytes):
    try:
        import docx
        doc = docx.Document(BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"[FEHLER DOCX] {str(e)}"

# --- MAIN FLOW ---
if uploaded_file is not None:
    st.success(f"✅ '{uploaded_file.name}' erfolgreich hochgeladen!")
    
    # Lire les bytes
    file_bytes = uploaded_file.getvalue()
    
    # Détecter le type et extraire
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    with st.spinner("Fritz analysiert das Dokument..."):
        if file_type == "pdf":
            extracted_text = extract_text_pdf(file_bytes)
        elif file_type == "docx":
            extracted_text = extract_text_docx(file_bytes)
        else:
            extracted_text = "[FEHLER] Nicht unterstütztes Dateiformat."
    
    # Afficher les métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dateityp", file_type.upper())
    with col2:
        word_count = len(extracted_text.split())
        st.metric("Wörter", word_count)
    with col3:
        char_count = len(extracted_text)
        st.metric("Zeichen", char_count)
    
    st.divider()
    
    # Afficher le texte extrait
    st.subheader("📋 Extrahierter Text")
    
    if extracted_text.startswith("[FEHLER"):
        st.error(extracted_text)
    else:
        with st.expander("Vollständigen Text anzeigen", expanded=False):
            st.text_area("Text", extracted_text, height=300)
        
        st.info("🔜 Nächster Schritt: Compliance-Analyse (v0.2)")
    
    st.divider()
    st.caption("Made with ❤️ in Germany | FKI © 2026")

else:
    st.info("👆 Lade ein Dokument hoch, um zu starten.")
    
    # Zone d'aide
    with st.expander("🧠 Was kann Fritz aktuell?"):
        st.write("""
        - PDF-Dateien lesen und Text extrahieren
        - DOCX-Dateien lesen und Text extrahieren
        - Wort- und Zeichenzählung anzeigen
        
        **Kommt in v0.2:** DSGVO-Check, Vertragsrisiken, Compliance-Score
        """)
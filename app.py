import streamlit as st
import tempfile
import os
import re

from export_chat import export_single_as_docx, export_all_as_docx
from source_reference import get_source_pages
from document_loader import load_document
from text_splitter import split_documents
from vector_store import create_vector_store
from rag_pipeline import create_llm, generate_answer

st.set_page_config(page_title="DocuMind", page_icon="🧠", layout="wide")

# --- Session State Init ---
if "sessions" not in st.session_state:
    st.session_state["sessions"] = []
if "active_index" not in st.session_state:
    st.session_state["active_index"] = None
if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None
if "llm" not in st.session_state:
    st.session_state["llm"] = None
if "file_name" not in st.session_state:
    st.session_state["file_name"] = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🧠 DocuMind")
    st.markdown("---")
    st.markdown("### 🗂️ History")

    if st.session_state["sessions"]:
        for i, session in enumerate(st.session_state["sessions"]):
            label = session["title"][:30] + "..." if len(session["title"]) > 30 else session["title"]
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(f"💬 {label}", key=f"session_{i}", use_container_width=True):
                    st.session_state["active_index"] = i
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state["sessions"].pop(i)
                    if st.session_state["active_index"] == i:
                        st.session_state["active_index"] = None
                    elif (
                        st.session_state["active_index"] is not None
                        and st.session_state["active_index"] > i
                    ):
                        st.session_state["active_index"] -= 1
                    st.rerun()
    else:
        st.caption("No history yet. Upload a PDF and start asking!")


# --- Reusable Export UI Block ---
def show_export_ui(active):
    st.divider()
    scope = st.radio("Export scope:", ["This chat", "Entire history"], horizontal=True)

    if scope == "This chat":
        data = export_single_as_docx(active)
        fname = f"{active['title'][:30]}.docx"
    else:
        data = export_all_as_docx(st.session_state["sessions"])
        fname = "documind_full_history.docx"

    mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back to chat"):
            st.session_state["active_index"] = None
            st.rerun()
    with col2:
        st.download_button(
            label="📥 Export as DOCX",
            data=data,
            file_name=fname,
            mime=mime
        )


# --- Main Area ---
st.title("🧠 DocuMind")
st.write("RAG-Powered Document Question Answering")
st.divider()

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx"])

if uploaded_file:
    if st.session_state["file_name"] != uploaded_file.name:
        file_ext = "." + uploaded_file.name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        with st.spinner("Processing document... please wait"):
            file_type = uploaded_file.name.split(".")[-1].lower()
            documents = load_document(tmp_path, file_type)
            chunks = split_documents(documents)
            st.session_state["vector_store"] = create_vector_store(chunks)
            st.session_state["llm"] = create_llm()
            st.session_state["file_name"] = uploaded_file.name

        os.unlink(tmp_path)
        st.success(f"✅ {uploaded_file.name} is ready!")

    if st.session_state["active_index"] is not None:
        active = st.session_state["sessions"][st.session_state["active_index"]]
        st.markdown(f"### 💬 {active['title']}")
        st.divider()
        for msg in active["history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        show_export_ui(active)

    else:
        question = st.text_input("💬 Ask a question about your document:")

        if question:
            with st.spinner("Thinking..."):
                docs = st.session_state["vector_store"].similarity_search(question, k=3)
                answer = generate_answer(st.session_state["llm"], question, docs)

            answer = re.sub(r'\[\s*(.*?)\s*\]', r'$$\1$$', answer, flags=re.DOTALL)
            answer = re.sub(r'\\\((.*?)\\\)', r'$\1$', answer, flags=re.DOTALL)

            st.session_state["sessions"].append({
                "title": question,
                "history": [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer}
                ]
            })

            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                st.markdown(answer)
                pages = get_source_pages(docs)
                if pages:
                    st.caption(f"📄 Source pages: {', '.join(str(p) for p in pages)}")

else:
    if st.session_state["active_index"] is not None:
        active = st.session_state["sessions"][st.session_state["active_index"]]
        st.markdown(f"### 💬 {active['title']}")
        st.divider()
        for msg in active["history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        show_export_ui(active)
    else:
        st.info("Upload a PDF and ask questions about its contents.")
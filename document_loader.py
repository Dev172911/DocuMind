from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


def load_docx(file_path):
    loader = Docx2txtLoader(file_path)
    return loader.load()


def load_document(file_path, file_type):
    if file_type == "pdf":
        return load_pdf(file_path)
    elif file_type == "docx":
        return load_docx(file_path)
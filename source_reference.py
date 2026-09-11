def get_source_pages(docs):
    pages = []
    for doc in docs:
        page = doc.metadata.get("page", None)
        if page is not None and page + 1 not in pages:
            pages.append(page + 1)  # PyPDFLoader is 0-indexed, so +1
    pages.sort()
    return pages
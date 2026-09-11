from vector_store import load_vector_store

vector_store = load_vector_store()

question = "What is Coulomb's law?"

results = vector_store.similarity_search(question, k=3)

print(f"Retrieved {len(results)} relevant chunks")

print("\nFirst result:")
print(results[0].page_content[:500])
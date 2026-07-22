from src.vectorstore import FaissVectorStore

store = FaissVectorStore("faiss_store")
store.load()

print("Vectors:", store.index.ntotal)
print("Metadata:", len(store.metadata))
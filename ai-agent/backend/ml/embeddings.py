class TextEmbeddings:
    """
    Wrapper for generating embeddings to use in vector similarity search (e.g. for duplicates).
    """
    def __init__(self):
        # Could use sentence-transformers or OpenAI embeddings
        pass

    def get_embedding(self, text):
        # Return mock vector
        return [0.1] * 384

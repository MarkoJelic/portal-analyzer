"""Simple vector store placeholder."""

class VectorStore:
    def __init__(self):
        self.vectors = []

    def add(self, id, vector):
        self.vectors.append((id, vector))

import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model only once
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def generate_embedding(text: str) -> np.ndarray:
    """
    Generate an embedding vector for the given text.
    """

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding


def embedding_to_string(embedding: np.ndarray) -> str:
    """
    Convert embedding array to a JSON string
    for storing in SQLite.
    """

    return np.array2string(
        embedding,
        separator=","
    )


def string_to_embedding(text: str) -> np.ndarray:
    """
    Convert stored string back into
    a NumPy array.
    """

    text = text.replace("[", "")
    text = text.replace("]", "")

    return np.fromstring(
        text,
        sep=","
    )


if __name__ == "__main__":

    sentence = "Large pothole near the highway."

    vector = generate_embedding(sentence)

    print(vector.shape)

    print(vector[:10])

    string = embedding_to_string(vector)

    print(string[:100])

    restored = string_to_embedding(string)

    print(restored.shape)
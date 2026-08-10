from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "alibayram/embeddingmagibu-200m",
    trust_remote_code=True
)

sentences = [
    "Bugün hava çok güzel.",
    "Dışarısı güneşli.",
    "Uzun bağlam gerektiren çok detaylı bir hukuki veya teknik metin..."
]

embeddings = model.encode(sentences, normalize_embeddings=True)

print(embeddings.shape)
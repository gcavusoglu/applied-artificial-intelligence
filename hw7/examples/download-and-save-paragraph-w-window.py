import itertools

import psycopg2
from datasets import load_dataset
from huggingface_hub import login
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

model_name = "alibayram/embeddingmagibu-200m"
model = SentenceTransformer(
    model_name,
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# With an 8k context window, a larger chunk size like 2000 keeps deep semantic context intact.
MAX_CHUNK_TOKENS = 2000

def get_chunk_list(txt):
    paragraphs = [p.strip() for p in txt.split("\n") if p.strip()]
    print(paragraphs[0])

    text_ch = []
    current_chunk = []
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph_tokens = len(tokenizer.encode(paragraph, add_special_tokens=False))

        if paragraph_tokens > MAX_CHUNK_TOKENS:
            if current_chunk:
                text_ch.append("\n".join(current_chunk))
                current_chunk = []
                current_tokens = 0
            text_ch.append(paragraph)
            continue

        if current_tokens + paragraph_tokens > MAX_CHUNK_TOKENS:
            text_ch.append("\n".join(current_chunk))
            current_chunk = [paragraph]
            current_tokens = paragraph_tokens
        else:
            current_chunk.append(paragraph)
            current_tokens += paragraph_tokens

    # Add last paragraphs
    if current_chunk:
        text_ch.append("\n".join(current_chunk))
    return text_ch

# Get dataset
login(token="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")

streamed_dataset = load_dataset("umutertugrul/turkish-hospital-medical-articles", streaming=True)
raw_stream = next(iter(streamed_dataset.values()))
data_list = list(itertools.islice(raw_stream, 100))
print(f"Successfully retrieved {len(data_list)} rows without downloading the full dataset.")

if len(data_list) == 0:
    print("Error - No data received")
    exit(1)

with psycopg2.connect(dbname="pc", user="pc", password="", host="localhost", port="5432") as conn:
    register_vector(conn)
    cur = conn.cursor()
    insert_query = "INSERT INTO medical_data (url, chunk_text, chunk_vector) VALUES (%s, %s, %s);"

    for data in data_list:
        text = data['text']

        text_chunks = get_chunk_list(text)

        embedding_list = model.encode(text_chunks, normalize_embeddings=True)

        print(f"Generated {len(embedding_list)} embeddings.")
        print(f"Embedding shape: {embedding_list.shape}")

        for i in range(len(text_chunks)):
            cur.execute(insert_query, (data['url'], text_chunks[i], embedding_list[i]))

        conn.commit()

        # TODO
        break
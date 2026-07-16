from transformers import AutoTokenizer

# Download and load the pretrained tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Encode text
text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised thanks to these sheets and more recently with desktop publishing software like Aldus PageMaker and Microsoft Word including versions of Lorem Ipsum."
encoded_input = tokenizer(text)

# Get token ids
print("Token IDs:", encoded_input["input_ids"])

# Get tokens
tokens = tokenizer.tokenize(text)
print("Tokens:", tokens)

# Try to decode token IDs back to a human-readable string
decoded_text = tokenizer.decode(encoded_input["input_ids"])
print("Decoded Text:", decoded_text)
from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Modelin Hugging Face üzerindeki resmi tokenizer'ını yükleyin
tokenizer = AutoTokenizer.from_pretrained("magibu/embeddingmagibu-200m")

# 2. Splitter'ı bu tokenizer ile kurun
# Model 8192 token destekler, ancak RAG için ideal parça boyutu genelde 512-1024 arasındadır.
text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer=tokenizer,
    chunk_size=1024,      # Magibu token birimine göre maksimum parça büyüklüğü
    chunk_overlap=128,    # Parçalar arasındaki çakışma token miktarı
)

# 3. Metni Türkçe kurallarına (paragraf, cümle) dikkat ederek bölün
dokumanlar = text_splitter.split_text("Türkçe uzun doküman içeriğiniz buraya gelecek...")

print(dokumanlar)
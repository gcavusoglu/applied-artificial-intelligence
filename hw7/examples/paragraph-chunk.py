import nltk
from nltk.tokenize import blankline_tokenize
from sentence_transformers import SentenceTransformer

# NLTK fonksiyonu metni boş satırlara göre paragraflara ayırır
def chunk_text_by_paragraphs_nltk(text):
    # blankline_tokenize boşlukları ve satır atlamalarını temizler
    paragraphs = blankline_tokenize(text)
    # Başındaki ve sonundaki gereksiz boşlukları kırparak temiz listeyi döner
    return [p.strip() for p in paragraphs if p.strip()]

# Örnek uzun metin
document = """
Yapay zeka teknolojileri son yıllarda büyük bir ivme kazandı. Özellikle doğal dil işleme alanındaki gelişmeler, makinelerin insan dilini anlama yeteneğini benzersiz bir seviyeye taşıdı.
Gömme modelleri (Embedding), kelimeleri veya paragrafları yüksek boyutlu vektör uzaylarında temsil eder. Bu sayede kelimeler arasındaki anlamsal ilişkiler matematiksel olarak hesaplanabilir hale gelir.
magibu/embeddingmagibu-200m modeli, Türkçe dil yapısına ve morfolojisine optimize edilmiş güçlü bir açık kaynaklı gömme modelidir. Geniş bağlam penceresi sayesinde uzun metinlerde de yüksek başarı gösterir.
"""

# 1. NLTK ile paragraflara ayırma (Paragraph Chunking)
chunks = chunk_text_by_paragraphs_nltk(document)
print(f"NLTK ile oluşturulan paragraf sayısı: {len(chunks)}")

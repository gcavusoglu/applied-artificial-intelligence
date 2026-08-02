import pandas as pd
from datasets import Dataset
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
import time

#Anlamsal benzerlik kontrolü için modeli başlatıyoruz
anlamsal_benzerlik_modeli = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")


# Verilen cevabın doğru olup olmadığını kontrol eden fonksiyon
def cevap_dogru_mu(dogru_cevap_index, verilen_cevap, secenekler):
    # Seçenekler A, B, C, D, E şeklinde dizildiği için harfler listesini tanımlıyoruz
    harfler = ['A', 'B', 'C', 'D', 'E']

    # Doğru cevaba karşılık gelen harfi belirliyoruz
    dogru_harf = harfler[dogru_cevap_index]

    # Kullanıcının verdiği cevabı büyük harflere çeviriyoruz, çünkü karşılaştırmada harf duyarlılığı istemiyoruz
    verilen_cevap = verilen_cevap.upper()

    # Verilen cevabın başındaki ve sonundaki boşlukları temizliyoruz
    verilen_cevap = verilen_cevap.strip()

    # Eğer verilen cevap doğrudan doğru harfe eşitse doğru kabul ediyoruz
    if dogru_harf == verilen_cevap:
        return True
    # Eğer cevap birden fazla karakter içeriyor ve 2. karakter boşluk, noktalama gibi özel karakterse,
    # sadece ilk harfi kontrol ediyoruz
    elif len(verilen_cevap) > 1 and verilen_cevap[1] in [" ", ":", ")", "=", "-", "."]:
        return dogru_harf == verilen_cevap[0]
    else:
        # Anlamsal benzerlik modelini kullanarak verilen cevap ve seçenekleri vektörel olarak kodluyoruz
        encoded_cevap = anlamsal_benzerlik_modeli.encode([verilen_cevap])
        encoded_secenekler = anlamsal_benzerlik_modeli.encode(secenekler)

        # Kodlanan cevap ile seçenekler arasındaki benzerlik puanlarını hesaplıyoruz
        benzerlik_listesi = anlamsal_benzerlik_modeli.similarity(encoded_cevap, encoded_secenekler).tolist()[0]

        # Benzerlik puanlarının en yükseğini buluyoruz
        en_yuksek_benzerlik = max(benzerlik_listesi)

        # En yüksek benzerlik puanının hangi seçeneğe ait olduğunu buluyoruz
        en_yuksek_benzerlik_index = benzerlik_listesi.index(en_yuksek_benzerlik)

        # Eğer en yüksek benzerlik doğru cevabın indeksine eşitse, doğru cevabı bulmuşuz demektir
        return en_yuksek_benzerlik_index == dogru_cevap_index

# Verilerimizi okuyoruz
mmlu_veri = pd.read_parquet(
    "hf://datasets/gmz1234/ai-benchmark/data/data.parquet")
model_detayli_sonuclar = []
model_bolum_sonuclar = []

# İlerleme çubuğu fonksiyonu
def ilerleme_cubugu(guncel, toplam, cubuk_uzunlugu=40):
    ilerleme = guncel / toplam
    blok = int(cubuk_uzunlugu * ilerleme)
    cubuk = "#" * blok + "-" * (cubuk_uzunlugu - blok)
    return f"[{cubuk}] {ilerleme * 100:.2f}%"

# Model test fonksiyonu
def modeli_test_et():
    model_id = "gmz1234/qwen3-custom-lora"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    amodel = AutoModelForCausalLM.from_pretrained(
      model_id,
      torch_dtype="auto",
      device_map="auto"
    )

    model = {'model': amodel, 'model_id': model_id,'details': { 'format': 'gguf', 'family': 'qwen3', 'parameter_size': '4.0B', 'quantization_level': 'N/A'} }
    model_detayli_sonuc = {
        'model': model_id,
        'format': model['details']['format'],
        'family': model['details']['family'],
        'parameter_size': model['details']['parameter_size'],
        'quantization_level': model['details']['quantization_level']
    }

    model_bolum_sonuc = {'model': model_id}

    baslama_zamani = time.time()
    dogru_cevap_sayisi = 0

    # Soruları test etme ve cevap kontrolü
    print(len(mmlu_veri))
    for i in range(len(mmlu_veri)):
        soru = mmlu_veri.iloc[i]['soru']
        soru += "\n"
        harfler = ['A', 'B', 'C', 'D', 'E']
        for j in range(len(mmlu_veri.iloc[i]['secenekler'])):
            secenek = mmlu_veri.iloc[i]['secenekler'][j]
            soru += harfler[j] + ": " + secenek + "\n"

        prompt = "I'm giving you the question and the options. Just write which option is the correct answer. For example, 'A' or 'B'. Please don't give any explanations!\nQuestion: " + soru

        generator = pipeline(
            "text-generation",
            model=model['model'],
            tokenizer=tokenizer
        )
        outputs = generator(prompt, max_new_tokens=50, do_sample=True, temperature=0.7, return_full_text=False)
        print(outputs[0]["generated_text"])

        cevap = outputs[0]["generated_text"]
        # Cevabı veriye ekleme
        mmlu_veri.loc[i, model['model_id'] + '_cevap'] = cevap

        bolum = mmlu_veri.iloc[i]['bolum']

        if bolum not in model_bolum_sonuc:
            model_bolum_sonuc[bolum] = 0

        sonuc = cevap_dogru_mu(mmlu_veri.iloc[i]['cevap'], cevap, mmlu_veri.iloc[i]['secenekler'])
        if sonuc:
            dogru_cevap_sayisi += 1
            model_bolum_sonuc[bolum] += 1

        soru_index = i + 1
        simdi = time.time()
        cubuk = ilerleme_cubugu(soru_index, len(mmlu_veri))

        print(
            f"\r{soru_index} soru çözüldü. Geçen süre: {round(simdi - baslama_zamani, 3)} saniye. Doğru cevap sayısı: {dogru_cevap_sayisi}. Başarı: {round(dogru_cevap_sayisi / soru_index, 4)} İlerleme: {cubuk}",
            end="")

    ortalama = round(dogru_cevap_sayisi / len(mmlu_veri), 4)
    bitis_zamani = time.time()

    model_bolum_sonuc['ortalama'] = ortalama * 100
    model_bolum_sonuclar.append(model_bolum_sonuc)
    model_bolum_sonuclar_df = pd.DataFrame(model_bolum_sonuclar).sort_values(by='ortalama', ascending=False,
                                                                             ignore_index=True)

    # Sonuçları kaydetme ve Hub'a gönderme
    model_bolum_sonuclar_ds = Dataset.from_pandas(model_bolum_sonuclar_df)
    model_bolum_sonuclar_ds.save_to_disk("model_bolum_sonuclar_ds")
   # try:
   #     model_bolum_sonuclar_ds.push_to_hub("alibayram/yapay_zeka_turkce_mmlu_bolum_sonuclari")
   # except Exception as e:
   #     print("Hub'a yükleme hatası: ", e)

    model_detayli_sonuc['dogru_cevap_sayisi'] = dogru_cevap_sayisi
    model_detayli_sonuc['basari'] = ortalama * 100
    model_detayli_sonuc['toplam_sure'] = round(bitis_zamani - baslama_zamani, 3)
    model_detayli_sonuclar.append(model_detayli_sonuc)

    model_detayli_sonuclar_df = pd.DataFrame(model_detayli_sonuclar).sort_values(by='basari', ascending=False,
                                                                                 ignore_index=True)

    sonuc_ds = Dataset.from_pandas(model_detayli_sonuclar_df)
    sonuc_ds.save_to_disk("sonuc_ds")
    #try:
    #    sonuc_ds.push_to_hub("alibayram/yapay_zeka_turkce_mmlu_liderlik_tablosu")
    #except Exception as e:
    #     print("Hub'a yükleme hatası: ", e)

    mmlu_veri_ds = Dataset.from_pandas(mmlu_veri)
    mmlu_veri_ds.save_to_disk("mmlu_veri_ds")
    #try:
    #    mmlu_veri_ds.push_to_hub("alibayram/yapay_zeka_turkce_mmlu_model_cevaplari")
    #except Exception as e:
    #    print("Hub'a yükleme hatası: ", e)

    print(
        f"{soru_index} soru çözüldü. Geçen süre: {round(simdi - baslama_zamani, 3)} saniye. Doğru cevap sayısı: {dogru_cevap_sayisi}")

    return model_detayli_sonuc

modeli_test_et()
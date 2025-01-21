import os
import requests

API_KEY = 'f2ea016667d4fecf9a4a64e77a927b35'

def dizi_ara(dizi_isimi):
    # TMDB API'ye sorgu gönder
    url = f"https://api.themoviedb.org/3/search/tv?api_key={API_KEY}&query={dizi_isimi}&page=1"
    response = requests.get(url)
    results = response.json().get('results', [])

    if results:
        print("Diziler:")
        for i, result in enumerate(results):
            print(f"{i + 1}. {result['name']} ({result['first_air_date']})")

        try:
            secim_index = int(input("\nHangi diziyi izlemek istersiniz? (1, 2, ...) Çıkış için 0: "))
            if secim_index == 0:
                print("Çıkılıyor...")
                return
            elif 1 <= secim_index <= len(results):
                secilen_dizi = results[secim_index - 1]
                print(f"Seçilen Dizi: {secilen_dizi['name']}")
                # Sezon bilgilerini al
                tv_id = secilen_dizi['id']
                sezon_bilgisi(tv_id, secilen_dizi['name'])
            else:
                print("Geçersiz seçim.")
        except ValueError:
            print("Geçersiz giriş.")
    else:
        print("Dizi bulunamadı.")

def sezon_bilgisi(tv_id, dizi_adi):
    # Dizinin sezon bilgilerini al
    url = f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={API_KEY}"
    response = requests.get(url)
    sezonlar = response.json().get('seasons', [])

    if sezonlar:
        print("\nSezonlar:")
        for i, sezon in enumerate(sezonlar):
            print(f"{i + 1}. {sezon['name']} ({sezon['air_date']})")

        try:
            secilen_sezon_index = int(input("\nHangi sezonu izlemek istersiniz? (1, 2, ...) Çıkış için 0: "))
            if secilen_sezon_index == 0:
                print("Çıkılıyor...")
                return
            elif 1 <= secilen_sezon_index <= len(sezonlar):
                secilen_sezon = sezonlar[secilen_sezon_index - 1]
                print(f"Seçilen Sezon: {secilen_sezon['name']}")
                # Bölüm bilgilerini al
                sezon_bolum_bilgisi(tv_id, secilen_sezon['season_number'], dizi_adi, secilen_sezon['name'])
            else:
                print("Geçersiz sezon seçimi.")
        except ValueError:
            print("Geçersiz giriş.")
    else:
        print("Sezon bilgisi bulunamadı.")

def sezon_bolum_bilgisi(tv_id, sezon_no, dizi_adi, sezon_adi):
    # Sezonun bölüm bilgilerini al
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/season/{sezon_no}?api_key={API_KEY}"
    response = requests.get(url)
    bolumler = response.json().get('episodes', [])

    if bolumler:
        print(f"\n{sezon_adi} Bölümleri:")
        for i, bolum in enumerate(bolumler):
            print(f"{i + 1}. {bolum['name']} ({bolum['air_date']})")

        try:
            secilen_bolum_index = int(input("\nHangi bölümü izlemek istersiniz? (1, 2, ...) Çıkış için 0: "))
            if secilen_bolum_index == 0:
                print("Çıkılıyor...")
                return
            elif 1 <= secilen_bolum_index <= len(bolumler):
                secilen_bolum = bolumler[secilen_bolum_index - 1]
                print(f"Seçilen Bölüm: {secilen_bolum['name']}")
                # Linki oluştur
                link = f"https://www.dizibox.plus/{dizi_adi.lower().replace(' ', '-')}-{sezon_no}-sezon-{secilen_bolum_index}-bolum-izle/2/"
                print(f"İzlemek için link: {link}")

                # Linki source_link.py'ye yaz
                with open("source.txt", "w") as f:
                    f.write(f"source_link = '{link}'\n")

                # source_link.py dosyasını çalıştır
                print("\nsource_link.py çalıştırılıyor...")
                os.system("python3 source_link.py")

                return
            else:
                print("Geçersiz bölüm seçimi.")
        except ValueError:
            print("Geçersiz giriş.")
    else:
        print("Bölüm bilgisi bulunamadı.")

def main():
    print("Mei TV'ye Hoşgeldiniz!")
    dizi_isimi = input("İzlemek istediğiniz diziyi giriniz: ")
    dizi_ara(dizi_isimi)

if __name__ == "__main__":
    main()

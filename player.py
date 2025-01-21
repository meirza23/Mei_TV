# -*- coding: utf-8 -*-
import subprocess

# Dosyadaki linki oku
def get_player_link(file_path):
    try:
        with open(file_path, "r") as f:
            link = f.read().strip()  # Dosyadaki linki oku ve boşlukları temizle
        return link if link else None
    except FileNotFoundError:
        print(f"{file_path} bulunamadı!")
        return None

# Linki çözümle ve medya URL'sini döndür
def resolve_media_url(link):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "--no-warnings", "--force-ipv4", 
             "--user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36", 
             link],  # Cookies.txt parametresi kaldırıldı
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            return result.stdout.strip()
        else:
            print("Geçerli bir medya URL'si çözümlenemedi!")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Link çözümlemede hata oluştu: {e.stderr}")
        return None
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        return None

# mpv ile medya oynat
def play_with_mpv(media_url):
    try:
        print(f"mpv ile oynatılıyor: {media_url}")
        result = subprocess.run(["mpv", media_url], check=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"mpv hatası: {result.stderr}")
        else:
            print(f"mpv başarıyla çalıştı.")
    except FileNotFoundError:
        print("mpv player sistemde yüklü değil!")
    except subprocess.CalledProcessError as e:
        print(f"mpv çalıştırılırken bir hata oluştu: {e}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

# Ana program
if __name__ == "__main__":
    file_path = "player_link.txt"

    # Linki dosyadan oku
    link = get_player_link(file_path)

    if link:
        print(f"Okunan link: {link}")
        
        # İlk olarak linki doğrudan mpv ile çalıştırmayı deneyelim
        print(f"mpv ile doğrudan oynatılmaya çalışılıyor: {link}")
        try:
            play_with_mpv(link)
        except Exception as e:
            print(f"Doğrudan mpv ile oynatılırken hata oluştu: {e}")
            print("Şimdi linki çözümlemeye çalışacağız.")

            # Linki çözümlenmeden önce, orijinal linki kaydediyoruz
            temper_link = link

            # Linki çözümle
            media_url = resolve_media_url(link)

            if media_url:
                print(f"Oynatılacak medya linki (çözümlendi): {media_url}")
                # Çözümlenen medya linkini mpv ile oynat
                play_with_mpv(media_url)
            else:
                print(f"Çözümleme başarısız oldu, doğrudan linki mpv ile oynatmayı deniyoruz.")
                # Eğer çözümleme başarısız olursa temper_link'i mpv ile oynat
                play_with_mpv(temper_link)
    else:
        print(f"{file_path} dosyasında link bulunamadı.")

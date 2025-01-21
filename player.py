# -*- coding: utf-8 -*-
import subprocess

# Dosyadaki linki oku
def get_player_link(file_path):
    """Dosyadaki video linkini oku."""
    try:
        with open(file_path, "r") as f:
            link = f.read().strip()  # Dosyadaki linki oku ve boşlukları temizle
        return link if link else None
    except FileNotFoundError:
        print(f"Error: {file_path} bulunamadı!")
        return None

# Linki çözümle ve medya URL'sini döndür
def resolve_media_url(link):
    """Verilen linki çözümleyip medya URL'sini döndür."""
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "--no-warnings", "--force-ipv4",
             "--user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36", 
             link],
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
        print(f"Error: Link çözümlemede hata oluştu: {e.stderr}")
        return None
    except Exception as e:
        print(f"Error: Beklenmeyen bir hata oluştu: {e}")
        return None

def play_with_mpv(media_url):
    """Çözümlenen medya URL'si ile mpv oynatıcıyı başlat."""
    try:
        print(f"mpv ile oynatılıyor: {media_url}")
        
        # Hata ayıklama log dosyasına yazma
        result = subprocess.run(
            ["mpv", "--no-terminal", "--log-file=mpv_log.txt", "--msg-level=all=debug", media_url],
            check=True, capture_output=True, text=True
        )
        
        # Eğer mpv'nin çıktısı hata içeriyorsa, hata mesajlarını göster ve orijinal link ile dene
        if result.returncode != 0 or result.stderr:
            print(f"Error: mpv hatası (returncode): {result.returncode}")
            print(f"Error: mpv hatası (stderr): {result.stderr}")
            raise Exception(f"mpv çalıştırılamadı: {result.stderr}")
        
        print(f"mpv başarıyla çalıştı.")
    except FileNotFoundError:
        print("Error: mpv player sistemde yüklü değil!")
    except subprocess.CalledProcessError as e:
        print(f"Error: mpv çalıştırılırken bir hata oluştu (stderr): {e.stderr}")
        print(f"Error: mpv çalıştırılırken bir hata oluştu (stdout): {e.stdout}")
        print("Doğrudan orijinal link ile oynatmayı deniyoruz...")
        play_with_mpv(original_link)  # Orijinal link ile oynatmayı dene
    except Exception as e:
        print(f"Error: Beklenmeyen bir hata oluştu: {e}")
        raise e  # Hata durumu daha üst katmana iletilir

# Ana program
if __name__ == "__main__":
    file_path = "player_link.txt"  # Dinamik olarak dosyadan okuma

    # Linki dosyadan oku
    original_link = get_player_link(file_path)

    if original_link:
        print(f"Okunan link: {original_link}")

        # Linki çözümle
        media_url = resolve_media_url(original_link)

        if media_url:
            print(f"Çözümlenen medya linki: {media_url}")
            print("mpv ile çözümlenen link oynatılıyor...")
            try:
                play_with_mpv(media_url)
            except Exception as e:
                print(f"Error: Çözümlenen linkle oynatma başarısız oldu: {e}")
                print("Doğrudan orijinal link ile oynatmayı deniyoruz...")
                play_with_mpv(original_link)
        else:
            print("Error: Çözümlenen bir link bulunamadı.")
            print("Doğrudan orijinal link ile oynatmayı deniyoruz...")
            play_with_mpv(original_link)
    else:
        print(f"Error: {file_path} dosyasında link bulunamadı!")


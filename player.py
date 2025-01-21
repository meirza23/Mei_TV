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

def resolve_media_url(link):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "--no-warnings", "--force-ipv4", 
             "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", 
             "--cookies", "/path/to/cookies.txt", link],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Link çözümlemede hata oluştu: {e.stderr}")
        return None


# mpv ile medya oynat
def play_with_mpv(media_url):
    try:
        subprocess.run(["mpv", media_url], check=True)
    except FileNotFoundError:
        print("mpv player sistemde yüklü değil!")
    except subprocess.CalledProcessError as e:
        print(f"mpv çalıştırılırken bir hata oluştu: {e}")

# Ana program
if __name__ == "__main__":
    file_path = "player_link.txt"

    # Linki dosyadan oku
    link = get_player_link(file_path)

    if link:
        print(f"Okunan link: {link}")
        
        # Linki çözümle
        media_url = resolve_media_url(link)

        if media_url:
            print(f"Oynatılacak medya linki (çözümlendi): {media_url}")
            # Çözümlenen medya linkini mpv ile oynat
            play_with_mpv(media_url)
        else:
            print(f"Çözümleme başarısız oldu, doğrudan linki mpv ile oynatmayı deniyoruz.")
            # Eğer çözümleme başarısız olursa doğrudan vidmoly linkini mpv ile oynat
            play_with_mpv(link)
    else:
        print(f"{file_path} dosyasında link bulunamadı.")

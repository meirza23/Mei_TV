from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import time
import subprocess  # player.py'i çalıştırmak için

from main import sezon_bolum_bilgisi

# Ağ loglarını almak için Chrome DevTools'u etkinleştirme
def setup_driver():
    # Chrome DevTools protokolünü etkinleştirme
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}  # Performans loglarını aç

    # Chrome ayarları
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    # Başlıkları ayarlama (fetch'teki başlıkları örnek olarak ekliyoruz)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36")
    options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
    options.add_argument("accept-language=en-US,en;q=0.9")
    options.add_argument("sec-ch-ua=\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"")
    options.add_argument("sec-ch-ua-mobile=?0")
    options.add_argument("sec-ch-ua-platform=\"Linux\"")
    options.add_argument("sec-fetch-dest=iframe")
    options.add_argument("sec-fetch-mode=navigate")
    options.add_argument("sec-fetch-site=cross-site")
    options.add_argument("upgrade-insecure-requests=1")
    
    # Driver'ı başlat
    service = Service("/opt/chrome/chromedriver-linux64/chromedriver")  # ChromeDriver yolunu belirt
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Ağ loglarını toplama
def capture_network_logs(driver, url_list):
    try:
        # URL listesi üzerinde dönerek her birini deneyelim
        for url in url_list:
            driver.get(url)  # Sayfayı aç

            logs = driver.get_log("performance")
            document_urls = []
            start_time = time.time()

            for entry in logs:
                if time.time() - start_time > 180:
                    print("3 dakika boyunca link bulunamadı. Döngü sonlandırılıyor.")
                    break  # 3 dakika geçtiği için döngüden çık

                log = json.loads(entry["message"])  # JSON formatında çöz
                message = log["message"]
                method = message.get("method", "")
                type_ = message.get("params", {}).get("type", "")
                document_url = message.get("params", {}).get("documentURL", "")

                # Sadece "document" türündeki ve "documentURL" bulunan ağ isteklerini filtrele
                if method == "Network.requestWillBeSent" and type_ == "Document" and document_url:
                    # Eğer documentURL https://vidmoly.to ile başlıyorsa ve .html ile bitiyorsa, işlem bitir
                    if document_url.startswith("https://vidmoly.to") and document_url.endswith(".html"):
                        document_urls.append(document_url)
                        # Bulunan URL'yi player_link.txt dosyasına yaz
                        with open("player_link.txt", "w") as f:
                            f.write(document_url)
                        print(f"Kaynak bulundu: {document_url}")
                        return  # Bulunduğunda işleme son ver

            # Eğer burada hiçbir şey bulunamazsa, diğer URL'yi deneyelim
            print(f"{url} üzerinde kaynak bulunamadı, başka birini deniyoruz...")

        # Eğer hiçbir URL çalışmazsa
        print("Kaynak bulunamadı.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    finally:
        # Driver'ı kapat
        driver.quit()

        # player.py'yi çağır
        try:
            subprocess.run(["python3", "player.py"], check=True)
        except Exception as e:
            print(f"player.py çağrılırken bir hata oluştu: {e}")

# Ana program
if __name__ == "__main__":
    # source.txt dosyasındaki linki oku ve URL'yi al
    with open("source.txt", "r") as f:
        source_line = f.readline().strip()  # ilk satırdaki linki al
        link = source_line.split('=')[-1].strip().strip("'")  # 'source_link = ' kısmını ayıklayıp linki al

    # source.txt dosyasını temizle
    with open("source.txt", "w") as f:
        f.write("")  # Dosyayı boşalt

    # Alternatif URL'leri oluştur
    url_list = [
        link,
        link.replace("/2/", "/1/"),
        link.replace("/2/", "/3/"),
        link.replace("/2/", "/4/")
    ]

    driver = setup_driver()
    capture_network_logs(driver, url_list)

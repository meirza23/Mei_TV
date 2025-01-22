import json
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def setup_driver():
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"} 

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36")
    
    service = Service("/opt/chrome/chromedriver-linux64/chromedriver")  
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def capture_network_logs_and_cookies(driver, url_list):
    try:
        document_urls = [] 
        for url in url_list:
            driver.get(url) 

            logs = driver.get_log("performance")
            start_time = time.time()

            for entry in logs:
                if time.time() - start_time > 180:
                    print("3 dakika boyunca link bulunamadı. Döngü sonlandırılıyor.")
                    break  

                log = json.loads(entry["message"])  
                message = log["message"]
                method = message.get("method", "")
                type_ = message.get("params", {}).get("type", "")
                document_url = message.get("params", {}).get("documentURL", "")

                if method == "Network.requestWillBeSent" and type_ == "Document" and document_url:
                    if document_url.startswith("https://vidmoly.to") and document_url.endswith(".html"):
                        document_urls.append(document_url)
                        with open("player_link.txt", "w") as f:
                            f.write(document_url)
                        print(f"Kaynak bulundu: {document_url}")
                        break 

            if document_urls:
                break
            else:
                print(f"{url} üzerinde kaynak bulunamadı, başka birini deniyoruz...")

        if document_urls:
            try:
                subprocess.run(["python3", "player.py"], check=True)
            except Exception as e:
                print(f"player.py çağrılırken bir hata oluştu: {e}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":

    with open("source.txt", "r") as f:
        source_line = f.readline().strip() 
        link = source_line.split('=')[-1].strip().strip("'")  

    with open("source.txt", "w") as f:
        f.write("")  

    url_list = [
        link,
        link.replace("/2/", "/1/"),
        link.replace("/2/", "/3/")
    ]

    driver = setup_driver()
    capture_network_logs_and_cookies(driver, url_list)

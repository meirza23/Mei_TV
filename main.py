import os
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

API_KEY = 'f2ea016667d4fecf9a4a64e77a927b35'

class MeiTVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mei TV")
        
        # Pencere boyutu ve arka plan rengi
        self.root.geometry("600x600")
        self.root.configure(bg="#f4f4f9")
        
        # Ana başlık fontu ve rengi
        self.label_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.label = tk.Label(root, text="Mei TV'ye Hoşgeldiniz!", font=self.label_font, bg="#f4f4f9", fg="#2e3b4e")
        self.label.pack(pady=20)

        # Dizi adı girişi
        self.dizi_isimi_label = tk.Label(root, text="İzlemek istediğiniz diziyi giriniz:", font=("Arial", 12), bg="#f4f4f9", fg="#333")
        self.dizi_isimi_label.pack(pady=10)
        
        self.dizi_isimi_entry = tk.Entry(root, width=50, font=("Arial", 12))
        self.dizi_isimi_entry.pack(pady=10)

        # Ara butonu (animasyon ve stil)
        self.ara_button = tk.Button(root, text="Ara", command=self.dizi_ara, relief="flat", bg="#56CCF2", fg="white", font=("Arial", 14), width=20)
        self.ara_button.pack(pady=15)

        self.result_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12), bg="#e6e6e6", selectmode=tk.SINGLE)
        self.result_listbox.pack(pady=10)

        self.sezon_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12), bg="#e6e6e6", selectmode=tk.SINGLE)
        self.sezon_listbox.pack(pady=10)

        self.bolum_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12), bg="#e6e6e6", selectmode=tk.SINGLE)
        self.bolum_listbox.pack(pady=10)

    def dizi_ara(self):
        dizi_isimi = self.dizi_isimi_entry.get()
        if not dizi_isimi:
            messagebox.showwarning("Giriş Hatası", "Lütfen dizi ismini giriniz.")
            return

        url = f"https://api.themoviedb.org/3/search/tv?api_key={API_KEY}&query={dizi_isimi}&page=1"
        response = requests.get(url)
        results = response.json().get('results', [])

        if results:
            self.result_listbox.delete(0, tk.END)
            for i, result in enumerate(results):
                self.result_listbox.insert(tk.END, f"{i + 1}. {result['name']} ({result['first_air_date']})")
            self.result_listbox.bind("<Double-1>", lambda event: self.sezon_bilgisi(results[self.result_listbox.curselection()[0]]))
        else:
            messagebox.showinfo("Sonuç", "Dizi bulunamadı.")

    def sezon_bilgisi(self, secilen_dizi):
        tv_id = secilen_dizi['id']
        url = f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={API_KEY}"
        response = requests.get(url)
        sezonlar = response.json().get('seasons', [])

        if sezonlar:
            self.sezon_listbox.delete(0, tk.END)
            for i, sezon in enumerate(sezonlar):
                self.sezon_listbox.insert(tk.END, f"{i + 1}. {sezon['name']} ({sezon['air_date']})")
            self.sezon_listbox.bind("<Double-1>", lambda event: self.sezon_bolum_bilgisi(secilen_dizi, sezonlar[self.sezon_listbox.curselection()[0]]))
        else:
            messagebox.showinfo("Sonuç", "Sezon bilgisi bulunamadı.")

    def sezon_bolum_bilgisi(self, secilen_dizi, secilen_sezon):
        tv_id = secilen_dizi['id']
        sezon_no = secilen_sezon['season_number']
        url = f"https://api.themoviedb.org/3/tv/{tv_id}/season/{sezon_no}?api_key={API_KEY}"
        response = requests.get(url)
        bolumler = response.json().get('episodes', [])

        if bolumler:
            self.bolum_listbox.delete(0, tk.END)
            for i, bolum in enumerate(bolumler):
                self.bolum_listbox.insert(tk.END, f"{i + 1}. {bolum['name']} ({bolum['air_date']})")
            self.bolum_listbox.bind("<Double-1>", lambda event: self.link_olustur(secilen_dizi['name'], sezon_no, bolumler[self.bolum_listbox.curselection()[0]]))
        else:
            messagebox.showinfo("Sonuç", "Bölüm bilgisi bulunamadı.")

    def link_olustur(self, dizi_adi, sezon_no, secilen_bolum):
        link = f"https://www.dizibox.plus/{dizi_adi.lower().replace(' ', '-')}-{sezon_no}-sezon-{secilen_bolum['episode_number']}-bolum-izle/2/"

        # Linki source_link.py'ye yaz
        with open("source.txt", "w") as f:
            f.write(f"source_link = '{link}'\n")

        # source_link.py dosyasını çalıştır
        print("\nsource_link.py çalıştırılıyor...")
        os.system("python3 source_link.py")


if __name__ == "__main__":
    root = tk.Tk()
    app = MeiTVApp(root)
    root.mainloop()

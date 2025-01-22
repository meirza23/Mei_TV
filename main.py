import os
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import source_link
import player

API_KEY = 'YOUR_TMDB_API_KEY'

class MeiTVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mei TV")

        self.root.geometry("600x700")
        self.root.configure(bg="#121212")  

        self.label_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.label = tk.Label(root, text="Mei TV'ye Hoşgeldiniz!", font=self.label_font, bg="#121212", fg="#FF6F00")
        self.label.pack(pady=30)

        self.dizi_isimi_label = tk.Label(root, text="İzlemek istediğiniz diziyi giriniz:", font=("Arial", 14), bg="#121212", fg="#ffffff")
        self.dizi_isimi_label.pack(pady=10)

        self.dizi_isimi_entry = tk.Entry(root, width=50, font=("Arial", 14), bg="#333333", fg="#ffffff", bd=0, relief="solid", highlightthickness=2)
        self.dizi_isimi_entry.pack(pady=10)
        self.dizi_isimi_entry.bind("<Return>", self.dizi_ara)

        self.ara_button = tk.Button(root, text="Ara", command=self.dizi_ara, relief="flat", bg="#FF6F00", fg="white", font=("Arial", 16), width=20, height=2, bd=0, highlightthickness=0)
        self.ara_button.pack(pady=15)
        self.ara_button.bind("<Enter>", lambda e: self.ara_button.config(bg="#FF8C00"))
        self.ara_button.bind("<Leave>", lambda e: self.ara_button.config(bg="#FF6F00"))

        self.result_listbox_frame = tk.Frame(root, bg="#121212")
        self.result_listbox_frame.pack(pady=10)

        self.result_listbox = tk.Listbox(self.result_listbox_frame, width=50, height=6, font=("Arial", 12), bg="#2e2e2e", fg="#ffffff", selectmode=tk.SINGLE, bd=0, highlightthickness=0)
        self.result_listbox.pack(side="left", fill="y", padx=5, pady=5)

        self.scrollbar = tk.Scrollbar(self.result_listbox_frame, orient="vertical", command=self.result_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_listbox.config(yscrollcommand=self.scrollbar.set)

        self.sezon_listbox_frame = tk.Frame(root, bg="#121212")
        self.sezon_listbox_frame.pack(pady=10)

        self.sezon_listbox = tk.Listbox(self.sezon_listbox_frame, width=50, height=6, font=("Arial", 12), bg="#2e2e2e", fg="#ffffff", selectmode=tk.SINGLE, bd=0, highlightthickness=0)
        self.sezon_listbox.pack(side="left", fill="y", padx=5, pady=5)

        self.scrollbar2 = tk.Scrollbar(self.sezon_listbox_frame, orient="vertical", command=self.sezon_listbox.yview)
        self.scrollbar2.pack(side="right", fill="y")
        self.sezon_listbox.config(yscrollcommand=self.scrollbar2.set)

        self.bolum_listbox_frame = tk.Frame(root, bg="#121212")
        self.bolum_listbox_frame.pack(pady=10)

        self.bolum_listbox = tk.Listbox(self.bolum_listbox_frame, width=50, height=6, font=("Arial", 12), bg="#2e2e2e", fg="#ffffff", selectmode=tk.SINGLE, bd=0, highlightthickness=0)
        self.bolum_listbox.pack(side="left", fill="y", padx=5, pady=5)

        self.scrollbar3 = tk.Scrollbar(self.bolum_listbox_frame, orient="vertical", command=self.bolum_listbox.yview)
        self.scrollbar3.pack(side="right", fill="y")
        self.bolum_listbox.config(yscrollcommand=self.scrollbar3.set)

    def dizi_ara(self, event=None):
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

        with open("source.txt", "w") as f:
            f.write(f"source_link = '{link}'\n")

        print("\nsource_link.py çalıştırılıyor...")
        os.system("python3 source_link.py")


if __name__ == "__main__":
    root = tk.Tk()
    app = MeiTVApp(root)
    root.mainloop()

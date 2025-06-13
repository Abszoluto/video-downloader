import os
import zipfile
import urllib.request
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import re
import time
from itertools import cycle
import sys
from PIL import Image, ImageTk

# --------- SPLASH SCREEN ---------
class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("520x320+700+350")
        self.overrideredirect(True)

        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        try:
            bg_img = Image.open("background.png").resize((520, 320), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.canvas = tk.Canvas(self, width=520, height=320, highlightthickness=0, bd=0)
            self.canvas.pack()
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
            self.canvas.create_text(260, 30, text="Universal Video Downloader", font=("Segoe UI", 20, "bold"), fill="red")
#            self.canvas.create_text(260, 60, text="", font=("Segoe UI", 12, "italic"), fill="#bbbbbb")
        except Exception as e:
            print(f"Erro ao carregar imagem da splash: {e}")

        self.progress = ttk.Progressbar(self, mode="determinate", length=350, maximum=100)
        self.progress.place(x=85, y=280)
        self.progress["value"] = 0
        self.rainbow_colors = cycle(["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#00ffff", "#0000ff", "#8b00ff"])
        self.anim = self.after(50, self.animate_bar)
        self.after(3000, self.close_splash)

    def close_splash(self):
        if hasattr(self, 'anim'):
            self.after_cancel(self.anim)
        self.destroy()

    def animate_bar(self):
        cor = next(self.rainbow_colors)
        splash_style = ttk.Style()
        splash_style.theme_use("clam")
        splash_style.configure("NeonSplash.Horizontal.TProgressbar", background=cor, troughcolor="#1a1a1a")
        self.progress.configure(style="NeonSplash.Horizontal.TProgressbar")
        self.progress["value"] += 2
        if self.progress["value"] < 100:
            self.anim = self.after(50, self.animate_bar)

# --------- FUNÇÃO PARA BAIXAR FFMPEG ---------
def baixar_ffmpeg_local():
    ffmpeg_pasta = "ffmpeg"
    ffmpeg_exe = os.path.join(ffmpeg_pasta, "ffmpeg.exe")

    if os.path.exists(ffmpeg_exe):
        return ffmpeg_exe

    os.makedirs(ffmpeg_pasta, exist_ok=True)
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(ffmpeg_pasta, "ffmpeg.zip")

    try:
        adicionar_mensagem("🔽 Baixando FFmpeg...")
        urllib.request.urlretrieve(url, zip_path)

        adicionar_mensagem("✅ Extraindo FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                if name.endswith("ffmpeg.exe") and "bin/" in name:
                    zip_ref.extract(name, ffmpeg_pasta)
                    caminho_extraido = os.path.join(ffmpeg_pasta, name)
                    destino = os.path.join(ffmpeg_pasta, "ffmpeg.exe")
                    shutil.move(caminho_extraido, destino)
                    break

        os.remove(zip_path)
        adicionar_mensagem("🎬 FFmpeg pronto para uso.")
        return ffmpeg_exe

    except Exception as e:
        adicionar_mensagem(f"Erro ao preparar FFmpeg: {e}")
        return None

# --------- FUNÇÕES DA GUI ---------
def escolher_diretorio():
    pasta = filedialog.askdirectory()
    if pasta:
        entrada_diretorio.delete(0, tk.END)
        entrada_diretorio.insert(0, pasta)

def atualizar_progresso(texto):
    match = re.search(r'\b(\d{1,3}\.\d)%', texto)
    if match:
        progresso = float(match.group(1))
        barra_progresso["value"] = progresso
        janela.update_idletasks()

def adicionar_mensagem(msg):
    try:
        texto_saida.insert(tk.END, msg + "\n")
        texto_saida.see(tk.END)
        janela.update_idletasks()
    except:
        pass

def baixar():
    url = entrada_url.get().strip()
    diretorio = entrada_diretorio.get().strip()

    if not url:
        messagebox.showwarning("Aviso", "Insira uma URL.", parent=janela)
        return
    if not diretorio:
        messagebox.showwarning("Aviso", "Escolha um diretório de download.", parent=janela)
        return

    botao_baixar.config(state=tk.DISABLED)
    barra_progresso["value"] = 0
    texto_saida.delete(1.0, tk.END)
    status_var.set("⏳ Baixando...")

    thread = threading.Thread(target=baixar_video, args=(url, diretorio))
    thread.start()

def baixar_video(url, diretorio):
    ffmpeg_exe = baixar_ffmpeg_local()
    if not ffmpeg_exe:
        messagebox.showerror("Erro", "Não foi possível preparar o FFmpeg.", parent=janela)
        botao_baixar.config(state=tk.NORMAL)
        status_var.set("Erro.")
        return

    comando = [
        "yt-dlp",
        "-f", "137+140/best[ext=mp4]/b",
        "--merge-output-format", "mp4",
        "--ffmpeg-location", ffmpeg_exe,
        "-o", os.path.join(diretorio, "%(title)s.%(ext)s"),
        "--no-part",  # <- ESSENCIAL para evitar arquivos duplicados
        url
    ]

    try:
        processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for linha in processo.stdout:
            adicionar_mensagem(linha.strip())
            atualizar_progresso(linha)

        processo.wait()
        if processo.returncode == 0:
            status_var.set("✅ Concluído.")
            messagebox.showinfo("Concluído", "Download finalizado com sucesso!", parent=janela)
        else:
            status_var.set("❌ Erro.")
            messagebox.showerror("Erro", "Erro durante o download.", parent=janela)
    except Exception as e:
        status_var.set("❌ Erro.")
        messagebox.showerror("Erro", f"Erro ao executar yt-dlp: {e}", parent=janela)

    botao_baixar.config(state=tk.NORMAL)

def animar_barra_neon():
    cores = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#00ffff", "#0000ff", "#8b00ff"]
    i = 0

    def atualizar_cor():
        nonlocal i
        barra_progresso.configure(style=f"Neon{i}.Horizontal.TProgressbar")
        i = (i + 1) % len(cores)
        janela.after(120, atualizar_cor)

    for idx, cor in enumerate(cores):
        estilo.configure(f"Neon{idx}.Horizontal.TProgressbar", troughcolor="#222", background=cor)

    atualizar_cor()

# --------- GUI PRINCIPAL ---------
def criar_gui():
    global janela, entrada_url, entrada_diretorio, botao_baixar, barra_progresso, texto_saida, status_var, estilo

    janela = tk.Tk()
    janela.title("Universal Video Downloader")
    janela.geometry("700x620")
    janela.configure(bg="#121212")
    janela.resizable(False, False)

    try:
        janela.iconbitmap("icon.ico")
    except:
        pass

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("TButton", font=("Segoe UI", 11), padding=10, background="#8B0000", foreground="white", borderwidth=0)
    estilo.map("TButton", background=[("active", "#ff3333")])
    estilo.configure("TLabel", background="#121212", foreground="white", font=("Segoe UI", 11))
    estilo.configure("TEntry", fieldbackground="#1e1e1e", foreground="white")
    estilo.configure("TProgressbar", thickness=20, troughcolor="#222", background="#ff3333")

    tk.Label(janela, text="Universal Video Downloader", font=("Segoe UI", 18, "bold"), bg="#121212", fg="#ff3333").pack(pady=15)

    tk.Label(janela, text="URL do vídeo:").pack(pady=(10, 0))
    entrada_url = ttk.Entry(janela, width=80)
    entrada_url.pack(pady=5)

    tk.Label(janela, text="Diretório de download:").pack(pady=(10, 0))
    frame_diretorio = tk.Frame(janela, bg="#121212")
    entrada_diretorio = ttk.Entry(frame_diretorio, width=60)
    entrada_diretorio.pack(side=tk.LEFT, padx=(0, 10), pady=5)
    ttk.Button(frame_diretorio, text="Selecionar Pasta", command=escolher_diretorio).pack(side=tk.LEFT)
    frame_diretorio.pack()

    botao_baixar = ttk.Button(janela, text="▶ Baixar Agora", command=baixar)
    botao_baixar.pack(pady=15)

    barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=600, mode="determinate")
    barra_progresso.pack(pady=5)

    tk.Label(janela, text="Progresso detalhado:").pack(pady=(10, 0))
    texto_saida = ScrolledText(janela, width=85, height=15, font=("Consolas", 10), bg="#0d0d0d", fg="#39ff14", insertbackground="white")
    texto_saida.pack(pady=5)

    status_var = tk.StringVar()
    status_var.set("Aguardando...")
    status_label = tk.Label(janela, textvariable=status_var, bg="#121212", fg="#bbbbbb", font=("Segoe UI", 10, "italic"))
    status_label.pack(pady=(0, 15))

    animar_barra_neon()
    return janela

# --------- MAIN ---------
def main():
    root = tk.Tk()
    root.withdraw()
    splash = SplashScreen(root)
    root.after(3000, lambda: (splash.destroy(), root.destroy()))
    root.mainloop()
    app = criar_gui()
    app.mainloop()

if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    main()
"""
Auto Clicker - GUI versiyonu
- Baslat/Durdur: buton veya F6
- Cikis: buton veya F9 (pencereden)
"""
import threading
import time
import tkinter as tk
from tkinter import ttk

from pynput import mouse, keyboard

# --- Tema renkleri (koyu) ---
BG      = "#1e1e2e"
FG      = "#cdd6f4"
ACCENT  = "#89b4fa"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
CARD    = "#313244"

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        root.title("Auto Clicker")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.running = False
        self.stop_evt = threading.Event()

        self._build_ui()

        # Global kisa yol dinleyicisi (arka planda)
        threading.Thread(target=self._hotkey_listener, daemon=True).start()

        # Tiklama dongusu (arka planda)
        self.ctrl = mouse.Controller()

    # ---------- Arayuz ----------
    def _build_ui(self):
        pad = {"padx": 16, "pady": 8}

        # Baslik
        title = tk.Label(self.root, text="🖱️  AUTO CLICKER", font=("Segoe UI", 16, "bold"),
                         bg=BG, fg=ACCENT)
        title.pack(pady=(16, 4))

        # --- Hiz ---
        frame_speed = tk.Frame(self.root, bg=CARD)
        frame_speed.pack(fill="x", **pad)

        tk.Label(frame_speed, text="Tik / saniye:", font=("Segoe UI", 11),
                 bg=CARD, fg=FG).pack(side="left", padx=12, pady=10)

        self.speed_var = tk.IntVar(value=100)
        self.speed = ttk.Scale(frame_speed, from_=1, to=1000, variable=self.speed_var,
                               command=lambda _: self._update_speed_label())
        self.speed.pack(side="left", fill="x", expand=True, padx=8, pady=10)

        self.speed_label = tk.Label(frame_speed, text="100", font=("Segoe UI", 11, "bold"),
                                    bg=CARD, fg=GREEN, width=6)
        self.speed_label.pack(side="right", padx=12, pady=10)

        # --- Buton secimi ---
        frame_btn = tk.Frame(self.root, bg=CARD)
        frame_btn.pack(fill="x", **pad)

        tk.Label(frame_btn, text="Tiklama butonu:", font=("Segoe UI", 11),
                 bg=CARD, fg=FG).pack(side="left", padx=12, pady=10)

        self.btn_var = tk.StringVar(value="left")
        for text, val in [("Sol", "left"), ("Sag", "right"), ("Orta", "middle")]:
            tk.Radiobutton(frame_btn, text=text, value=val, variable=self.btn_var,
                           bg=CARD, fg=FG, selectcolor=CARD,
                           activebackground=CARD, activeforeground=FG,
                           font=("Segoe UI", 10)).pack(side="left", padx=8, pady=10)

        # --- Tiklama tipi ---
        frame_type = tk.Frame(self.root, bg=CARD)
        frame_type.pack(fill="x", **pad)

        tk.Label(frame_type, text="Tiklama turu:", font=("Segoe UI", 11),
                 bg=CARD, fg=FG).pack(side="left", padx=12, pady=10)

        self.type_var = tk.StringVar(value="single")
        tk.Radiobutton(frame_type, text="Tek", value="single", variable=self.type_var,
                       bg=CARD, fg=FG, selectcolor=CARD,
                       activebackground=CARD, activeforeground=FG,
                       font=("Segoe UI", 10)).pack(side="left", padx=8, pady=10)
        tk.Radiobutton(frame_type, text="Cift", value="double", variable=self.type_var,
                       bg=CARD, fg=FG, selectcolor=CARD,
                       activebackground=CARD, activeforeground=FG,
                       font=("Segoe UI", 10)).pack(side="left", padx=8, pady=10)

        # --- Konum ---
        frame_pos = tk.Frame(self.root, bg=CARD)
        frame_pos.pack(fill="x", **pad)

        self.pos_var = tk.StringVar(value="mouse")
        tk.Radiobutton(frame_pos, text="Fare neredeyse", value="mouse", variable=self.pos_var,
                       bg=CARD, fg=FG, selectcolor=CARD,
                       activebackground=CARD, activeforeground=FG,
                       font=("Segoe UI", 10)).pack(side="left", padx=12, pady=10)
        tk.Radiobutton(frame_pos, text="Sabit konum", value="fixed", variable=self.pos_var,
                       bg=CARD, fg=FG, selectcolor=CARD,
                       activebackground=CARD, activeforeground=FG,
                       font=("Segoe UI", 10)).pack(side="left", padx=8, pady=10)

        self.fixed_x = tk.StringVar(value="960")
        self.fixed_y = tk.StringVar(value="540")
        tk.Label(frame_pos, text="X:", bg=CARD, fg=FG).pack(side="left", padx=(12, 0))
        tk.Entry(frame_pos, textvariable=self.fixed_x, width=5, bg=BG, fg=FG,
                 insertbackground=FG, relief="flat").pack(side="left", padx=2)
        tk.Label(frame_pos, text="Y:", bg=CARD, fg=FG).pack(side="left", padx=(8, 0))
        tk.Entry(frame_pos, textvariable=self.fixed_y, width=5, bg=BG, fg=FG,
                 insertbackground=FG, relief="flat").pack(side="left", padx=2)

        # --- Baslat / Durdur ---
        self.toggle_btn = tk.Button(self.root, text="▶  BASLAT", font=("Segoe UI", 13, "bold"),
                                    bg=GREEN, fg="#1e1e2e", activebackground=GREEN,
                                    relief="flat", cursor="hand2", bd=0,
                                    command=self.toggle)
        self.toggle_btn.pack(fill="x", padx=16, pady=(4, 4), ipady=8)

        # --- Alt bilgi ---
        info = tk.Label(self.root, text="Kisa yol:  F6 = baslat/durdur   •   F9 = cik",
                        font=("Segoe UI", 9), bg=BG, fg=FG)
        info.pack(pady=(4, 12))

    # ---------- Mantik ----------
    def _update_speed_label(self):
        self.speed_label.config(text=str(self.speed_var.get()))

    def _hotkey_listener(self):
        with keyboard.Listener(on_press=self._on_key) as listener:
            listener.join()

    def _on_key(self, key):
        try:
            if key == keyboard.Key.f6:
                self.root.after(0, self.toggle)
            elif key == keyboard.Key.f9:
                self.root.after(0, self._quit)
        except AttributeError:
            pass

    def toggle(self):
        if self.running:
            self._stop()
        else:
            self._start()

    def _start(self):
        self.running = True
        self.toggle_btn.config(text="■  DURDUR", bg=RED, activebackground=RED)
        threading.Thread(target=self._click_loop, daemon=True).start()

    def _stop(self):
        self.running = False
        self.toggle_btn.config(text="▶  BASLAT", bg=GREEN, activebackground=GREEN)

    def _click_loop(self):
        speed = self.speed_var.get()
        interval = 1.0 / speed
        button = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle,
        }[self.btn_var.get()]
        click_type = self.type_var.get()

        # Sabit konum kullanilacaksa hesapla
        fixed = None
        if self.pos_var.get() == "fixed":
            try:
                fixed = (int(self.fixed_x.get()), int(self.fixed_y.get()))
            except ValueError:
                fixed = None

        while self.running:
            if fixed:
                self.ctrl.position = fixed
            if click_type == "double":
                self.ctrl.click(button, 2)
            else:
                self.ctrl.click(button)
            time.sleep(interval)

    def _quit(self):
        self.running = False
        self.stop_evt.set()
        self.root.destroy()

    def on_close(self):
        self._quit()


def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()

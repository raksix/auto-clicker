"""
Otomatik tıkla (Auto Clicker)
- Başlat/Durdur: F6
- Çıkış: F9
"""
import sys
import time
import threading
from pynput import mouse, keyboard

# Ayarlar
INTERVAL = 0.01          # tıklama aralığı (saniye) - 0.01 = 100 tık/sn
BUTTON = mouse.Button.left
RUNNING = False
stop_flag = threading.Event()

def clicker_loop():
    """Sürekli tıklayan döngü."""
    ctrl = mouse.Controller()
    while not stop_flag.is_set():
        if RUNNING:
            ctrl.click(BUTTON)
        time.sleep(INTERVAL)

def on_press(key):
    global RUNNING
    try:
        if key == keyboard.Key.f6:
            RUNNING = not RUNNING
            status = "BASLADI" if RUNNING else "DURDURULDU"
            print(f"[{status}] tiklamalar {'aktif' if RUNNING else 'pasif'}")
        elif key == keyboard.Key.f9:
            print("Cikiliyor...")
            stop_flag.set()
            sys.exit(0)
    except AttributeError:
        pass

def main():
    print("=== AUTO CLICKER ===")
    print(f"Tiklama araligi : {INTERVAL} sn  ({round(1/INTERVAL)} tik/sn)")
    print("F6 = Baslat/Durdur    F9 = Cik")
    print("-" * 40)

    # Tıklama döngüsünü arka planda başlat
    t = threading.Thread(target=clicker_loop, daemon=True)
    t.start()

    # Klavye dinleyici
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()

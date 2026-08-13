# 🖱️ Auto Clicker

Hızlı ve kullanımı kolay bir otomatik tıklama (auto clicker) uygulaması. GUI ve terminal versiyonu içerir.

## ✨ Özellikler

- ⚡ 1–1000 tık/saniye arası ayarlanabilir hız (slider ile)
- 🖱️ Sol / Sağ / Orta buton seçimi
- 🔄 Tek veya çift tıklama
- 📍 Fare konumunu takip et veya sabit X/Y koordinatı kullan
- ⌨️ Klavye kısayolları: `F6` = başlat/durdur, `F9` = çık
- 🎨 Koyu modern tema (GUI)

## 🚀 Kullanım

### Hazır EXE (Python gerektirmez)

Windows 10/11 için derlenmiş sürümü [Releases](https://github.com/raksix/auto-clicker/releases) sayfasından indirip çalıştırabilirsin.

> **Not:** İmzasız EXE olduğu için Windows SmartScreen uyarı gösterebilir — **"Daha fazla bilgi" → "Yine de çalıştır"** diyerek geçilir. Antivirüsler de imza eksikliğinden yanlış alarm verebilir; kod tamamen temizdir.

### Kaynak koddan çalıştırma

```bash
# Gereksinimler
pip install pynput

# GUI versiyonu
python autoclicker_gui.py

# Terminal versiyonu
python autoclicker.py
```

## 📦 EXE'yi kendin derlemek

```bash
pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name "AutoClicker" autoclicker_gui.py
```

Çıktı: `dist/AutoClicker.exe`

## 📁 Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `autoclicker_gui.py` | GUI versiyonu (tkinter) |
| `autoclicker.py` | Basit terminal versiyonu |

## ⚠️ Sorumluluk Reddi

Bu uygulama eğitim ve kişisel kullanım içindir. Oyunlarda veya yasaklı ortamlarda hile amaçlı kullanımı hizmet şartlarını ihlal edebilir. Kullanımından doğacak sonuçlardan kullanıcı sorumludur.

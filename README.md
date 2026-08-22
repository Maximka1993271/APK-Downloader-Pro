<h1 align="center">📱 APK Downloader Pro</h1>

<p align="center">
  <a href="https://github.com/Maximka1993271/APK-Downloader-Pro/releases">
    <img src="https://img.shields.io/badge/version-1.2.1-blue.svg?style=for-the-badge&logo=github" alt="Version"/>
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=for-the-badge&logo=python" alt="Python"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge" alt="License"/>
  </a>
  <a href="https://github.com/Maximka1993271/APK-Downloader-Pro/releases">
    <img src="https://img.shields.io/github/downloads/Maximka1993271/APK-Downloader-Pro/total.svg?style=for-the-badge&logo=github" alt="Downloads"/>
  </a>
  <a href="https://github.com/Maximka1993271/APK-Downloader-Pro">
    <img src="https://img.shields.io/badge/Open%20Source-✅-brightgreen.svg?style=for-the-badge" alt="Open Source"/>
  </a>
  <a href="https://github.com/Maximka1993271/APK-Downloader-Pro">
    <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg?style=for-the-badge" alt="Platform"/>
  </a>
  <a href="https://github.com/Maximka1993271/APK-Downloader-Pro">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge&logo=github" alt="PRs Welcome"/>
  </a>
</p>

<p align="center">
  <b>🚀 Удобный desktop-клиент для загрузки APK-файлов напрямую из Google Play</b><br/>
  Просто, быстро и безопасно. Поддержка русского, украинского и английского языков.<br/>
  <b>🔓 Free • Open Source • Privacy First • Cross-Platform</b>
</p>

---

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="Screenshots/light_theme.png" alt="Light Theme" width="450"/>
        <br/>
        <b>☀️ Light Theme</b>
      </td>
      <td align="center">
        <img src="Screenshots/dark_theme.png" alt="Dark Theme" width="450"/>
        <br/>
        <b>🌙 Dark Theme</b>
      </td>
    </tr>
  </table>
</div>

---

## ⚠️ Official Source Warning

> **🚨 IMPORTANT: This is the ONLY official distribution channel for APK Downloader Pro.**
>
> This application is **only published on GitHub** under this repository:
> **[https://github.com/Maximka1993271/APK-Downloader-Pro](https://github.com/Maximka1993271/APK-Downloader-Pro)**
>
> **I DO NOT upload this application to:**
> - ❌ Any app stores
> - ❌ Telegram
> - ❌ File hosting services
> - ❌ Social media platforms
>
> **If you find this application anywhere else, it is NOT the original version and may contain malware, spyware, or modified code.**
>
> **Always download from the official GitHub repository only!**

---

## ⭐ Project Highlights

- ✅ **Free & Open Source** — MIT License
- ✅ **Cross-Platform** — Windows, Linux, macOS
- ✅ **Direct APK Download** — From Google Play via gplaydl
- ✅ **3 Languages** — Русский, Українська, English
- ✅ **3 Themes** — Light, Dark, System (auto-sync with OS)
- ✅ **Neon Animation** — Modern glowing interface
- ✅ **APK Signature Verification** — Via apksigner (optional)
- ✅ **Settings Persistence** — Saved in user's AppData
- ✅ **Async Download** — Non-blocking interface
- ✅ **No Ads • No Tracking • No Telemetry**
- ✅ **100% Local Processing**

---

## 📱 Подготовка аккаунта для gplaydl (ВАЖНО!)

Для работы программы необходимо авторизовать `gplaydl` с вашим аккаунтом Google. Это делается через официальный сервис аутентификации `gplaydl`.

### Шаг 1: Перейдите на сайт аутентификации gplaydl

Откройте в браузере на компьютере или телефоне:
👉 **[https://dispenser.gplaydl.com/](https://dispenser.gplaydl.com/)**

Это официальный сервис для авторизации `gplaydl`.

### Шаг 2: Войдите в свой аккаунт Google

1. На сайте нажмите **"Sign in with Google"**
2. Выберите аккаунт Google, который хотите использовать
3. Подтвердите вход

### Шаг 3: Получите токен

1. После входа, на странице будет отображен ваш **персональный токен** (длинная строка символов)
2. **Скопируйте этот токен** и сохраните в безопасном месте

> ⚠️ **Важно!** Токен дает доступ к вашему аккаунту через `gplaydl`. Не передавайте его третьим лицам.

### Шаг 4: Привяжите токен в gplaydl

Теперь, когда у вас есть токен, привяжите его к `gplaydl` на вашем компьютере:

```bash
gplaydl link

Во время выполнения команды:

Вас попросят ввести токен — вставьте скопированный токен

Нажмите Enter

После успешной привязки, программа сможет скачивать APK! ✅

🔄 Если нужно обновить токен
Токен может быть отозван или истечь. В этом случае:

Снова зайдите на dispenser.gplaydl.com

Получите новый токен

Выполните gplaydl link и введите новый токен

📋 Полный чек-лист для новичков
Чтобы программа заработала:

□ Установлен Python 3.8+
□ Установлен gplaydl (pip install gplaydl)
□ Зарегистрирован аккаунт Google
□ Получен токен на dispenser.gplaydl.com
□ Выполнена команда gplaydl link с введенным токеном
После выполнения всех пунктов, можете запускать APK Downloader Pro и скачивать приложения! 🚀

🚀 Quick Start
Option 1: Download Ready .exe (Windows)
Go to Releases

Download APK_Downloader_Pro.exe

Run and enjoy! 🎉

Option 2: Run from Source Code
bash
# Clone the repository
git clone https://github.com/Maximka1993271/APK-Downloader-Pro.git
cd APK-Downloader-Pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python apk_downloader.py
📋 Requirements
Python 3.8 or higher

gplaydl for APK downloading:

bash
pip install gplaydl
🔑 Настройка gplaydl (ВАЖНО!)
После установки gplaydl, нужно привязать аккаунт Google:

bash
gplaydl link
Во время выполнения команды:

Введите ваш токен с dispenser.gplaydl.com

Нажмите Enter

После успешной привязки, программа сможет скачивать APK! ✅

🎯 How to Use
1. Вставьте ссылку на приложение из Google Play
text
https://play.google.com/store/apps/details?id=com.example.app
Или просто укажите Package ID: com.example.app

2. Нажмите "📥 Скачать APK"
3. Выберите место сохранения файла
4. Дождитесь завершения загрузки ✅
✨ Features
Feature	Description
📥 APK Download	Direct download from Google Play
🌍 3 Languages	Русский, Українська, English
🎨 3 Themes	Light, Dark, System (auto-sync with OS)
✨ Neon Animation	Modern glowing interface with color cycling
🔒 Signature Check	APK verification via apksigner (optional)
💾 Settings Save	Saved to user's AppData folder
⚡ Async Download	Non-blocking interface
📂 Save Dialog	Choose where to save APK file
⌨️ Context Menu	Copy/Paste/Cut/Clear for URL field
🔗 Package ID Input	Support for direct package ID input
🖥️ Cross-Platform	Windows, Linux, macOS
📊 Progress Bar	Real-time download progress
🐛 v1.2.1 Features
✅ Full localization: Russian, Ukrainian, English

✅ Three themes: Light, Dark, System

✅ Neon animation with color cycling

✅ APK signature verification (via apksigner)

✅ Settings saved to user's AppData folder

✅ Proper error handling and user feedback

✅ Asynchronous download without UI freezing

✅ Context menu for URL field (copy/paste/cut/clear)

✅ Progress bar with real-time updates

✅ GitHub profile link in footer

🔒 Privacy
All processing is performed locally on your machine.
No advertisements, tracking, telemetry, analytics or user data collection.
Your privacy is 100% protected.

📸 Screenshots
<div align="center"> <table> <tr> <td align="center"> <img src="Screenshots/light_theme.png" alt="Light Theme" width="400"/> <br/> <b>☀️ Light Theme</b> </td> <td align="center"> <img src="Screenshots/dark_theme.png" alt="Dark Theme" width="400"/> <br/> <b>🌙 Dark Theme</b> </td> </tr> </table> </div>
⌨️ Keyboard Shortcuts
Shortcut	Action
Enter	Start download (in URL field)
Ctrl+V	Paste from clipboard
Context Menu	Copy/Paste/Cut/Clear
🛠️ Build EXE
bash
# Install PyInstaller
pip install pyinstaller

# Create EXE
pyinstaller --onefile --windowed --name=APK_Downloader_Pro apk_downloader.py

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
  <img src="Screenshots/light_theme.png" alt="APK Downloader Pro Light Theme" width="600"/>
</p>

<p align="center">
  <b>🚀 Удобный desktop-клиент для загрузки APK-файлов напрямую из Google Play</b><br/>
  Просто, быстро и безопасно. Поддержка русского, украинского и английского языков.<br/>
  <b>🔓 Free • Open Source • Privacy First • Cross-Platform</b>
</p>

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

## 📱 Подготовка телефона (ВАЖНО!)

Для работы программы необходимо настроить **gplaydl** с вашим аккаунтом Google.

### Шаг 1: Установите Google Authenticator на телефон

1. Откройте **Play Market** или **App Store** на телефоне
2. Установите приложение **Google Authenticator**:
   - [Ссылка на Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
   - [Ссылка на App Store](https://apps.apple.com/app/google-authenticator/id388497605)

### Шаг 2: Включите двухфакторную аутентификацию (2FA)

1. Откройте браузер на компьютере и перейдите на страницу управления аккаунтом Google:
   - **https://myaccount.google.com/security**
2. В разделе **"Вход в Google"** нажмите **"Двухэтапная аутентификация"**
3. Включите двухэтапную аутентификацию
4. Выберите способ **"Google Authenticator"**
5. Отсканируйте QR-код через приложение на телефоне
6. Введите код из приложения для подтверждения

### Шаг 3: Создайте пароль приложения для gplaydl

1. Перейдите на страницу создания паролей приложений:
   - **https://myaccount.google.com/apppasswords**
2. В поле **"Название"** введите: `gplaydl`
3. Нажмите **"Создать"**
4. **Скопируйте сгенерированный пароль** (выглядит как `xxxx xxxx xxxx xxxx`)
5. Сохраните его в безопасном месте (понадобится для настройки)

---

## 🚀 Quick Start

### Option 1: Download Ready .exe (Windows)

1. Go to [Releases](https://github.com/Maximka1993271/APK-Downloader-Pro/releases)
2. Download `APK_Downloader_Pro.exe`
3. Run and enjoy! 🎉

### Option 2: Run from Source Code

```bash
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

pip install gplaydl

🔑 Настройка gplaydl (ВАЖНО!)
После установки gplaydl, нужно привязать аккаунт Google:
gplaydl link

Во время выполнения команды:

Введите ваш email Google

Введите пароль приложения (который создали на шаге 3)

Если запросит код подтверждения — введите код из Google Authenticator на телефоне

После успешной привязки, программа сможет скачивать APK! ✅

🎯 How to Use
1. Вставьте ссылку на приложение из Google Play

https://play.google.com/store/apps/details?id=com.example.app

Или просто укажите Package ID: com.example.app

2. Нажмите "📥 Скачать APK"
3. Выберите место сохранения файла
4. Дождитесь завершения загрузки ✅

📱 Полная инструкция для новичков
Что нужно для работы?
Телефон с установленным Google Authenticator

Включенная двухфакторная аутентификация в аккаунте Google

Пароль приложения для gplaydl

Установленный Python 3.8+ (если запускаете из исходников)

Пошаговая инструкция:
На телефоне: Установить Google Authenticator

В браузере: Включить 2FA и создать пароль приложения

На компьютере: Установить gplaydl и выполнить gplaydl link

Запустить программу и начать скачивать APK!

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
🤝 How to Contribute
Fork the repository

Create a branch: git checkout -b feature/amazing-feature

Commit: git commit -m 'Add amazing feature'

Push: git push origin feature/amazing-feature

Open a Pull Request

❓ FAQ
Q: Почему gplaydl не найден?
A: Установите: pip install gplaydl

Q: gplaydl выдает ошибку "not linked"?
A: Выполните: gplaydl link и введите данные аккаунта

Q: Что такое пароль приложения и где его взять?
A: Перейдите на https://myaccount.google.com/apppasswords → создайте пароль для gplaydl

Q: Обязательно ли включать 2FA?
A: Да, без двухфакторной аутентификации gplaydl не сможет работать

Q: Безопасно ли это?
A: Да! Пароль приложения работает только для gplaydl и не дает доступа к другим сервисам Google

Q: Как обновить программу?
A: Скачайте новую версию из Releases

Q: Работает ли на macOS/Linux?
A: Да! Просто запустите из исходного кода.

📄 License
Distributed under the MIT License. See LICENSE for details.

👤 Author
Maxim Melnikov

GitHub: @Maximka1993271

⭐ Support
If you like this project, give it a ⭐ on GitHub!

<p align="center"> <b>Made with ❤️</b><br/> <b>Maxim Melnikov</b> — <a href="https://github.com/Maximka1993271">@Maximka1993271</a> </p><p align="center"> <sub>APK Downloader Pro v1.2.1 — 22 August 2026</sub><br/> <sub>🔓 Open Source — fully open source code</sub> </p> ```
📝 Что добавлено:
✅ Раздел "Подготовка телефона" — пошаговая инструкция

✅ Установка Google Authenticator — ссылки на Play Market и App Store

✅ Включение 2FA — подробное руководство

✅ Создание пароля приложения — инструкция со скриншотами

✅ Настройка gplaydl — команда gplaydl link

✅ Полная инструкция для новичков — от начала до конца

✅ Обновленный FAQ — ответы на частые вопросы

💡 Важно!
Пользователям нужно будет:

✅ Установить Google Authenticator на телефон

✅ Включить двухфакторную аутентификацию

✅ Создать пароль приложения

✅ Выполнить gplaydl link

Без этих шагов программа не сможет скачивать APK!

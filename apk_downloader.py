import customtkinter as ctk
import os
import re
import threading
import subprocess
from tkinter import filedialog, Menu, messagebox as msgbox
import webbrowser
import shutil
import colorsys
import json
import time
import tempfile
import sys
import queue
import zipfile
import zlib
import struct
from urllib.parse import urlparse, parse_qs
from enum import Enum, auto

class DownloadStatus(Enum):
    """Статусы операции загрузки"""
    IDLE = auto()
    DOWNLOADING = auto()
    CANCELLING = auto()
    FINISHING = auto()
    SHUTTING_DOWN = auto()

class APKDownloaderApp:
    def __init__(self):
        # Безопасное сохранение настроек в AppData на Windows (или в домашней папке на других ОС)
        if os.name == 'nt':
            app_data = os.getenv('APPDATA')
            config_dir = os.path.join(app_data, "APKDownloaderPro") if app_data else os.path.expanduser("~")
        else:
            config_dir = os.path.expanduser("~")
            
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
            except Exception:
                config_dir = os.path.expanduser("~")
                
        self.config_file = os.path.join(config_dir, "settings.json")
        
        # Переменные по умолчанию
        self.current_lang = "ru"
        self.current_theme = "system"
        self.neon_enabled = True
        
        # Динамический путь к рабочей папке пользователя
        self.download_folder = os.path.join(os.path.expanduser("~"), "Desktop", "apk_downloader")
        
        # Загружаем сохраненные настройки
        self.load_settings()

        # Настройка внешнего вида с учетом загруженной темы
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        
        # Основное окно
        self.window = ctk.CTk()
        self.window.title("📱 APK Downloader Pro")
        self.window.geometry("820x740")
        self.window.minsize(780, 680)
        
        # Переменные состояния
        self.is_gplaydl_installed = False
        self.current_process = None
        self.is_cancelled = False
        self.current_download_path = None
        self.download_thread = None
        self.download_status = DownloadStatus.IDLE
        self.is_shutting_down = False
        self.output_queue = queue.Queue()
        self.final_result = None
        self._last_apk_signature_status = None
        self._finalized = False
        self._operation_id = 0
        self.overwrite_response = None
        self.overwrite_event = threading.Event()
        self._reader_threads = []
        self._reader_lock = threading.Lock()
        self._process_lock = threading.Lock()
        self._shutdown_lock = threading.Lock()
        self._shutdown_started = False
        self._shutdown_deadline = 5.0  # секунд
        
        # Переменные неоновой анимации
        self.hue = 0.0
        self.animation_running = True
        self.is_error_state = False
        self.app_version = "v1.2.1"
        self.github_url = "https://github.com/Maximka1993271"
        
        if not os.path.exists(self.download_folder):
            try:
                os.makedirs(self.download_folder)
            except Exception:
                self.download_folder = os.getcwd()

        # Словари переводов — ПОЛНАЯ ЛОКАЛИЗАЦИЯ EN/RU/UA
        self.translations = {
            "ru": {
                "title": "Скачивание APK",
                "subtitle": "Загружайте приложения из Google Play напрямую",
                "url_label": "Ссылка на приложение:",
                "url_placeholder": "https://play.google.com/store/apps/details?id=...",
                "download_btn": "📥 Скачать APK",
                "cancel_btn": "❌ Отмена",
                "status": "Ожидание действий...",
                "status_waiting": "Ожидание действий...",
                "status_downloading": "Скачивание в процессе...",
                "status_complete": "✅ Успешно завершено!",
                "status_cancelled": "⛔ Загрузка отменена",
                "status_timeout": "⏱️ Превышено время ожидания",
                "status_error": "❌ Ошибка",
                "open_folder": "📂 Открыть папку",
                "clear": "🗑️ Очистить",
                "apk_saved": "💾 Файл сохранен в:",
                "error_invalid_url": "⚠️ Пожалуйста, введите корректную ссылку",
                "error_download": "❌ Ошибка скачивания:",
                "save_as": "Сохранить как",
                "gplaydl_ok": "✅ готов",
                "gplaydl_missing": "❌ gplaydl не найден!",
                "ctx_paste": "Вставить",
                "ctx_copy": "Копировать",
                "ctx_cut": "Вырезать",
                "ctx_clear": "Очистить",
                "msg_warning": "⚠️ Внимание",
                "error_gplaydl_not_linked": "🔗 gplaydl не настроен! Выполните: gplaydl link",
                "error_gplaydl_not_found": "📦 Установите зависимость: pip install gplaydl",
                "theme_system": "Системная",
                "theme_light": "Светлая",
                "theme_dark": "Тёмная",
                "neon_switch": "✨ Неон",
                "version": "📌 Версия: {0}",
                "author": "👤 Автор:",
                "file_exists_title": "Файл существует",
                "file_exists_msg": "Файл {} уже существует.\n\nЗаменить его?",
                "progress_prefix": "⏳ ",
                "saved_prefix": "➜ ",
                "sig_verified_suffix": "  🔒 Подпись проверена (apksigner)"
            },
            "ua": {
                "title": "Завантаження APK",
                "subtitle": "Завантажуйте додатки з Google Play безпосередньо",
                "url_label": "Посилання на додаток:",
                "url_placeholder": "https://play.google.com/store/apps/details?id=...",
                "download_btn": "📥 Завантажити APK",
                "cancel_btn": "❌ Скасувати",
                "status": "Очікування дій...",
                "status_waiting": "Очікування дій...",
                "status_downloading": "Завантаження в процесі...",
                "status_complete": "✅ Успішно завершено!",
                "status_cancelled": "⛔ Завантаження скасовано",
                "status_timeout": "⏱️ Перевищено час очікування",
                "status_error": "❌ Помилка",
                "open_folder": "📂 Відкрити папку",
                "clear": "🗑️ Очистити",
                "apk_saved": "💾 Файл збережено в:",
                "error_invalid_url": "⚠️ Будь ласка, введіть коректне посилання",
                "error_download": "❌ Помилка завантаження:",
                "save_as": "Зберегти як",
                "gplaydl_ok": "✅ готовий",
                "gplaydl_missing": "❌ gplaydl не знайдено!",
                "ctx_paste": "Вставити",
                "ctx_copy": "Копіювати",
                "ctx_cut": "Вирізати",
                "ctx_clear": "Очистити",
                "msg_warning": "⚠️ Увага",
                "error_gplaydl_not_linked": "🔗 gplaydl не налаштовано! Виконайте: gplaydl link",
                "error_gplaydl_not_found": "📦 Встановіть залежність: pip install gplaydl",
                "theme_system": "Системна",
                "theme_light": "Світла",
                "theme_dark": "Темна",
                "neon_switch": "✨ Неон",
                "version": "📌 Версія: {0}",
                "author": "👤 Автор:",
                "file_exists_title": "Файл існує",
                "file_exists_msg": "Файл {} вже існує.\n\nЗамінити його?",
                "progress_prefix": "⏳ ",
                "saved_prefix": "➜ ",
                "sig_verified_suffix": "  🔒 Підпис перевірено (apksigner)"
            },
            "en": {
                "title": "APK Downloader",
                "subtitle": "Download apps directly from Google Play",
                "url_label": "Application Link:",
                "url_placeholder": "https://play.google.com/store/apps/details?id=...",
                "download_btn": "📥 Download APK",
                "cancel_btn": "❌ Cancel",
                "status": "Waiting for action...",
                "status_waiting": "Waiting for action...",
                "status_downloading": "Downloading in progress...",
                "status_complete": "✅ Successfully completed!",
                "status_cancelled": "⛔ Download cancelled",
                "status_timeout": "⏱️ Timeout exceeded",
                "status_error": "❌ Error",
                "open_folder": "📂 Open Folder",
                "clear": "🗑️ Clear",
                "apk_saved": "💾 File saved to:",
                "error_invalid_url": "⚠️ Please enter a valid URL",
                "error_download": "❌ Download error:",
                "save_as": "Save as",
                "gplaydl_ok": "✅ is ready",
                "gplaydl_missing": "❌ gplaydl not found!",
                "ctx_paste": "Paste",
                "ctx_copy": "Copy",
                "ctx_cut": "Cut",
                "ctx_clear": "Clear",
                "msg_warning": "⚠️ Warning",
                "error_gplaydl_not_linked": "🔗 gplaydl is not linked! Run: gplaydl link",
                "error_gplaydl_not_found": "📦 Please install: pip install gplaydl",
                "theme_system": "System",
                "theme_light": "Light",
                "theme_dark": "Dark",
                "neon_switch": "✨ Neon",
                "version": "📌 Version: {0}",
                "author": "👤 Dev:",
                "file_exists_title": "File exists",
                "file_exists_msg": "File {} already exists.\n\nReplace it?",
                "progress_prefix": "⏳ ",
                "saved_prefix": "➜ ",
                "sig_verified_suffix": "  🔒 Signature verified (apksigner)"
            }
        }
        
        self.setup_ui()
        self.check_dependencies_async()
        self.animate_neon()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Запускаем обработчик очереди
        self.start_output_processor()

    def load_settings(self):
        """Загрузка настроек из файла конфигурации.

        Каждое значение валидируется по типу/допустимому множеству перед
        применением: settings.json может быть повреждён, отредактирован
        вручную или содержать устаревший формат, и это не должно приводить
        к падению приложения при старте (например, KeyError в
        self.translations[self.current_lang], если "language" содержит
        произвольную строку/число/None).
        """
        if not os.path.exists(self.config_file):
            return
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                settings = json.load(f)

            if not isinstance(settings, dict):
                raise ValueError("settings.json corrupted: top-level value is not an object")

            lang = settings.get("language", "ru")
            if isinstance(lang, str) and lang in self.translations:
                self.current_lang = lang

            theme = settings.get("theme", "system")
            if isinstance(theme, str) and theme in ("system", "light", "dark"):
                self.current_theme = theme

            neon = settings.get("neon_enabled", True)
            if isinstance(neon, bool):
                self.neon_enabled = neon

            folder = settings.get("download_folder", self.download_folder)
            if isinstance(folder, str) and folder.strip():
                self.download_folder = folder
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")

    def save_settings(self):
        """Атомарное сохранение настроек в безопасную директорию пользователя"""
        settings = {
            "language": self.current_lang,
            "theme": self.current_theme,
            "neon_enabled": self.neon_enabled,
            "download_folder": self.download_folder
        }
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            tmp_file = self.config_file + ".tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_file, self.config_file)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
        
    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))
        
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")
        
        self.title_label = ctk.CTkLabel(
            title_box,
            text=self.translations[self.current_lang]["title"],
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold")
        )
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = ctk.CTkLabel(
            title_box,
            text=self.translations[self.current_lang]["subtitle"],
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=("gray50", "gray60")
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))
        
        settings_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        settings_box.pack(side="right", anchor="n")
        
        # Переключатель языков
        self.lang_var = ctk.StringVar(value=self.current_lang.upper())
        self.lang_selector = ctk.CTkSegmentedButton(
            settings_box,
            values=["EN", "RU", "UA"],
            variable=self.lang_var,
            command=self.change_language,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            selected_color="#00A170",
            selected_hover_color="#007D56",
            unselected_color=("#e2e8f0", "#21262d"),
            unselected_hover_color=("#cbd5e1", "#30363d"),
            text_color=("#1e293b", "#f8fafc"),
            height=34,
            corner_radius=10
        )
        self.lang_selector.pack(side="right", padx=(12, 0))
        
        texts = self.translations[self.current_lang]
        initial_theme_values = [texts["theme_system"], texts["theme_light"], texts["theme_dark"]]
        
        # Меню выбора темы
        self.theme_menu = ctk.CTkOptionMenu(
            settings_box,
            values=initial_theme_values,
            command=self.change_theme,
            width=120,
            height=34,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=("#e2e8f0", "#21262d"),
            button_color=("#cbd5e1", "#30363d"),
            button_hover_color=("#94a3b8", "#484f58"),
            text_color=("#1e293b", "#f8fafc")
        )
        
        if self.current_theme == "light":
            self.theme_menu.set(texts["theme_light"])
        elif self.current_theme == "dark":
            self.theme_menu.set(texts["theme_dark"])
        else:
            self.theme_menu.set(texts["theme_system"])
            
        self.theme_menu.pack(side="right", padx=(12, 0))

        # Переключатель неона (ВКЛ / ВЫКЛ)
        self.neon_var = ctk.BooleanVar(value=self.neon_enabled)
        self.neon_switch = ctk.CTkSwitch(
            settings_box,
            text=texts["neon_switch"],
            variable=self.neon_var,
            command=self.toggle_neon,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            progress_color="#00A170",
            button_color=("white", "#f8fafc"),
            button_hover_color=("#e2e8f0", "#cbd5e1")
        )
        self.neon_switch.pack(side="right")

        input_card = ctk.CTkFrame(
            self.main_container, 
            fg_color=("gray92", "gray14"), 
            corner_radius=20
        )
        input_card.pack(fill="x", pady=(0, 20), ipadx=20, ipady=20)
        
        self.url_label = ctk.CTkLabel(
            input_card,
            text=self.translations[self.current_lang]["url_label"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
        )
        self.url_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        self.neon_outer_frame = ctk.CTkFrame(
            input_card,
            corner_radius=18,
            fg_color="transparent",
            border_width=2,
            border_color="#00FF88"
        )
        self.neon_outer_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.neon_glow_frame = ctk.CTkFrame(
            self.neon_outer_frame,
            corner_radius=15,
            fg_color="transparent",
            border_width=2,
            border_color="#00E5FF"
        )
        self.neon_glow_frame.pack(fill="x", padx=3, pady=3)
        
        self.url_entry = ctk.CTkEntry(
            self.neon_glow_frame,
            placeholder_text=self.translations[self.current_lang]["url_placeholder"],
            height=50,
            corner_radius=12,
            border_width=2,
            border_color="#00FF88",
            fg_color=("white", "#121417"),
            font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        self.url_entry.pack(fill="x", padx=3, pady=3)
        
        # Контекстное меню
        self.context_menu = Menu(self.window, tearoff=0, bg="#2b2b2b", fg="white", font=("Segoe UI", 10))
        self.context_menu.add_command(label=texts["ctx_paste"], command=self.paste_from_clipboard)
        self.context_menu.add_command(label=texts["ctx_copy"], command=self.copy_to_clipboard)
        self.context_menu.add_command(label=texts["ctx_cut"], command=self.cut_to_clipboard)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=texts["ctx_clear"], command=self.clear_url_field)
        
        self.url_entry.bind("<Button-3>", self.show_context_menu)
        self.url_entry.bind("<Control-v>", self.paste_from_clipboard)
        self.url_entry.bind("<Control-V>", self.paste_from_clipboard)
        self.url_entry.bind("<Return>", lambda event: self.start_download()) 
        
        buttons_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 25))
        
        self.download_btn = ctk.CTkButton(
            buttons_frame,
            text=self.translations[self.current_lang]["download_btn"],
            command=self.start_download,
            height=55,
            corner_radius=27,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            fg_color="#00A170", 
            hover_color="#007D56"
        )
        self.download_btn.pack(side="left", padx=(0, 15), expand=True, fill="x")
        
        self.open_folder_btn = ctk.CTkButton(
            buttons_frame,
            text=self.translations[self.current_lang]["open_folder"],
            command=self.open_download_folder,
            height=55,
            corner_radius=27,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color=("gray75", "gray25"),
            text_color=("black", "white"),
            hover_color=("gray65", "gray35")
        )
        self.open_folder_btn.pack(side="left", padx=(0, 15), expand=True, fill="x")
        
        self.clear_btn = ctk.CTkButton(
            buttons_frame,
            text=self.translations[self.current_lang]["clear"],
            command=self.clear_fields,
            height=55,
            corner_radius=27,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color="transparent",
            border_width=2,
            border_color=("#E53935", "#EF5350"),
            text_color=("#E53935", "#EF5350"),
            hover_color=("#FFEBEE", "#3f1d1e")
        )
        self.clear_btn.pack(side="left", expand=True, fill="x")
        
        footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        self.version_label = ctk.CTkLabel(
            footer_frame,
            text=self.translations[self.current_lang]["version"].format(self.app_version),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=("gray50", "gray50")
        )
        self.version_label.pack(side="left")
        
        author_box = ctk.CTkFrame(footer_frame, fg_color="transparent")
        author_box.pack(side="right")
        
        self.author_label = ctk.CTkLabel(
            author_box,
            text=self.translations[self.current_lang]["author"],
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=("gray50", "gray50")
        )
        self.author_label.pack(side="left", padx=(0, 5))
        
        self.github_link = ctk.CTkButton(
            author_box,
            text="Maximka1993271",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="transparent",
            text_color="#00A170",
            hover_color=("gray85", "gray25"),
            height=20,
            width=20,
            command=self.open_github_profile
        )
        self.github_link.pack(side="left")
        
        status_card = ctk.CTkFrame(
            self.main_container,
            fg_color=("gray92", "gray14"),
            corner_radius=20
        )
        status_card.pack(fill="x", side="bottom", ipadx=20, ipady=20)
        
        status_header = ctk.CTkFrame(status_card, fg_color="transparent")
        status_header.pack(fill="x", padx=20, pady=(20, 10))
        
        self.status_label = ctk.CTkLabel(
            status_header,
            text=self.translations[self.current_lang]["status"],
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            anchor="w"
        )
        self.status_label.pack(side="left")
        
        self.gplaydl_status = ctk.CTkLabel(
            status_header,
            text="● Проверка gplaydl...",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#D4A017", "#FFC107") 
        )
        self.gplaydl_status.pack(side="right")
        
        self.progress_bar = ctk.CTkProgressBar(
            status_card, 
            height=8,
            corner_radius=4,
            progress_color="#00A170"
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 15))
        self.progress_bar.set(0)
        
        self.file_info_label = ctk.CTkLabel(
            status_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("gray50", "gray60"),
            anchor="w"
        )
        self.file_info_label.pack(fill="x", padx=20, pady=(0, 20))

    def animate_neon(self):
        if not self.animation_running:
            return

        try:
            if not self.is_error_state:
                if self.neon_enabled:
                    r, g, b = colorsys.hsv_to_rgb(self.hue, 0.9, 1.0)
                    color1 = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

                    r2, g2, b2 = colorsys.hsv_to_rgb((self.hue + 0.12) % 1.0, 0.85, 1.0)
                    color2 = f"#{int(r2 * 255):02x}{int(g2 * 255):02x}{int(b2 * 255):02x}"

                    if self.neon_outer_frame.winfo_exists():
                        self.neon_outer_frame.configure(border_color=color1)
                    if self.neon_glow_frame.winfo_exists():
                        self.neon_glow_frame.configure(border_color=color2)
                    if self.url_entry.winfo_exists():
                        self.url_entry.configure(border_color=color1)

                    self.hue = (self.hue + 0.006) % 1.0
                else:
                    static_color = ("gray75", "gray35")
                    if self.neon_outer_frame.winfo_exists():
                        self.neon_outer_frame.configure(border_color=static_color)
                    if self.neon_glow_frame.winfo_exists():
                        self.neon_glow_frame.configure(border_color=static_color)
                    if self.url_entry.winfo_exists():
                        self.url_entry.configure(border_color=static_color)
        except Exception:
            # Один сбой конфигурации виджета (например, гонка с уничтожением
            # окна) не должен навсегда останавливать цикл анимации — reschedule
            # всё равно происходит ниже, в finally.
            pass
        finally:
            if self.animation_running:
                self._safe_after(30, self.animate_neon)

    def highlight_entry_error(self):
        self.is_error_state = True
        error_color = "#FF1744"
        
        self.neon_outer_frame.configure(border_color=error_color)
        self.neon_glow_frame.configure(border_color="#FF5252")
        self.url_entry.configure(border_color=error_color)
        
        self.window.after(1500, self.reset_error_state)

    def reset_error_state(self):
        self.is_error_state = False

    def toggle_neon(self):
        self.neon_enabled = self.neon_var.get()
        self.save_settings()

    def change_theme(self, selected_value):
        texts = self.translations[self.current_lang]
        if selected_value == texts["theme_light"]:
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
        elif selected_value == texts["theme_dark"]:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
        else:
            ctk.set_appearance_mode("system")
            self.current_theme = "system"
            
        self.save_settings()

    def change_language(self, lang):
        self.current_lang = lang.lower()
        self.update_ui_texts()
        self.save_settings()
            
    def update_ui_texts(self):
        texts = self.translations[self.current_lang]
        
        self.title_label.configure(text=texts["title"])
        self.subtitle_label.configure(text=texts.get("subtitle", ""))
        self.url_label.configure(text=texts["url_label"])
        self.url_entry.configure(placeholder_text=texts["url_placeholder"])
        
        if self.download_status == DownloadStatus.IDLE:
            self.download_btn.configure(text=texts["download_btn"])
        else:
            self.download_btn.configure(text=texts["cancel_btn"])
            
        self.open_folder_btn.configure(text=texts["open_folder"])
        self.clear_btn.configure(text=texts["clear"])
        self.neon_switch.configure(text=texts["neon_switch"])
        
        self.version_label.configure(text=texts["version"].format(self.app_version))
        self.author_label.configure(text=texts["author"])
        
        theme_values = [texts["theme_system"], texts["theme_light"], texts["theme_dark"]]
        self.theme_menu.configure(values=theme_values)
        
        if self.current_theme == "light":
            self.theme_menu.set(texts["theme_light"])
        elif self.current_theme == "dark":
            self.theme_menu.set(texts["theme_dark"])
        else:
            self.theme_menu.set(texts["theme_system"])
        
        # Обновляем статус в зависимости от текущего состояния
        if self.download_status == DownloadStatus.IDLE:
            if self.progress_bar.get() == 1.0:
                self.status_label.configure(text=texts["status_complete"])
            else:
                self.status_label.configure(text=texts["status"])
        elif self.download_status == DownloadStatus.DOWNLOADING:
            self.status_label.configure(text=texts["status_downloading"])
        elif self.download_status == DownloadStatus.CANCELLING:
            self.status_label.configure(text=texts["status_cancelled"])
        else:
            self.status_label.configure(text=texts["status"])
            
        # Обновляем контекстное меню
        self.context_menu.entryconfigure(0, label=texts["ctx_paste"])
        self.context_menu.entryconfigure(1, label=texts["ctx_copy"])
        self.context_menu.entryconfigure(2, label=texts["ctx_cut"])
        self.context_menu.entryconfigure(4, label=texts["ctx_clear"])
        
        self.update_gplaydl_status_ui()

    def check_dependencies_async(self):
        def task():
            try:
                # ИСПРАВЛЕНО: правильная проверка для EXE и скрипта
                if getattr(sys, 'frozen', False):
                    # В EXE режиме проверяем наличие gplaydl.exe
                    gplaydl_path = shutil.which("gplaydl")
                    if not gplaydl_path:
                        exe_dir = os.path.dirname(sys.executable)
                        gplaydl_exe = os.path.join(exe_dir, "gplaydl.exe")
                        if os.path.exists(gplaydl_exe):
                            gplaydl_path = gplaydl_exe
                    self.is_gplaydl_installed = gplaydl_path is not None
                else:
                    # В режиме скрипта проверяем через python -m gplaydl
                    process = subprocess.run(
                        [sys.executable, "-m", "gplaydl", "--version"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                        timeout=5
                    )
                    self.is_gplaydl_installed = (process.returncode == 0)
            except Exception:
                self.is_gplaydl_installed = False
            
            self._safe_after(0, self.update_gplaydl_status_ui)
        
        threading.Thread(target=task, daemon=True).start()

    def update_gplaydl_status_ui(self):
        texts = self.translations[self.current_lang]
        if self.is_gplaydl_installed:
            self.gplaydl_status.configure(text=f"● {texts['gplaydl_ok']}", text_color="#00A170")
        else:
            self.gplaydl_status.configure(text=f"● {texts['gplaydl_missing']}", text_color=("#E53935", "#EF5350"))

    def open_github_profile(self):
        webbrowser.open(self.github_url)
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def paste_from_clipboard(self, event=None):
        try:
            clipboard_text = self.window.clipboard_get()
            self.url_entry.insert(ctk.INSERT, clipboard_text)
            return "break"
        except Exception:
            pass
    
    def copy_to_clipboard(self):
        try:
            selected_text = self.url_entry.get()
            if selected_text:
                self.window.clipboard_clear()
                self.window.clipboard_append(selected_text)
        except Exception:
            pass
    
    def cut_to_clipboard(self):
        try:
            selected_text = self.url_entry.get()
            if selected_text:
                self.window.clipboard_clear()
                self.window.clipboard_append(selected_text)
                self.url_entry.delete(0, 'end')
        except Exception:
            pass
    
    def clear_url_field(self):
        self.url_entry.delete(0, 'end')
    
    def _validate_package_id(self, package_id):
        """Строгая валидация Android Package ID"""
        if not package_id or not isinstance(package_id, str):
            return False
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)+$'
        return bool(re.fullmatch(pattern, package_id))
        
    def extract_app_id(self, url):
        """Извлечение Package ID из URL или прямого ввода"""
        url = url.strip()
        if not url:
            return None
        
        # Проверка на Package ID (без http)
        if self._validate_package_id(url):
            return url
        
        # Строгая проверка hostname
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname.lower() if parsed.hostname else ""
            # Только http(s) и только если hostname точно равен play.google.com
            if parsed.scheme in ("http", "https") and hostname == "play.google.com":
                query_params = parse_qs(parsed.query)
                if 'id' in query_params:
                    package_id = query_params['id'][0]
                    if self._validate_package_id(package_id):
                        return package_id
        except Exception:
            pass
        
        # Безопасный fallback: ищем id в URL только если это точно ссылка на play.google.com
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname.lower() if parsed.hostname else ""
            if parsed.scheme in ("http", "https") and hostname == "play.google.com":
                match = re.search(r'[?&]id=([^&]+)', url)
                if match:
                    package_id = match.group(1)
                    if self._validate_package_id(package_id):
                        return package_id
        except Exception:
            pass
        
        return None

    def start_output_processor(self):
        """Запускает обработчик очереди вывода в GUI потоке"""
        def process_queue():
            try:
                while True:
                    try:
                        output = self.output_queue.get_nowait()
                        if output:
                            self._process_output(output)
                    except queue.Empty:
                        break
            except Exception:
                pass
            if not self.is_shutting_down:
                self.window.after(50, process_queue)
        
        self.window.after(50, process_queue)

    def _process_output(self, output):
        """Обработка вывода gplaydl (безопасно обновляет GUI)"""
        output = output.strip()
        if not output:
            return
        
        texts = self.translations[self.current_lang]
        if "Downloading" in output:
            percent_match = re.search(r'(\d+)%', output)
            if percent_match:
                progress = int(percent_match.group(1)) / 100
                self.progress_bar.set(progress)
            self.status_label.configure(text=f"{texts['progress_prefix']}{output[:100]}")
        elif "Saved" in output or "Saving" in output:
            self.status_label.configure(text=f"{texts['saved_prefix']}{output[:100]}")

    def _read_output_thread(self, pipe, queue_, stdout_buffer, stderr_buffer, is_stderr=False):
        """Читает вывод из pipe и помещает в очередь и буфер"""
        try:
            for line in iter(pipe.readline, ''):
                if line:
                    queue_.put(line)
                    if is_stderr:
                        stderr_buffer.append(line)
                    else:
                        stdout_buffer.append(line)
        except Exception:
            pass
        finally:
            try:
                pipe.close()
            except Exception:
                pass

    def _get_current_process(self):
        """Безопасное получение текущего процесса с блокировкой"""
        with self._process_lock:
            return self.current_process

    def _safe_after(self, delay, func):
        """window.after(), устойчивый к тому, что окно уже уничтожено.

        Worker/reader-потоки маршалят обновления UI через window.after(...).
        Если параллельно идёт shutdown и окно уже задестроено к моменту вызова,
        обычный window.after() кидает исключение прямо в фоновом потоке
        (некритично для процесса — поток daemon, — но даёт "грязный" traceback
        при закрытии и является именно тем сценарием 'callback после destroy',
        который нужно исключать)."""
        try:
            self.window.after(delay, func)
        except Exception:
            pass

    def _terminate_process(self):
        """Безопасное завершение процесса с таймаутом"""
        process = self._get_current_process()
        if process:
            try:
                if process.poll() is None:
                    process.terminate()
                    # Ждем с таймаутом
                    for _ in range(10):
                        if process.poll() is not None:
                            break
                        time.sleep(0.1)
                    if process.poll() is None:
                        process.kill()
                        try:
                            process.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            pass
            except Exception:
                pass

    def _safe_shutdown(self):
        """Безопасное завершение приложения с таймаутом"""
        with self._shutdown_lock:
            if self._shutdown_started:
                return
            self._shutdown_started = True
        
        self.animation_running = False
        self.is_shutting_down = True
        
        # Завершаем процесс — это разблокирует ожидание в download_with_gplaydl
        self._terminate_process()
        
        # Ждём (с ограничением) завершения worker-потока загрузки, ПРЕЖДЕ чем
        # уничтожать окно. Без этого worker мог всё ещё работать в момент
        # destroy() и затем попытаться обратиться к уже уничтоженному окну
        # (см. _safe_after) — окно всё равно будет закрыто вовремя, т.к. join
        # ограничен таймаутом.
        worker = self.download_thread
        if worker and worker.is_alive():
            try:
                worker.join(timeout=2.0)
            except Exception:
                pass
        
        # Завершаем reader threads
        with self._reader_lock:
            for thread in self._reader_threads:
                try:
                    if thread and thread.is_alive():
                        thread.join(timeout=0.5)
                except Exception:
                    pass
            self._reader_threads = []
        
        # Принудительно устанавливаем статус IDLE
        self.download_status = DownloadStatus.IDLE
        self.is_cancelled = True
        self._finalized = True
        
        # Сохраняем настройки
        self.save_settings()
        
        # Закрываем окно
        try:
            self.window.after(0, self.window.destroy)
        except Exception:
            pass

    def _get_gplaydl_command(self, app_id, temp_dir):
        """Возвращает правильную команду для запуска gplaydl"""
        if getattr(sys, 'frozen', False):
            # Режим EXE: используем gplaydl.exe
            gplaydl_path = shutil.which("gplaydl")
            if not gplaydl_path:
                # Пробуем найти в папке с программой
                exe_dir = os.path.dirname(sys.executable)
                gplaydl_exe = os.path.join(exe_dir, "gplaydl.exe")
                if os.path.exists(gplaydl_exe):
                    gplaydl_path = gplaydl_exe
                else:
                    # Пробуем найти в папке Scripts
                    scripts_dir = os.path.join(os.path.dirname(exe_dir), "Scripts")
                    gplaydl_exe = os.path.join(scripts_dir, "gplaydl.exe")
                    if os.path.exists(gplaydl_exe):
                        gplaydl_path = gplaydl_exe
                    else:
                        raise Exception("gplaydl.exe не найден! Установите gplaydl и добавьте в PATH")
            
            return [
                gplaydl_path, "download", app_id,
                "-o", temp_dir,
                "--no-splits",
                "--no-extras"
            ]
        else:
            # Режим Python скрипта: используем python -m gplaydl
            return [
                sys.executable, "-m", "gplaydl", "download", app_id,
                "-o", temp_dir,
                "--no-splits",
                "--no-extras"
            ]

    def _validate_and_select_apk(self, temp_dir):
        """Находит и проверяет скачанный APK во временной директории.

        Проверки:
          - есть хотя бы один файл *.apk с ненулевым размером;
          - это корректный ZIP-архив;
          - в архиве присутствует AndroidManifest.xml;
          - CRC всех записей архива совпадает (zf.testzip()) — обнаруживает
            битую/оборванную загрузку;
          - если ровно один такой файл — он используется как результат;
            если их 0 или больше 1 — операция считается неуспешной.

        ВАЖНО: это структурная проверка ZIP-контейнера, а НЕ проверка
        подлинности/цифровой подписи Android APK. Такая проверка отдельно
        выполняется в _try_verify_apk_signature(), и только если в системе
        реально есть apksigner — в остальных случаях signature_status будет
        'unavailable', и это не должно маскироваться под "проверено".

        Возвращает (apk_path, signature_status).
        """
        apk_files = [f for f in os.listdir(temp_dir) if f.endswith('.apk')]
        if not apk_files:
            raise Exception("APK файл не найден во временной папке")

        valid_apks = []
        for f in apk_files:
            file_path = os.path.join(temp_dir, f)
            if os.path.getsize(file_path) <= 0:
                continue
            try:
                with zipfile.ZipFile(file_path, 'r') as zf:
                    if 'AndroidManifest.xml' not in zf.namelist():
                        continue
                    # Дешёвая проверка заявленного суммарного размера ДО
                    # распаковки (чтение только метаданных central directory,
                    # без декомпрессии) — конкретная, ограниченная защита от
                    # patologически большого/сфабрикованного архива, прежде
                    # чем testzip() ниже реально начнёт разжимать содержимое.
                    declared_size = sum(zi.file_size for zi in zf.infolist())
                    if declared_size > 4 * 1024 * 1024 * 1024:  # 4 GiB, заведомо больше любого реального APK
                        continue
                    # Проверка целостности содержимого (CRC каждой записи).
                    # Выполняется один раз для уже полностью скачанного файла,
                    # поэтому стоимость (декомпрессия) приемлема; это защита
                    # от битой/оборванной загрузки. Источник файла — gplaydl,
                    # аутентифицированный напрямую с Google Play, а не
                    # произвольный недоверенный ввод, поэтому classic
                    # zip-bomb здесь не основная модель угрозы — но верхний
                    # предел размера выше всё равно ограничивает худший случай.
                    if zf.testzip() is not None:
                        continue
            except (zipfile.BadZipFile, OSError, EOFError, zlib.error, struct.error):
                # Любая ошибка чтения/распаковки означает "файл не прошёл
                # валидацию", а не "приложение должно упасть". zipfile может
                # поднять не только BadZipFile (например, zlib.error при
                # повреждённом потоке deflate внутри иначе корректного ZIP,
                # что и показал regression-тест на нарочно испорченном CRC).
                continue
            valid_apks.append(file_path)

        if not valid_apks:
            raise Exception("Все APK файлы повреждены или невалидны")

        if len(valid_apks) != 1:
            raise Exception(f"Ожидался 1 APK файл, найдено {len(valid_apks)}")

        apk_path = valid_apks[0]

        signature_status = self._try_verify_apk_signature(apk_path)
        if signature_status == 'failed':
            # apksigner был найден и явно сообщил, что подпись невалидна —
            # fail-closed: файл отклоняется, а не просто помечается.
            raise Exception(
                "apksigner сообщил, что подпись APK недействительна — файл отклонён"
            )

        return apk_path, signature_status

    def _try_verify_apk_signature(self, apk_path):
        """Необязательная, best-effort проверка подписи APK через системный
        apksigner (Android SDK build-tools), если он есть в PATH.

        Это ЧЕСТНАЯ, ограниченная реализация: apksigner отсутствует на
        подавляющем большинстве пользовательских машин (это отдельный
        инструмент из Android SDK, не устанавливаемый этим приложением и не
        входящий в зависимости gplaydl/customtkinter/Pillow). Поэтому
        результат 'unavailable' — ожидаемый и нормальный исход для типичной
        установки, а не признак поломки.

        Возвращает:
          'verified'    — apksigner подтвердил подпись (returncode == 0);
          'failed'      — apksigner нашёл файл невалидным/неподписанным;
          'unavailable' — apksigner не найден в PATH, проверка не выполнялась;
          'error'       — apksigner найден, но вызов завершился неожиданно
                          (таймаут, отсутствие прав и т.п.); проверка не
                          выполнена, это НЕ равнозначно 'verified' или 'failed'.
        """
        apksigner_path = shutil.which("apksigner")
        if not apksigner_path:
            return 'unavailable'
        try:
            result = subprocess.run(
                [apksigner_path, "verify", apk_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return 'verified' if result.returncode == 0 else 'failed'
        except Exception:
            return 'error'

    def download_with_gplaydl(self, app_id, save_path):
        """Скачивание с безопасным чтением stdout/stderr, подтверждением перезаписи"""
        texts = self.translations[self.current_lang]
        temp_dir = None
        process = None
        stdout_thread = None
        stderr_thread = None
        
        # Буферы для накопления вывода
        stdout_buffer = []
        stderr_buffer = []
        
        try:
            self._safe_after(0, lambda: self.status_label.configure(
                text=f"{texts['status_downloading']} {app_id}..."
            ))
            
            # Проверяем существование файла через GUI поток
            if os.path.exists(save_path):
                self.overwrite_response = None
                self.overwrite_event.clear()
                
                def ask_overwrite():
                    response = msgbox.askyesno(
                        texts["file_exists_title"],
                        texts["file_exists_msg"].format(os.path.basename(save_path))
                    )
                    self.overwrite_response = response
                    self.overwrite_event.set()
                
                self._safe_after(0, ask_overwrite)
                
                # Ждём ответа пользователя, но проверяем shutdown/cancel каждые
                # 0.2с, а не блокируемся на полные 30с — иначе bounded join
                # worker-потока в _safe_shutdown() не успевал бы за разумное
                # время, а Cancel во время open-диалога не отменял бы загрузку
                # немедленно.
                deadline = time.monotonic() + 30
                got_response = False
                while time.monotonic() < deadline:
                    if self.is_shutting_down or self.is_cancelled:
                        break
                    if self.overwrite_event.wait(0.2):
                        got_response = True
                        break
                
                if not got_response:
                    self.is_cancelled = True
                    return False
                
                if not self.overwrite_response:
                    self.is_cancelled = True
                    return False
            
            # Создаем уникальную временную папку (mkdtemp — атомарное создание
            # с гарантией уникальности и безопасными правами доступа, в
            # отличие от предсказания пути через os.path.join + makedirs)
            temp_dir = tempfile.mkdtemp(prefix="apk_download_")
            
            # ИСПРАВЛЕНО: получаем правильную команду для gplaydl
            command = self._get_gplaydl_command(app_id, temp_dir)
            
            # Синхронизированный доступ к current_process
            with self._process_lock:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                self.current_process = process
            
            # Запускаем потоки для чтения stdout и stderr
            stdout_queue = queue.Queue()
            stderr_queue = queue.Queue()
            
            stdout_thread = threading.Thread(
                target=self._read_output_thread,
                args=(process.stdout, stdout_queue, stdout_buffer, stderr_buffer, False),
                daemon=True
            )
            stderr_thread = threading.Thread(
                target=self._read_output_thread,
                args=(process.stderr, stderr_queue, stdout_buffer, stderr_buffer, True),
                daemon=True
            )
            
            stdout_thread.start()
            stderr_thread.start()
            
            with self._reader_lock:
                self._reader_threads = [stdout_thread, stderr_thread]
            
            start_time = time.monotonic()
            timeout = 600  # 10 минут
            
            while True:
                if self.is_shutting_down or self.is_cancelled:
                    break
                
                if time.monotonic() - start_time > timeout:
                    raise TimeoutError("Превышено время ожидания (10 минут)")
                
                try:
                    while True:
                        try:
                            output = stdout_queue.get_nowait()
                            if output:
                                self.output_queue.put(output)
                        except queue.Empty:
                            break
                except Exception:
                    pass
                
                try:
                    while True:
                        try:
                            output = stderr_queue.get_nowait()
                            if output:
                                self.output_queue.put(f"[stderr] {output}")
                        except queue.Empty:
                            break
                except Exception:
                    pass
                
                if process.poll() is not None:
                    break
                
                time.sleep(0.1)
            
            if self.is_shutting_down:
                self._terminate_process()
                return False
            
            if self.is_cancelled:
                self._terminate_process()
                return False
            
            process.wait()
            return_code = process.returncode
            
            # Дожидаемся завершения reader threads
            with self._reader_lock:
                for thread in self._reader_threads:
                    try:
                        if thread and thread.is_alive():
                            thread.join(timeout=1.0)
                    except Exception:
                        pass
            
            # Теперь собираем буферы
            stdout_content = "".join(stdout_buffer)
            stderr_content = "".join(stderr_buffer)
            
            if return_code == 0:
                found_file, apk_signature_status = self._validate_and_select_apk(temp_dir)
                self._last_apk_signature_status = apk_signature_status
                
                # Безопасная замена с защитой старого APK
                try:
                    os.replace(found_file, save_path)
                except OSError:
                    # Fallback с проверками
                    backup_path = save_path + ".backup"
                    
                    # Удаляем старый backup если есть
                    if os.path.exists(backup_path):
                        try:
                            os.remove(backup_path)
                        except Exception:
                            pass
                    
                    # Сохраняем старый файл если есть
                    old_file_saved = False
                    if os.path.exists(save_path):
                        try:
                            shutil.move(save_path, backup_path)
                            old_file_saved = True
                        except Exception:
                            raise Exception("Не удалось создать резервную копию старого APK")
                    
                    # Пытаемся переместить новый файл
                    try:
                        shutil.move(found_file, save_path)
                        # Удаляем backup только если все успешно
                        if old_file_saved and os.path.exists(backup_path):
                            try:
                                os.remove(backup_path)
                            except Exception:
                                pass
                    except Exception as e:
                        # Восстанавливаем старый файл из backup
                        if old_file_saved and os.path.exists(backup_path):
                            try:
                                shutil.move(backup_path, save_path)
                            except Exception:
                                pass
                        raise Exception(f"Ошибка сохранения файла: {e}")
                
                if not os.path.exists(save_path) or os.path.getsize(save_path) == 0:
                    raise Exception("Ошибка сохранения APK файла")
                
                self.download_folder = os.path.dirname(save_path)
                self.save_settings()
                
                return True
            else:
                # Полная диагностика ошибки
                error_parts = []
                error_parts.append(f"gplaydl завершился с кодом {return_code}")
                error_parts.append(f"Команда: {' '.join(command)}")
                
                if stdout_content:
                    error_parts.append(f"\n--- STDOUT ---\n{stdout_content[:500]}")
                if stderr_content:
                    error_parts.append(f"\n--- STDERR ---\n{stderr_content[:500]}")
                
                # Проверяем конкретные известные ошибки
                combined = (stdout_content + stderr_content).lower()
                if "not linked" in combined or "link" in combined:
                    error_parts.append("\n🔗 gplaydl не привязан к аккаунту! Выполните: gplaydl link")
                elif "invalid" in combined or "expired" in combined:
                    error_parts.append("\n🔑 Токен истек или недействителен. Выполните: gplaydl link")
                elif "not found" in combined or "no such" in combined:
                    error_parts.append("\n📦 Приложение не найдено в Google Play")
                elif "timeout" in combined:
                    error_parts.append("\n⏰ Превышено время ожидания ответа от Google Play")
                else:
                    error_parts.append("\n💡 Полный вывод ошибки выше для диагностики")
                
                raise Exception("\n".join(error_parts))
                
        except TimeoutError:
            self._terminate_process()
            raise
        except Exception as e:
            if self.is_cancelled or self.is_shutting_down:
                return False
            raise Exception(str(e)) from e
        finally:
            with self._process_lock:
                self.current_process = None
            # Очистка reader threads
            with self._reader_lock:
                for thread in self._reader_threads:
                    try:
                        if thread and thread.is_alive():
                            thread.join(timeout=0.5)
                    except Exception:
                        pass
                self._reader_threads = []
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass

    def download_complete(self, filepath, operation_id):
        """Финализация SUCCESS с проверкой operation_id и корректным переводом"""
        if self.is_shutting_down:
            return
        if operation_id != self._operation_id:
            return
        if self._finalized:
            return
        self._finalized = True
        self.download_status = DownloadStatus.IDLE
        self.progress_bar.set(1.0)
        
        texts = self.translations[self.current_lang]
        self.status_label.configure(
            text=texts['status_complete'],
            text_color="#00A170"
        )
        info_text = f"{texts['apk_saved']} {os.path.basename(filepath)}"
        if getattr(self, '_last_apk_signature_status', None) == 'verified':
            info_text += texts.get('sig_verified_suffix', '')
        self.file_info_label.configure(text=info_text)
        self.reset_download_button()
        
    def download_timeout(self, operation_id):
        """Финализация TIMEOUT с проверкой operation_id"""
        if self.is_shutting_down:
            return
        if operation_id != self._operation_id:
            return
        if self._finalized:
            return
        self._finalized = True
        self.download_status = DownloadStatus.IDLE
        self.progress_bar.set(0.0)
        
        texts = self.translations[self.current_lang]
        self.status_label.configure(
            text=texts['status_timeout'],
            text_color="#FF9800"
        )
        self.reset_download_button()
        
    def download_error(self, error_msg, operation_id):
        """Финализация FAILED с проверкой operation_id"""
        if self.is_shutting_down:
            return
        if operation_id != self._operation_id:
            return
        if self._finalized:
            return
        self._finalized = True
        self.download_status = DownloadStatus.IDLE
        self.progress_bar.set(0.0)
        
        texts = self.translations[self.current_lang]
        self.status_label.configure(
            text=f"{texts['status_error']}: {error_msg}",
            text_color="#E53935"
        )
        self.reset_download_button()
        
    def download_cancelled(self, operation_id):
        """Финализация CANCELLED с проверкой operation_id"""
        if self.is_shutting_down:
            return
        if operation_id != self._operation_id:
            return
        if self._finalized:
            return
        self._finalized = True
        self.download_status = DownloadStatus.IDLE
        self.progress_bar.set(0.0)
        
        texts = self.translations[self.current_lang]
        self.status_label.configure(
            text=texts["status_cancelled"],
            text_color=("#E53935", "#EF5350")
        )
        self.reset_download_button()
    
    def reset_download_button(self):
        texts = self.translations[self.current_lang]
        self.download_btn.configure(
            text=texts["download_btn"],
            fg_color="#00A170",
            hover_color="#007D56",
            command=self.start_download,
            state="normal"
        )
        self.download_status = DownloadStatus.IDLE
        self.is_cancelled = False
        self._finalized = False
    
    def cancel_download(self):
        self.is_cancelled = True
        if self.download_status == DownloadStatus.DOWNLOADING:
            self.download_status = DownloadStatus.CANCELLING
        process = self._get_current_process()
        if process:
            try:
                process.terminate()
            except Exception:
                pass

    def download_apk(self, app_id):
        if self.is_shutting_down:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".apk",
            filetypes=[("APK files", "*.apk"), ("All files", "*.*")],
            title=self.translations[self.current_lang]["save_as"],
            initialfile=f"{app_id}.apk",
            initialdir=self.download_folder
        )
        
        if not file_path:
            self.is_cancelled = True
            self.download_status = DownloadStatus.IDLE
            self._safe_after(0, lambda: self.download_cancelled(self._operation_id))
            return
        
        self._operation_id += 1
        operation_id = self._operation_id
        save_path = file_path
        
        self.current_download_path = file_path
        self.download_status = DownloadStatus.DOWNLOADING
        self._finalized = False
        self.is_cancelled = False
        
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(app_id, operation_id, save_path),
            daemon=True
        )
        self.download_thread.start()

    def _download_worker(self, app_id, operation_id, save_path):
        """Worker поток для скачивания с operation_id и изолированным save_path"""
        result = {
            'status': 'failed',
            'message': '',
            'path': save_path,
            'operation_id': operation_id
        }
        
        try:
            success = self.download_with_gplaydl(app_id, save_path)
            
            if operation_id != self._operation_id:
                return
            
            if self.is_cancelled or self.is_shutting_down:
                result['status'] = 'cancelled'
            elif success:
                result['status'] = 'success'
            else:
                result['status'] = 'failed'
                result['message'] = self.translations[self.current_lang]["error_download"]
                
        except TimeoutError:
            result['status'] = 'timeout'
            result['message'] = "Timeout exceeded (10 minutes)"
        except Exception as e:
            if operation_id != self._operation_id:
                return
            if not self.is_cancelled and not self.is_shutting_down:
                result['status'] = 'failed'
                result['message'] = str(e)
            else:
                result['status'] = 'cancelled'
        
        def update_ui():
            if self.is_shutting_down:
                return
            
            if operation_id != self._operation_id:
                return
            
            if self._finalized:
                return
            
            if result['status'] == 'success':
                self.download_complete(result['path'], operation_id)
            elif result['status'] == 'cancelled':
                self.download_cancelled(operation_id)
            elif result['status'] == 'timeout':
                self.download_timeout(operation_id)
            else:
                self.download_error(result['message'], operation_id)
            
            self.current_download_path = None
            self.download_status = DownloadStatus.IDLE
        
        self._safe_after(0, update_ui)
    
    def start_download(self):
        if self.download_status != DownloadStatus.IDLE:
            return
        
        if self.is_shutting_down:
            return
        
        if self.download_btn.cget("state") == "disabled":
            return
            
        url = self.url_entry.get().strip()
        texts = self.translations[self.current_lang]
        
        if not url:
            self.highlight_entry_error()
            return
            
        app_id = self.extract_app_id(url)
        if not app_id:
            self.highlight_entry_error()
            return
            
        self.is_cancelled = False
        self.current_download_path = None
        self._finalized = False
        
        self.download_btn.configure(
            text=texts["cancel_btn"],
            fg_color=("#E53935", "#EF5350"),
            hover_color=("#C62828", "#D32F2F"),
            command=self.cancel_download,
            state="normal"
        )
        
        self.status_label.configure(
            text=texts["status_downloading"],
            text_color=("black", "white")
        )
        
        self.progress_bar.set(0.1)
        self.file_info_label.configure(text="")
        
        self.download_apk(app_id)
        
    def open_download_folder(self):
        folder = self.download_folder
        if not os.path.exists(folder):
            folder = os.path.join(os.path.expanduser("~"), "Desktop")
            
        if os.name == 'nt':
            os.startfile(folder)
        else:
            webbrowser.open(folder)
            
    def clear_fields(self):
        self.url_entry.delete(0, 'end')
        self.status_label.configure(
            text=self.translations[self.current_lang]["status"],
            text_color=("black", "white")
        )
        self.progress_bar.set(0)
        self.file_info_label.configure(text="")

    def on_closing(self):
        self._safe_shutdown()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = APKDownloaderApp()
    app.run()
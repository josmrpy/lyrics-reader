import json
import os
import difflib
import urllib.request
import urllib.parse
import urllib.error

import customtkinter as ctk
from PIL import Image, ImageSequence

APP_VERSION = "0.2.2"

# base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")

SONGS_DB = os.path.join(DATA_DIR, "saved_songs.json")
EMOJI_CONFIG = os.path.join(DATA_DIR, "default_emoji.txt")

# * Default emoji GIF and get the name from the config file
EMOJI_NAME = "cray.gif"

os.makedirs(DATA_DIR, exist_ok=True)


def write_default_emoji_config():
    with open(EMOJI_CONFIG, "w", encoding="utf-8") as f:
        f.write(EMOJI_NAME + "\n")


try:  # check if the emoji config file exists nor is empty
    with open(EMOJI_CONFIG, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()

        if first_line:
            EMOJI_NAME = first_line
        else:
            raise ValueError("Empty emoji config file")
except (FileNotFoundError, ValueError):
    write_default_emoji_config()


EMOJI_GIF = os.path.join(ASSETS_DIR, EMOJI_NAME)

# Constants for GUI
GIF_ANIM_INTERVAL = 100
GIF_SIZE = (62, 44)
SAMPLE_SIZE = 32

WINDOW_WIDTH = 340
WINDOW_HEIGHT = 160
TRANSPARENT_COLOR = "#ff00ff"


def load_database():
    if not os.path.exists(SONGS_DB):
        return {}
    try:
        with open(SONGS_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_database(db, title, artist, lyrics):
    db[title] = {"artist": artist, "lyrics": lyrics}
    try:
        with open(SONGS_DB, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def search_database(db, name):
    if not db:
        return None
    word_matches = difflib.get_close_matches(
        name.lower(), [t.lower() for t in db], n=1, cutoff=0.6
    )
    return (
        next((t for t in db if t.lower() == word_matches[0]), None)
        if word_matches
        else None
    )


# * Search lyrics from LRCLIB API // main feature
# TODO: Add more sources for lyrics search
def search_on_lrclib(song_name) -> tuple[str | None, str | None, str | None]:
    try:
        url = f"https://lrclib.net/api/search?q={urllib.parse.quote(song_name)}"
        request = urllib.request.Request(
            url, headers={"User-Agent": "LyricsSearcher/1.0 (personal use)"}
        )
        with urllib.request.urlopen(request, timeout=8) as resp:
            results = json.loads(resp.read().decode("utf-8"))

        for result in results or []:
            lyrics = (result.get("plainLyrics") or "").strip()

            if lyrics:
                track_name = result.get("trackName") or song_name
                artist_name = result.get("artistName") or ""
                return track_name, artist_name, lyrics
        return None, None, None

    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return None, None, None


def split_into_verses(lyrics):
    lines = [
        l.strip() for l in lyrics.replace("\r\n", "\n").strip().split("\n") if l.strip()
    ]
    return lines or ["(letra vacía)"]


def load_gif_frames(path, size):
    if not os.path.exists(path):
        return []
    try:
        with Image.open(path) as imagen:
            return [
                c.convert("RGBA").resize(size) for c in ImageSequence.Iterator(imagen)
            ]
    except Exception:
        return []


def create_gif_frames(frames, size):
    return [ctk.CTkImage(light_image=f, dark_image=f, size=size) for f in frames]


# * Lyrics Windows Class // main gui window
class LyricsWindows(ctk.CTkToplevel):
    def __init__(self, master, title, verses, gif_frames):  # @josmr.py
        super().__init__(master)

        self.title = title
        self.verses = verses
        self.index = 0
        self.gif_frames = gif_frames
        self.gif_index = 0
        self.animation_id = None

        self.overrideredirect(True)
        x = (self.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        self.resizable(False, False)

        self.configure(fg_color=TRANSPARENT_COLOR)
        try:
            self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        except Exception:
            pass

        self.build_interface()

        self.bind("<space>", self.handle_ok)
        self.bind("<Return>", self.handle_ok)
        self.bind("<Left>", self.handle_previous)
        self.bind("<Escape>", self.close)

        self.lift()
        self.attributes("-topmost", True)
        self.after(50, self.force_focus)

    def force_focus(self):
        self.focus_force()
        self.ok_button.focus_set()

    def build_interface(self):
        self.card = ctk.CTkFrame(
            self,
            corner_radius=14,
            fg_color="#f5f6f7",
            border_width=1,
            border_color="#d0d4d8",
        )
        self.card.pack(expand=True, fill="both", padx=1, pady=1)

        bar_frame = ctk.CTkFrame(self.card, fg_color="transparent", height=24)
        bar_frame.pack(fill="x", padx=14, pady=(10, 0))

        close_button = ctk.CTkButton(
            bar_frame,
            text="✕",
            width=18,
            height=18,
            corner_radius=0,
            fg_color="transparent",
            hover_color="#e0e0e0",
            text_color="#888888",
            font=("Arial", 12),
            command=self.close,
        )
        close_button.pack(side="right")

        self.title_label = ctk.CTkLabel(
            bar_frame,
            text=self.title.lower(),
            font=("Consolas", 12),
            text_color="#555555",
        )
        self.title_label.pack(side="left")

        for widget in (bar_frame, self.title_label):
            widget.bind("<ButtonPress-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.drag)

        content = ctk.CTkFrame(self.card, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=16, pady=(0, 2))

        self.gif_label = ctk.CTkLabel(content, text="")
        self.gif_label.pack(side="left", padx=(0, 10))

        self.verse_label = ctk.CTkLabel(
            content,
            text=self.verses[self.index],
            font=("Georgia", 13),
            wraplength=210,
            justify="left",
            anchor="w",
            text_color="#2b2b2b",
            padx=10,
        )
        self.verse_label.pack(side="left", expand=True, fill="both")

        self.ok_button = ctk.CTkButton(
            self.card,
            text=self.get_button_text(),
            width=50,
            height=28,
            corner_radius=0,
            fg_color="#e8eeee",
            hover_color="#dbe4e6",
            text_color="#384850",
            border_width=2,
            border_color="#688a96",
            font=("Segoe UI", 11),
            command=self.handle_ok,
        )
        self.ok_button.pack(pady=(0, 14))

        if self.gif_frames:
            self.animate_gif()
        else:
            print(f"! No se pudo cargar el GIF del emoji '{EMOJI_NAME}'")
            self.gif_label.configure(text=":)", font=("Segoe UI Emoji", SAMPLE_SIZE))

    def get_button_text(self):
        return "Cerrar" if self.index == len(self.verses) - 1 else "OK"

    def start_drag(self, event):
        self.x_offset = event.x_root - self.winfo_x()
        self.y_offset = event.y_root - self.winfo_y()

    def drag(self, event):
        self.geometry(f"+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}")

    def animate_gif(self):
        self.gif_label.configure(image=self.gif_frames[self.gif_index])
        self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
        self.animation_id = self.after(GIF_ANIM_INTERVAL, self.animate_gif)

    def handle_ok(self, event=None):
        if self.index == len(self.verses) - 1:
            self.close()
            return
        self.index += 1
        self.verse_label.configure(text=self.verses[self.index])
        self.ok_button.configure(text=self.get_button_text())

    def handle_previous(self, event=None):
        if self.index > 0:
            self.index -= 1
            self.verse_label.configure(text=self.verses[self.index])
            self.ok_button.configure(text=self.get_button_text())

    def close(self, event=None):
        if self.animation_id is not None:
            self.after_cancel(self.animation_id)
        self.master.destroy()


def search_from_terminal() -> tuple[str | None, str | None]:
    song_name = input("Escribe el nombre de la canción: ").strip()

    if not song_name:
        print("No escribiste ningún nombre.")
        return None, None

    local_database = load_database()

    print("Buscando en la base local...")
    local_title = search_database(local_database, song_name)
    if local_title:
        datos = local_database[local_title]
        print(f"Encontrada en local: {local_title} — {datos['artist']}")
        return local_title, datos["lyrics"]

    print("No está en local, buscando en internet (LRCLIB)...")
    title, artist, lyrics = search_on_lrclib(song_name)
    if not lyrics:
        print("No se encontró la letra de esa canción.")
        return None, None

    print(f"Encontrada en internet: {title} — {artist}")
    save_database(local_database, title, artist, lyrics)
    return title, lyrics


def main():
    print(f"=== Buscador de letras v{APP_VERSION} ===")
    print("Made by Josimar M. (@josmr.py)\n")
    title, lyrics = search_from_terminal()
    if not lyrics:
        return

    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.withdraw()

    loaded_frames = load_gif_frames(EMOJI_GIF, GIF_SIZE)
    gif_frames = create_gif_frames(loaded_frames, GIF_SIZE)

    LyricsWindows(root, title, split_into_verses(lyrics), gif_frames)
    root.mainloop()


if __name__ == "__main__":
    main()

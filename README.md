# Lyrics Reader

Lyrics Reader is a small Python desktop utility for finding and reading song lyrics one verse at a time.

This project is part of my personal portfolio, where I document and showcase projects I build while learning and experimenting with software development.

It searches a local JSON cache first and uses the [LRCLIB API](https://lrclib.net/) when a song is not already saved locally.

## Features

* Search for a song by title from a simple terminal prompt.
* Reuse previously found lyrics without making another network request.
* Read lyrics in a compact, always-on-top desktop window.
* Move forward with `OK`, `Enter`, or `Space`.
* Return to the previous verse with `Left Arrow`.
* Supports Spanish and other Unicode lyrics.
* Uses the included `emoji.gif` animation when available, with a fallback emoji when it is not.

## Requirements

* Windows is recommended because the reader uses a Windows-style transparent window color.
* Python 3 with `pip`.
* Internet access for songs that are not already in the local cache.

Install the required packages:

```powershell
python -m pip install customtkinter Pillow
```

The remaining imports come from Python's standard library.

## Getting started

Clone the repository and enter its directory:

```powershell
git clone https://github.com/josmrpy/lyrics-reader.git
cd lyrics-reader
```

Install the dependencies and start the application:

```powershell
python -m pip install customtkinter Pillow
python main.py
```

When prompted, enter a song title:

```text
=== Buscador de letras v0.1.0 ===

Made by Josimar M. (@josmr.py)

Escribe el nombre de la canción: Intruso
```

If the song exists in `saved_songs.json`, Lyrics Reader uses that entry. Otherwise, it queries LRCLIB, displays the result, and saves it to `saved_songs.json` for later searches.

The included `emoji.gif` is loaded automatically when it is in the same directory as `main.py`.

## Reading controls

| Action                       | Control                   |
| ---------------------------- | ------------------------- |
| Advance to the next verse    | `OK`, `Enter`, or `Space` |
| Return to the previous verse | `Left Arrow`              |
| Close the reader             | `Escape` or `Cerrar`      |
| Move the reader window       | Drag its title area       |

## Project files

```text
main.py          Application code
saved_songs.json Local lyrics cache
emoji.gif        Optional animated reader asset
```

## About this project

Lyrics Reader is a personal project created to experiment with Python, desktop interfaces, API integration, local data storage, and keyboard-based interaction.

More projects and experiments can be found on my portfolio:

<https://josmrpy.github.io/>

## License

This repository is primarily intended to showcase my work and development process. It does not currently include a separate open-source license.

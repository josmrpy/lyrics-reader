# Lyrics Reader

![Version](https://img.shields.io/badge/version-0.2.3-3776AB)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python\&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success)

<p align="center">
  <img src="assets/music.gif" width="80">
</p>

Lyrics Reader is a small Python desktop utility for finding and reading song lyrics one line at a time.

This project is part of my personal portfolio, where I document and showcase projects I build while learning and experimenting with software development.

It searches a local JSON cache first and uses the [LRCLIB API](https://lrclib.net/) when a song is not already saved locally.

## Features

<p align="right">
  <img src="assets/search.gif" width="72">
</p>

* Search for a song by title from a simple terminal prompt.
* Reuse previously found lyrics without making another network request.
* Read lyrics in a compact, always-on-top desktop window.
* Move forward with `OK`, `Enter`, or `Space`.
* Return to the previous verse with `Left Arrow`.
* Supports Spanish, English and other Unicode lyrics.
* Uses a configurable animated GIF from `assets/`, with a fallback emoji when it is not available.

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

<p align="right">
  <img src="assets/download.gif" width="56">
</p>

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
=== Buscador de letras v0.2.0 ===
Made by Josimar M. (@josmr.py)

Escribe el nombre de la canción: Intruso
```

If the song exists in `data/saved_songs.json`, Lyrics Reader uses that entry. Otherwise, it queries LRCLIB, displays the result, and saves it to the local cache for later searches.

The GIF filename is read from `data/default_emoji.txt`. The default value is `cray.gif`, which is loaded from `assets/`. You can edit this file to choose any other GIF included in the assets folder.

To use another included animation, replace the filename in `data/default_emoji.txt`, for example:

```text
music.gif
```

The complete emoji catalog, including previews and filenames, is available in [`assets.md`](assets.md).

## Reading controls

<p align="right">
  <img src="assets/read.gif" width="56">
</p>

| Action                       | Control                   |
| ---------------------------- | ------------------------- |
| Advance to the next verse    | `OK`, `Enter`, or `Space` |
| Return to the previous verse | `Left Arrow`              |
| Close the reader             | `Escape` or `Cerrar`      |
| Move the reader window       | Drag its title area       |

## Project files

```text
main.py                  Application code
  assets/                  Animated GIF assets
  assets.md                Emoji catalog, configuration notes, and credits
data/default_emoji.txt   GIF filename used by the reader
data/saved_songs.json    Local lyrics cache
```

## About this project

<p align="right">
  <img src="assets/scaut.gif" width="72">
</p>

Lyrics Reader is a personal project created to experiment with Python, desktop interfaces, API integration, local data storage, and keyboard-based interaction.

More projects and experiments can be found on my portfolio:

<https://josmrpy.github.io/>

## Credits

<p align="right">
  <img src="assets/thank_you2.gif" width="72">
</p>

The animated GIF emojis included in this project were obtained from the SmileyPak collection by Kolobanga.

Source: <https://kolobanga.ru/en/smileypak>

## License

This repository is primarily intended to showcase my work and development process. It does not currently include a separate open-source license.

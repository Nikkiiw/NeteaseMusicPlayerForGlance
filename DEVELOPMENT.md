# Development & Maintenance Guide

This document explains the internal logic and file structure of the NetEase Music Daily Recommend Player project.

## 📁 File Structure

| File | Location | Description |
| :--- | :--- | :--- |
| `add_songs.py` | `Scripts/` | Adds songs from `song_ids.txt` to the playlist specified in `playlist_id.txt`. |
| `creat_list.py` | `Scripts/` | Creates a new playlist named "daily" and saves its ID to `playlist_id.txt`. |
| `del_list.py` | `Scripts/` | Deletes the playlist ID stored in `playlist_id.txt`. |
| `song_ids.py` | `Scripts/` | Fetches daily recommendation songs and saves their IDs to `song_ids.txt`. |
| `api.txt` | `Scripts/` | Configuration: Base URL of the NetEase Cloud Music API. |
| `cookie.txt` | `Scripts/` | Configuration: `MUSIC_U` cookie for authentication. |
| `playlist_id.txt` | `Scripts/` | State: Stores the currently active playlist ID. |
| `song_ids.txt` | `Scripts/` | State: Stores the list of song IDs to be added. |
| `netmusic.html` | `Player/` | The web interface for the player. |
| `background.js` | `ChromeExtension/` | Service worker for the Chrome extension. |

## ⚙️ Script Logic (in `Scripts/`)

### `add_songs.py`
- Reads `playlist_id.txt`, `cookie.txt`, `api.txt`, and `song_ids.txt`.
- **Note**: It reverses the song list (`song_ids.reverse()`) before adding them, so the first recommended song appears at the top of the playlist (since adding songs usually pushes them to the top).
- Uses a 0.5s delay between requests to avoid rate limiting.

### `song_ids.py`
- Fetches songs from `/recommend/songs`.
- Extracts `id` from the `dailySongs` array in the API response.

### `creat_list.py` / `del_list.py`
- Handles the lifecycle of the "daily" playlist.
- These scripts ensure that you have a fresh playlist every day instead of just appending to an old one.

## 🛠️ Troubleshooting

### API Issues
If the scripts fail, check if your self-hosted API is running and accessible. You can test it by visiting `http://<your-api-url>/status`.

### Cookie Expiration
If you get "Login required" errors, your `MUSIC_U` cookie might have expired. Follow the instructions in the README to get a new one and update `Scripts/cookie.txt`.

### Web Player Not Loading
- Check the browser console (F12) for errors.
- Ensure `Scripts/playlist_id.txt` is being correctly fetched.
- Verify that `netease-mini-player-v2.js` and `netease-mini-player-v2.css` are in the same directory as `netmusic.html` (inside `Player/`).

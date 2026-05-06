Project: Jumper (2D platformer)

Refactor plan:
- Move game logic into `src/` with `main.py` as entrypoint.
- Centralize constants in `src/settings.py` and asset loading in `src/assets.py`.
- Move entities into `src/entities/` and UI into `src/ui/`.

Audio notes:
- Prefer OGG/WAV for cross-platform compatibility with SDL_mixer.

To run (current state uses original `jumper.py`):

```bash
python3 jumper.py
```

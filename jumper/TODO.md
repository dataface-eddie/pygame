# Project TODO

This is an actionable checklist for agents to pick tasks off and implement.

- [x] Plan sound effects integration — determine where SFX are needed (jump, coins, death, fireballs).
- [x] Add sound effect assets — place `.wav`/`.mp3` files in `assets/audio/`.
- [x] Integrate sound library — initialize `pygame.mixer` and centralize loading.
- [x] Implement sound effects in code — play SFX for jump, coin, death, fireballs.
- [x] Test sound effects — run the game and verify SFX playback.
- [x] Add sound for coin collection.
- [x] Add death-by-fireball sound.
- [x] Create `src/` skeleton and migrate code into `src/`.
- [x] Migrate platforms and coins into `src/world.py`.
- [x] Migrate `Player` into `src/entities/player.py`.
- [x] Migrate `Fireball` into `src/entities/fireball.py`.
- [ ] Migrate `Enemy` into `src/entities/enemy.py` and integrate.
- [x] Create `src/main.py` entrypoint.
- [ ] Add tests & CI (pytest).
- [x] Centralize assets in `src/assets.py`.
- [x] Convert MP3s to OGG/WAV and archive incompatible `.ogg` files.
- [x] Add character selection menu for `Charles`/`Carlisle`.

## New feature items (priority)

- [ ] Add Boss Enemy at end of level — design boss entity, AI, and attacks.
- [ ] Build Level Complete screen — show when boss is defeated, with stats and continue.
- [ ] Boss hit mechanics — boss requires 5 hits; flash effect + hit SFX on each hit.
- [ ] Start a second level — implement new level layout and transition after boss defeat.

## Optional / future

- [ ] Add mute/volume controls and HUD slider.
- [ ] Persist player character choice to a settings file.
- [ ] Add unit tests for `AssetManager` and entity collision.
- [ ] Add small CI pipeline to run tests on push.

--
Edit this file to reprioritize or add implementation notes for each task.

# DeFlock

A game about how rules become cages.

You write the sacred text of a new religion. Every verse is a
constraint. Every constraint binds you. Survive a year without your
own scripture destroying you — or your followers discovering that
you were the biggest heretic in it.

## Status: Slice 1

Runnable APK. Campaign auto-starts, turn 1 renders, options
resolve, event log populates, scenes cycle across all 12
archetypes. No drift, no doctrines, no factions yet — those land
in later slices.

## Layout

    src/deflock/
      app.py              Kivy App entrypoint
      engine/
        state.py          Campaign, Follower dataclasses
        scenes.py         12 scene archetypes + deterministic pick
        turn.py           resolve(campaign, action) -> (campaign, events)
      screens/
        main.py           the only Kivy screen so far
      assets/             placeholder icon and presplash

## Run

Local:

    uv sync
    uv run python -m deflock

Android build (CI or local):

    uv run ksproject android build debug --clean

The APK lands in `project_dist/gradle/app/build/outputs/apk/debug/`.

## Notes

- Placeholder assets: `deflock_icon.png` and `presplash.png` are
  solid `#0f0a07` squares. Replace before shipping.
- `uv.lock` is not committed yet. Run `uv sync` once, then commit
  the generated lock for reproducible builds.

# Python utilities for Table Top Simulator (TTS)

This repo has Python utilities to help create games to
[TTS](https://www.tabletopsimulator.com/).
Now this repo includes just exporting images of a card game to TTS deck template.
You need to import the deck template to a TTS game:
[documentation](https://kb.tabletopsimulator.com/custom-content/custom-deck/).

## Install

```
pip install git+https://github.com/jukujala/tts-utils
```

## How: generate TTS deck template

```
python -m tts_utils.create_tts_deck \
    --input <input path> \
    --back <card back image> \
    --output <output path>
```

- `<input path>` has card images in separate files.
- `<card back image>` is a single file.

Example with test data included in this repository:

```
python -m tts_utils.create_tts_deck \
    --input tests/data/card_images \
    --back tests/data/card_back.png \
    --output tests/data/deck_templates/
```

# Wizard Eldrin's Cognitive Tasks

A pair of Pygame-based cognitive tasks built for PSY 475 (Fall 2024).

## Games

### Game 1 — Lost Items (`game_1.py`)

A **response inhibition and spatial congruency** task. Colored items appear on the left or right side of the screen:

- **Red item** — press `F`
- **Blue item** — press `J`
- **Green item** — do not press any key (inhibit response)

The game includes 3 practice trials followed by 10 test trials. Participants must respond within a brief time window. Performance is scored by correct responses and reaction time.

### Game 2 — Wizard's Test (`game_2.py`)

A **dual-task** paradigm combining digit counting with task switching. On each trial:

1. A target digit (1–4) is shown alongside two rows of colored digits.
2. Participants count how many times the target digit appears **in black**.
3. A color cue (BLUE or RED) determines the response format:
   - **BLUE** — type the numeric answer directly
   - **RED** — type the corresponding letter key (`1→Q`, `2→W`, `3→E`, `4→R`)

10 trials are presented with a 3-second time limit each. A score above 7 is required to proceed.

## Requirements

- Python 3
- Pygame (`pip install pygame`)

## Running

```bash
python game_1.py   # Launch Game 1
python game_2.py   # Launch Game 2
```

## Assets

All image assets live in the `assets/` directory:

| Asset | Used by |
|---|---|
| `assets/background_image.JPG` | Both games |
| `assets/game1_intro.jpg` / `assets/game1_end.jpg` | Game 1 |
| `assets/success.jpg` / `assets/failure.png` | Game 2 |
| `assets/red/`, `assets/blue/`, `assets/green/` (each with `1.png`–`10.png`) | Game 1 |

## Project Structure

```
├── game_1.py              # Game 1: Response inhibition task
├── game_2.py              # Game 2: Dual-task paradigm
├── requirements.txt
├── assets/                # Images and sprites
├── docs/                  # Project documents and instructions
│   ├── inst_game_2.pdf
│   ├── instructions.docx
│   └── puzzle_summaries.pdf
└── recordings/            # Gameplay recordings
    ├── game_2_recording.mov
    └── puzzle1_gameplay.mov
```

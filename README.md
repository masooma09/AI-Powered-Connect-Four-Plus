# Connect Four AI with Fog of War & Genetic Strategy 📊🧠

An AI-enhanced version of the classic Connect Four game built in Python using Pygame. Featuring multiple AI difficulty levels, an innovative Fog of War mode, and offline-trained Genetic AI strategies that help players consistently beat the AI when followed manually.

---

## 👥 Team Members
- Masooma Hassan – 22K4749  
- Muhammad Haris – 22K4752  
- Muhammad Abdullah – 22K4712

---

## 🧠 Overview

This project blends strategic gameplay with AI-powered logic. It supports human and AI gameplay, five AI difficulty levels using the Minimax algorithm, and a Fog of War mode that increases difficulty by hiding opponent moves.

Additionally, we created a Genetic Algorithm trainer (in `genetic.py`) that evolves a sequence of moves offline. These move sequences are then used by human players in actual games to achieve consistently strong performance against the AI.

---

## 🚀 Features

- 🎮 **Game Modes**:
  - Player vs Player
  - Player vs AI (5 difficulty levels)
  - AI vs AI
  - Fog of War (PvAI)

- 🧠 **AI Mechanics**:
  - Minimax with Alpha-Beta pruning
  - Heuristics for evaluating game states (center control, threats, blocks)
  - Adjustable difficulty: Easy to Godmode

- 🧬 **Genetic Strategy Trainer**:
  - Evolves strong move sequences over 500 generations
  - Not used in real-time gameplay, but assists players with optimal moves
  - Helps players consistently beat the AI if followed correctly

- 🎨 **User Interface**:
  - Pygame UI with restart/quit buttons
  - Sound effects and visual feedback
  - Custom fonts and dark theme aesthetics

---

## 📂 Folder Structure

```
├── assets/
│   ├── fonts/
│   └── sound/
├── src/
│   ├── game.py
│   ├── functions.py
│   ├── minmax_ai.py
│   ├── score_ai.py
│   ├── genetic.py
│   ├── ui_components.py
│   └── variables.py
├── PROJECT PROPOSAL AI.docx
├── Project_Report_Revised.docx
├── demo_video.mp4
└── README.md
```

---

## ▶️ How to Run

1. Install dependencies:
```bash
pip install pygame numpy
```

2. Start the game:
```bash
python src/game.py
```

To experiment with genetic strategy evolution:
```bash
python src/genetic.py
```

---

## 🎥 Demo Video

📺 [Watch Here](https://youtu.be/EDhE7eQHNw4?si=dJG43iuR7Rx_AyvO) 
🎙️ Shows gameplay across all modes, including Fog of War and AI vs AI.

---

## 📅 Submission Details

- **Course**: Artificial Intelligence  
- **Instructor**: Miss Mehak Mazhar  
- **Deadline**: 11th May 2025  

---

## 🙌 Acknowledgements

Thanks to our instructor and my all team members for their guidance. This project helped us explore both theoretical and applied AI in a creative, engaging way.
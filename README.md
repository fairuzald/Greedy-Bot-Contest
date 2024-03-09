# Tugas Besar IF2211 Strategi Algoritma Team Alucard

## Table of Contents

- [Tugas Besar IF2211 Strategi Algoritma Team Alucard](#tugas-besar-if2211-strategi-algoritma-team-alucard)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Algorithm Description](#algorithm-description)
  - [Program Requirements](#program-requirements)
  - [Running the Program](#running-the-program)
  - [Authors](#authors)

## Project Description

This project is an Algorithm Strategies Project that implements a bot using the Greedy Algorithm as the backbone of the decision making algorithm. The basic for this project is an understanding in Object-Oriented Programming, The Greedy Algorithm, Algorithm Design and Analysis. The bot to be implemented is a bot from The Etimo Diamonds 2 Challenge game, where it an be classified as a battle-royale.

The full game description can be read [here](https://github.com/Etimo/diamonds2/blob/main/RULES.md)

Starter pack can be downloaded [here](https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1)

Game engine can be downloaded [here](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)

## Algorithm Description

The base algorithm used in this project is the greedy algorithm, which offers various alternatives such as greedy by nearest distance, safest position, etc. Our team opted for the greedy by priority action approach, allowing us to choose greedy approaches based on the features we want to prioritize at any given time, and set the goal position using the main greedy algorithm.

The objective of this game is to collect as many diamonds as possible while keeping them stored in the inventory. To achieve this objective, we need to maximize our choices of heading and actions to take. The greedy strategy devised involves searching for diamonds closest to the base while considering the best clusters based on pre-defined time constraints.

In essence, the greedy algorithm selects the best possible solution available at a particular moment, or in other words, the local maximum at that instance. Consequently, in certain scenarios, the greedy algorithm can approximate the global maximum using the local maximum.


Our description of the algorithm is [here](https://youtu.be/9MXRM4zggRI?si=zADk3sNxqKR4i7D)

## Program Requirements

* Python version 3.12

## Running the Program
1. Clone repository [here](https://github.com/fairuzald/Tubes1_Alucard/)
2. Move src
```cd src```
3. Install dependencies using pip
```pip install -r requirements.txt```
4. Run
To run a single bot (in this example, we are running one bot with the logic contained in the file game/logic/random.py):
```python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo```
To run multiple bots simultaneously (in this example, we are running 4 bots with the same logic, which is game/logic/alucard.py):
```
Untuk windows
```./run-bots.bat```

Untuk Linux / (possibly) macOS
```./run-bots.sh```
```

## Authors

| NIM      | Name                       |
| -------- | -------------------------- |
| 13522015 | Yusuf Ardian Sandi         |
| 13522075 | Moh Fairuz Alauddin Yahya  |
| 13522095 | Rayhan Fadhlan Azka        |
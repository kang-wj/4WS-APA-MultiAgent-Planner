# 4WS-APA-MultiAgent-Planner

An intelligent automated parking planning system designed for Four-Wheel Steering (4WS) vehicles, driven by a Multi-Agent architecture combining Heuristic Search and Reinforcement Learning (PPO).

## 🚀 Key Features & Core Logic

This project solves the high computational cost and poor trajectory smoothness of traditional parking algorithms (like Hybrid A*) in narrow spaces for 4WS vehicles. It utilizes a Multi-Agent workflow:

1. **Search Agent:** Uses long-chain spatial reasoning based on modified A* to generate a collision-free coarse path.
2. **RL Agent (PPO):** Acts as a local planner. It takes the coarse path and outputs precise front/rear steering angles leveraging 4WS kinematics (e.g., Crab Walk, Zero-Radius Turn) for smooth trajectory generation.
3. **Simulation Agent:** Automates the closed-loop validation by interacting with CarSim and Simulink APIs.

## 🛠️ Installation

```bash
git clone [https://github.com/yourusername/4WS-APA-MultiAgent-Planner.git](https://github.com/yourusername/4WS-APA-MultiAgent-Planner.git)
cd 4WS-APA-MultiAgent-Planner
pip install -r requirements.txt



##🚗 Quick Start

Run the multi-agent evaluation pipeline:
Bash
python scripts/evaluate_apollo.py --scenario narrow_perpendicular

import os
import torch
import torch.optim as optim
from envs.parking_env import ParkingEnvironment
from agents.rl_ppo_agent import ActorCritic

def train():
    print("--- Starting PPO Training for 4WS Parking Agent ---")
    env = ParkingEnvironment()
    model = ActorCritic(state_dim=3, action_dim=3)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    
    epochs = 1000
    for epoch in range(epochs):
        state = env.reset()
        done = False
        epoch_reward = 0
        
        # Simplified Rollout
        while not done:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            action, _ = model(state_tensor)
            
            next_state, reward, done, _ = env.step(action.detach().numpy().flatten())
            epoch_reward += reward
            state = next_state
            
            # (PPO Update logic would go here: calc advantage, surrogate loss, backprop)
            
        if epoch % 100 == 0:
            print(f"Epoch {epoch}/{epochs} | Total Reward: {epoch_reward:.2f}")

    # Save weights
    os.makedirs("../models", exist_ok=True)
    torch.save(model.state_dict(), "../models/ppo_4ws_latest.pth")
    print("Training complete. Weights saved.")

if __name__ == "__main__":
    train()

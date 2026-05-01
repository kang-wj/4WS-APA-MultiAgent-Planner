import numpy as np
import torch
import torch.nn as nn
from typing import List
from envs.parking_env import ParkingEnvironment

class ActorCritic(nn.Module):
    """PPO Actor-Critic Network structure."""
    def __init__(self, state_dim, action_dim):
        super(ActorCritic, self).__init__()
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Tanh() # Output bounded steering angles
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, state):
        return self.actor(state), self.critic(state)

class RLParkingAgent:
    """
    PPO-based Agent for local trajectory smoothing and 4WS action generation.
    """
    def __init__(self, model_path: str = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network = ActorCritic(state_dim=3, action_dim=3).to(self.device)
        if model_path:
            self._load_model(model_path)

    def _load_model(self, path: str):
        # Mock loading
        print(f"Loaded PPO model weights from {path}")

    def generate_smooth_control(self, coarse_path: List[np.ndarray], env: ParkingEnvironment) -> List[np.ndarray]:
        """
        Takes coarse path and outputs fine-grained [v, delta_f, delta_r] controls.
        """
        refined_trajectory = []
        state = env.reset()
        
        # Inference loop
        for _ in range(len(coarse_path)):
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            with torch.no_grad():
                action, _ = self.network(state_tensor)
            
            action_np = action.cpu().numpy().flatten()
            # Scale actions to physical limits (e.g., max steering angle 35 deg)
            scaled_action = action_np * np.array([1.5, 0.6, 0.6]) 
            
            next_state, _, _, _ = env.step(scaled_action)
            refined_trajectory.append(next_state)
            state = next_state
            
        return refined_trajectory

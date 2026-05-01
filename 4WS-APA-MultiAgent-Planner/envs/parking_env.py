import numpy as np
from typing import Tuple, Dict

class ParkingEnvironment:
    """
    4WS (Four-Wheel Steering) Parking Environment for Reinforcement Learning.
    Includes kinematic constraints for Crab Walk and Zero-Radius Turn.
    """
    def __init__(self, scenario: str = 'narrow_parallel'):
        self.scenario = scenario
        self.dt = 0.1 # Simulation time step
        self.wheelbase = 2.85
        
        # Grid map for obstacle detection (Mock)
        self.obstacle_map = np.zeros((100, 100)) 
        self.start_state = np.array([0.0, 0.0, 0.0]) # x, y, yaw
        self.target_state = np.array([10.0, 5.0, np.pi/2])
        self.current_state = self.start_state.copy()

    def reset(self) -> np.ndarray:
        """Resets the environment to initial state."""
        self.current_state = self.start_state.copy()
        return self.current_state

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Dict]:
        """
        Executes one time step based on 4WS kinematic bicycle model.
        action: [velocity, delta_front, delta_rear]
        """
        v, delta_f, delta_r = action
        x, y, yaw = self.current_state

        # 4WS Kinematic Model update
        beta = np.arctan(0.5 * (np.tan(delta_f) + np.tan(delta_r)))
        next_x = x + v * np.cos(yaw + beta) * self.dt
        next_y = y + v * np.sin(yaw + beta) * self.dt
        next_yaw = yaw + (v * np.cos(beta) / self.wheelbase) * (np.tan(delta_f) - np.tan(delta_r)) * self.dt

        self.current_state = np.array([next_x, next_y, next_yaw])
        
        # Mock reward and done conditions
        done = self._check_collision() or self._reached_target()
        reward = self._compute_reward()
        
        return self.current_state, reward, done, {}

    def _check_collision(self) -> bool:
        # Simplified collision check logic
        return False
        
    def _reached_target(self) -> bool:
        dist = np.linalg.norm(self.current_state[:2] - self.target_state[:2])
        return dist < 0.2

    def _compute_reward(self) -> float:
        return -0.1 # Step penalty

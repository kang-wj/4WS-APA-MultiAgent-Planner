import numpy as np
from typing import List

class GlobalSearchAgent:
    """
    Heuristic Search Agent using a modified A* algorithm for coarse path generation.
    Reduces the search space for the downstream RL local planner.
    """
    def __init__(self, heuristic_weight: float = 1.5):
        self.weight = heuristic_weight

    def plan(self, start: np.ndarray, target: np.ndarray, grid_map: np.ndarray) -> List[np.ndarray]:
        """
        Executes A* search to find a collision-free topological corridor.
        """
        # Mock A* implementation: returns a linearly interpolated coarse path
        coarse_path = []
        steps = 20
        for i in range(steps + 1):
            ratio = i / steps
            interp_x = start[0] + ratio * (target[0] - start[0])
            interp_y = start[1] + ratio * (target[1] - start[1])
            interp_yaw = start[2] + ratio * (target[2] - start[2])
            coarse_path.append(np.array([interp_x, interp_y, interp_yaw]))
            
        return coarse_path

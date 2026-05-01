import time
import argparse
from agents.search_agent import GlobalSearchAgent
from agents.rl_ppo_agent import RLParkingAgent
from agents.sim_agent import CarSimValidationAgent
from envs.parking_env import ParkingEnvironment

def run_multi_agent_pipeline(scenario_name):
    print(f"--- Starting Multi-Agent APA Pipeline for {scenario_name} ---")
    
    env = ParkingEnvironment(scenario=scenario_name)
    search_agent = GlobalSearchAgent()
    rl_agent = RLParkingAgent(model_path="../models/ppo_4ws_latest.pth")
    sim_agent = CarSimValidationAgent()

    start_time = time.time()
    coarse_path = search_agent.plan(env.start_state, env.target_state, env.obstacle_map)
    print(f"[Agent 1] Search Agent completed coarse planning. Nodes expanded: {len(coarse_path)}")

    refined_trajectory = rl_agent.generate_smooth_control(coarse_path, env)
    planning_time = time.time() - start_time
    print(f"[Agent 2] RL Agent generated 4WS steering commands. Planning time: {planning_time*1000:.2f} ms")

    validation_result = sim_agent.run_closed_loop(refined_trajectory)
    
    if validation_result['success']:
        print(f"[Agent 3] Validation Passed. Max cross-track error: {validation_result['max_cte']:.3f}m")
    else:
        print("[Agent 3] Validation Failed: Collision detected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenario', type=str, default='narrow_parallel', help='Parking scenario type')
    args = parser.parse_args()
    
    run_multi_agent_pipeline(args.scenario)

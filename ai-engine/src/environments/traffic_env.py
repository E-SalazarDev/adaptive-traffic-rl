import gymnasium as gym
import numpy as np
import traci

from gymnasium import spaces

from src.config.settings import SUMO_CONFIGS_DIR
from src.simulation.scenario_generator import create_scenario


class TrafficEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, max_steps: int = 600):
        super().__init__()

        self.max_steps = max_steps
        self.current_step = 0
        self.traffic_light_id = None
        self.sumo_running = False

        # Estado:
        # [queue_north, queue_south, queue_east, queue_west, current_phase]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0], dtype=np.float32),
            high=np.array([100, 100, 100, 100, 20], dtype=np.float32),
            dtype=np.float32,
        )

        # Acciones:
        # 0 = mantener fase
        # 1 = cambiar fase
        self.action_space = spaces.Discrete(2)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.close()

        create_scenario()

        config_file = SUMO_CONFIGS_DIR / "single_intersection.sumocfg"

        command = [
            "sumo",
            "-c",
            str(config_file),
            "--no-warnings",
            "--start",
            "--quit-on-end",
        ]

        traci.start(command)

        self.sumo_running = True
        self.current_step = 0

        traffic_light_ids = traci.trafficlight.getIDList()
        self.traffic_light_id = traffic_light_ids[0] if traffic_light_ids else None

        observation = self._get_state()
        info = self._get_info()

        return observation, info

    def step(self, action):
        if not self.sumo_running:
            raise RuntimeError("SUMO no está corriendo. Ejecuta reset() primero.")

        self._apply_action(action)

        traci.simulationStep()
        self.current_step += 1

        observation = self._get_state()
        reward = self._calculate_reward()

        terminated = traci.simulation.getMinExpectedNumber() <= 0
        truncated = self.current_step >= self.max_steps

        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def close(self):
        if self.sumo_running:
            traci.close()
            self.sumo_running = False

    def _apply_action(self, action: int) -> None:
        if self.traffic_light_id is None:
            return

        current_phase = traci.trafficlight.getPhase(self.traffic_light_id)
        total_phases = len(traci.trafficlight.getAllProgramLogics(self.traffic_light_id)[0].phases)

        if action == 0:
            return

        if action == 1:
            next_phase = (current_phase + 1) % total_phases
            traci.trafficlight.setPhase(self.traffic_light_id, next_phase)

    def _get_queue_length_by_edge(self, edge_id: str) -> int:

        return traci.edge.getLastStepHaltingNumber(edge_id)

    def _get_queues(self) -> dict:
        return {
            "north": self._get_queue_length_by_edge("A2A1"),
            "south": self._get_queue_length_by_edge("A0A1"),
            "west": self._get_queue_length_by_edge("A1B1"),
            "east": self._get_queue_length_by_edge("C1B1"),
        }

    def _get_state(self):
        queues = self._get_queues()

        current_phase = 0

        if self.traffic_light_id is not None:
            current_phase = traci.trafficlight.getPhase(self.traffic_light_id)

        state = np.array(
            [
                queues["north"],
                queues["south"],
                queues["east"],
                queues["west"],
                current_phase,
            ],
            dtype=np.float32,
        )

        return state

    def _calculate_reward(self) -> float:
        queues = self._get_queues()
        total_queue = sum(queues.values())

        return -float(total_queue)

    def _get_info(self) -> dict:
        queues = self._get_queues()

        return {
            "step": self.current_step,
            "queues": queues,
            "total_queue": sum(queues.values()),
            "traffic_light_id": self.traffic_light_id,
            "active_vehicles": len(traci.vehicle.getIDList()),
        }
from pathlib import Path

from src.config.settings import SUMO_OUTPUTS_DIR
from src.simulation.sumo_runner import run_traci_timeline_simulation
from src.utils.json_exporter import export_json


def calculate_baseline_metrics(timeline: list[dict]) -> dict:
    if not timeline:
        return {
            "avg_waiting_time": 0,
            "max_queue_length": 0,
            "throughput": 0,
            "avg_speed": 0,
            "total_reward": 0,
            "episode_length": 0,
        }

    total_queues = []
    active_vehicle_counts = []
    speeds = []

    for step in timeline:
        total_queues.append(step["total_queue"])
        active_vehicle_counts.append(step["active_vehicles"])

        for vehicle in step["vehicles"]:
            speeds.append(vehicle["speed"])

    total_reward = -sum(total_queues)

    return {
        "avg_waiting_time": round(sum(total_queues) / len(total_queues), 4),
        "max_queue_length": max(total_queues),
        "throughput": max(active_vehicle_counts),
        "avg_speed": round(sum(speeds) / len(speeds), 4) if speeds else 0,
        "total_reward": total_reward,
        "episode_length": len(timeline),
    }


def run_fixed_baseline(max_steps: int = 600) -> dict:
    timeline = run_traci_timeline_simulation(max_steps=max_steps)

    metrics = calculate_baseline_metrics(timeline)

    result = {
        "strategy": "FIXED_TIME",
        "scenario_id": "single_intersection_default",
        "metrics": metrics,
        "timeline": timeline,
    }

    output_path: Path = SUMO_OUTPUTS_DIR / "fixed_baseline_result.json"
    export_json(result, output_path)

    print(f"[OK] Resultado baseline exportado: {output_path}")

    return result
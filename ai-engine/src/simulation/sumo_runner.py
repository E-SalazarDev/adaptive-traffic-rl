import subprocess
from pathlib import Path

import traci

from src.config.settings import SUMO_CONFIGS_DIR, SUMO_OUTPUTS_DIR


CONFIG_FILE_NAME = "single_intersection.sumocfg"
TIMELINE_FILE_NAME = "timeline_fixed_baseline.json"


def run_sumo_simulation() -> None:
    config_file = SUMO_CONFIGS_DIR / CONFIG_FILE_NAME

    if not config_file.exists():
        raise FileNotFoundError(f"No existe el archivo SUMO config: {config_file}")

    command = [
        "sumo",
        "-c",
        str(config_file),
        "--no-warnings",
    ]

    print("Ejecutando SUMO...")
    print(" ".join(command))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    print("\nSTDOUT:")
    print(result.stdout)

    print("\nSTDERR:")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError("SUMO terminó con error.")

    print("Simulación SUMO ejecutada correctamente.")


def get_queue_length_by_edge(edge_id: str) -> int:
    vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)

    queue_count = 0

    for vehicle_id in vehicle_ids:
        speed = traci.vehicle.getSpeed(vehicle_id)

        if speed < 0.1:
            queue_count += 1

    return queue_count


def get_vehicle_snapshots() -> list[dict]:
    vehicles = []

    for vehicle_id in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(vehicle_id)

        vehicles.append(
            {
                "id": vehicle_id,
                "x": round(x, 2),
                "y": round(y, 2),
                "speed": round(traci.vehicle.getSpeed(vehicle_id), 2),
                "angle": round(traci.vehicle.getAngle(vehicle_id), 2),
                "lane": traci.vehicle.getLaneID(vehicle_id),
            }
        )

    return vehicles


def run_traci_timeline_simulation(max_steps: int = 600) -> list[dict]:
    config_file = SUMO_CONFIGS_DIR / CONFIG_FILE_NAME

    if not config_file.exists():
        raise FileNotFoundError(f"No existe el archivo SUMO config: {config_file}")

    command = [
        "sumo",
        "-c",
        str(config_file),
        "--no-warnings",
        "--start",
        "--quit-on-end",
    ]

    timeline = []

    print("Ejecutando SUMO con TraCI...")
    print(" ".join(command))

    traci.start(command)

    try:
        traffic_light_ids = traci.trafficlight.getIDList()
        traffic_light_id = traffic_light_ids[0] if traffic_light_ids else None

        for step in range(max_steps):
            traci.simulationStep()

            queues = {
                "north": get_queue_length_by_edge("A2A1"),
                "south": get_queue_length_by_edge("A0A1"),
                "west": get_queue_length_by_edge("A1B1"),
                "east": get_queue_length_by_edge("C1B1"),
            }

            current_phase = None
            current_phase_name = "NO_TRAFFIC_LIGHT"

            if traffic_light_id:
                current_phase = traci.trafficlight.getPhase(traffic_light_id)
                current_phase_name = traci.trafficlight.getRedYellowGreenState(
                    traffic_light_id
                )

            vehicles = get_vehicle_snapshots()

            total_queue = sum(queues.values())

            timeline.append(
                {
                    "time": step,
                    "traffic_light_id": traffic_light_id,
                    "phase": current_phase,
                    "phase_state": current_phase_name,
                    "queues": queues,
                    "total_queue": total_queue,
                    "active_vehicles": len(vehicles),
                    "vehicles": vehicles,
                }
            )

            if traci.simulation.getMinExpectedNumber() <= 0:
                break

    finally:
        traci.close()

    return timeline
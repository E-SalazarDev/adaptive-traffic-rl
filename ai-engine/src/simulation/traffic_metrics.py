import xml.etree.ElementTree as ET
from pathlib import Path

from src.config.settings import SUMO_OUTPUTS_DIR


def parse_tripinfo_metrics(tripinfo_path: Path) -> dict:
    if not tripinfo_path.exists():
        raise FileNotFoundError(f"No existe tripinfo.xml: {tripinfo_path}")

    tree = ET.parse(tripinfo_path)
    root = tree.getroot()

    waiting_times = []
    speeds = []
    durations = []
    vehicle_count = 0

    for trip in root.findall("tripinfo"):
        vehicle_count += 1

        duration = float(trip.attrib.get("duration", 0))
        waiting_time = float(trip.attrib.get("waitingTime", 0))
        route_length = float(trip.attrib.get("routeLength", 0))

        durations.append(duration)
        waiting_times.append(waiting_time)

        if duration > 0:
            speeds.append(route_length / duration)

    avg_waiting_time = sum(waiting_times) / vehicle_count if vehicle_count > 0 else 0
    avg_speed = sum(speeds) / len(speeds) if speeds else 0
    avg_duration = sum(durations) / vehicle_count if vehicle_count > 0 else 0

    return {
        "avg_waiting_time": round(avg_waiting_time, 4),
        "avg_speed": round(avg_speed, 4),
        "avg_trip_duration": round(avg_duration, 4),
        "throughput": vehicle_count,
    }


def parse_summary_metrics(summary_path: Path) -> dict:
    if not summary_path.exists():
        raise FileNotFoundError(f"No existe summary.xml: {summary_path}")

    tree = ET.parse(summary_path)
    root = tree.getroot()

    max_running_vehicles = 0
    episode_length = 0

    for step in root.findall("step"):
        time = float(step.attrib.get("time", 0))
        running = int(step.attrib.get("running", 0))

        episode_length = max(episode_length, int(time))
        max_running_vehicles = max(max_running_vehicles, running)

    return {
        "episode_length": episode_length,
        "max_running_vehicles": max_running_vehicles,
    }


def collect_sumo_metrics() -> dict:
    tripinfo_path = SUMO_OUTPUTS_DIR / "tripinfo.xml"
    summary_path = SUMO_OUTPUTS_DIR / "summary.xml"

    trip_metrics = parse_tripinfo_metrics(tripinfo_path)
    summary_metrics = parse_summary_metrics(summary_path)

    metrics = {
        **trip_metrics,
        **summary_metrics,
        "max_queue_length": 0,
        "total_reward": 0,
    }

    return metrics
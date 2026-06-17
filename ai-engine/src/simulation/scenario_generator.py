import subprocess
from pathlib import Path

from src.config.settings import (
    SUMO_NETWORKS_DIR,
    SUMO_ROUTES_DIR,
    SUMO_CONFIGS_DIR,
)


NETWORK_FILE_NAME = "single_intersection.net.xml"
ROUTES_FILE_NAME = "single_intersection.rou.xml"
CONFIG_FILE_NAME = "single_intersection.sumocfg"


def create_network_file() -> Path:
    network_file = SUMO_NETWORKS_DIR / NETWORK_FILE_NAME

    command = [
        "netgenerate",
        "--grid",
        "--grid.number", "3",
        "--grid.length", "200",
        "--tls.guess",
        "--output-file", str(network_file),
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("No se pudo generar la red SUMO con netgenerate.")

    return network_file


def create_routes_file() -> Path:
    routes_file = SUMO_ROUTES_DIR / ROUTES_FILE_NAME

    content = """<?xml version="1.0" encoding="UTF-8"?>

<routes>
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" maxSpeed="13.89"/>

    <route id="north_to_south" edges="A2A1 A1A0"/>
    <route id="south_to_north" edges="A0A1 A1A2"/>
    <route id="west_to_east" edges="A1B1 B1C1"/>
    <route id="east_to_west" edges="C1B1 B1A1"/>

    <flow id="flow_north_south" type="car" route="north_to_south" begin="0" end="600" vehsPerHour="300"/>
    <flow id="flow_south_north" type="car" route="south_to_north" begin="0" end="600" vehsPerHour="300"/>
    <flow id="flow_west_east" type="car" route="west_to_east" begin="0" end="600" vehsPerHour="200"/>
    <flow id="flow_east_west" type="car" route="east_to_west" begin="0" end="600" vehsPerHour="200"/>
</routes>
"""

    routes_file.write_text(content, encoding="utf-8")
    return routes_file


def create_config_file() -> Path:
    config_file = SUMO_CONFIGS_DIR / CONFIG_FILE_NAME

    content = f"""<?xml version="1.0" encoding="UTF-8"?>

<configuration>
    <input>
        <net-file value="../networks/{NETWORK_FILE_NAME}"/>
        <route-files value="../routes/{ROUTES_FILE_NAME}"/>
    </input>

    <time>
        <begin value="0"/>
        <end value="600"/>
        <step-length value="1"/>
    </time>

    <output>
        <tripinfo-output value="../outputs/tripinfo.xml"/>
        <summary-output value="../outputs/summary.xml"/>
    </output>
</configuration>
"""

    config_file.write_text(content, encoding="utf-8")
    return config_file


def create_scenario() -> dict:
    network_file = create_network_file()
    routes_file = create_routes_file()
    config_file = create_config_file()

    return {
        "network_file": str(network_file),
        "routes_file": str(routes_file),
        "config_file": str(config_file),
    }
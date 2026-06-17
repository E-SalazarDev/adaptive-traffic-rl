import subprocess
from pathlib import Path

from src.config.settings import SUMO_CONFIGS_DIR


def run_sumo_simulation() -> None:
    config_file = SUMO_CONFIGS_DIR / "single_intersection.sumocfg"

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
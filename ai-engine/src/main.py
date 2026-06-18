import shutil
import sys

from src.config.settings import (
    PROJECT_NAME,
    VERSION,
    SUMO_HOME,
    ensure_directories_exist,
    get_project_paths,
)

from src.simulation.scenario_generator import create_scenario
from src.simulation.sumo_runner import (
    run_sumo_simulation,
    run_traci_timeline_simulation,
)
from src.simulation.traffic_metrics import collect_sumo_metrics
from src.config.settings import SUMO_OUTPUTS_DIR
from src.simulation.sumo_runner import run_traci_timeline_simulation
from src.utils.json_exporter import export_json
from src.agents.fixed_controller import run_fixed_baseline

def check_python_version() -> None:
    print("\n[1] Verificando Python...")
    print(f"Version detectada: {sys.version}")

    if sys.version_info.major == 3 and sys.version_info.minor >= 10:
        print("[OK] Python compatible.")
    else:
        print("[WARNING] Se recomienda Python 3.10 o superior.")


def check_sumo_installation() -> None:
    print("\n[2] Verificando SUMO...")

    sumo_binary = shutil.which("sumo")
    sumo_gui_binary = shutil.which("sumo-gui")

    if SUMO_HOME:
        print(f"[OK] SUMO_HOME detectado: {SUMO_HOME}")
    else:
        print("[WARNING] SUMO_HOME no está configurado.")

    if sumo_binary:
        print(f"[OK] sumo detectado en PATH: {sumo_binary}")
    else:
        print("[WARNING] No se encontró 'sumo' en PATH.")

    if sumo_gui_binary:
        print(f"[OK] sumo-gui detectado en PATH: {sumo_gui_binary}")
    else:
        print("[WARNING] No se encontró 'sumo-gui' en PATH.")


def check_python_imports() -> None:
    print("\n[3] Verificando librerías Python...")

    packages = [
        "numpy",
        "pandas",
        "gymnasium",
        "stable_baselines3",
        "traci",
        "sumolib",
    ]

    for package in packages:
        try:
            __import__(package)
            print(f"[OK] {package}")
        except ImportError:
            print(f"[MISSING] {package}")


def print_project_paths() -> None:
    print("\n[4] Rutas del proyecto...")

    paths = get_project_paths()

    for name, path in paths.items():
        print(f"{name}: {path}")


def generate_and_run_sumo_scenario() -> None:
    print("\n[5] Generando escenario SUMO...")

    scenario_files = create_scenario()

    for name, path in scenario_files.items():
        print(f"[OK] {name}: {path}")

    print("\n[6] Ejecutando simulación SUMO...")
    run_sumo_simulation()


def main() -> None:
    print("=" * 70)
    print(f"{PROJECT_NAME} v{VERSION}")
    print("FASE 2 - Crear y ejecutar una intersección SUMO")
    print("=" * 70)

    ensure_directories_exist()

    check_python_version()
    check_sumo_installation()
    check_python_imports()
    print_project_paths()

    generate_and_run_sumo_scenario()
    print("\n[7] Leyendo métricas de SUMO...")
    metrics = collect_sumo_metrics()

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\nResultado:")
    print("Escenario SUMO generado y ejecutado correctamente.")
    print("Se crearon tripinfo.xml y summary.xml")
    
    print("\n[8] Ejecutando simulación con TraCI")
    timeline = run_traci_timeline_simulation(max_steps=600)

    timeline_path = SUMO_OUTPUTS_DIR / "timeline_fixed_baseline.json"
    export_json(timeline, timeline_path)

    print(f"[OK] Timeline exportado: {timeline_path}")
    print(f"[OK] Timesteps registrados: {len(timeline)}")
    
    print("\n[9] Ejecutando baseline de semáforo fijo...")
    fixed_result = run_fixed_baseline(max_steps=600)

    print("\nMétricas baseline fijo:")
    for key, value in fixed_result["metrics"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
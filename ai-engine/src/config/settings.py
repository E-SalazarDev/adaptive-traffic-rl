from pathlib import Path
import os


# Carpeta raíz de ai-engine
BASE_DIR = Path(__file__).resolve().parents[2]

# Carpetas principales
SRC_DIR = BASE_DIR / "src"

SUMO_DIR = BASE_DIR / "sumo"
SUMO_NETWORKS_DIR = SUMO_DIR / "networks"
SUMO_ROUTES_DIR = SUMO_DIR / "routes"
SUMO_CONFIGS_DIR = SUMO_DIR / "configs"
SUMO_OUTPUTS_DIR = SUMO_DIR / "outputs"

MODELS_DIR = BASE_DIR / "models"
SAVED_MODELS_DIR = MODELS_DIR / "saved_models"

EXPORTS_DIR = SRC_DIR / "exports"
RESULTS_DIR = EXPORTS_DIR / "results"

# Variable de entorno de SUMO en Windows
SUMO_HOME = os.environ.get("SUMO_HOME")

PROJECT_NAME = "Adaptive Traffic RL - AI Engine"
VERSION = "0.1.0"


def ensure_directories_exist() -> None:
    """
    Crea las carpetas necesarias si no existen.
    Esto evita errores cuando el proyecto intente guardar archivos.
    """

    directories = [
        SUMO_NETWORKS_DIR,
        SUMO_ROUTES_DIR,
        SUMO_CONFIGS_DIR,
        SUMO_OUTPUTS_DIR,
        SAVED_MODELS_DIR,
        RESULTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_project_paths() -> dict:
    """
    Devuelve las rutas importantes del proyecto.
    Sirve para depurar y verificar que todo esté apuntando bien.
    """

    return {
        "base_dir": str(BASE_DIR),
        "src_dir": str(SRC_DIR),
        "sumo_dir": str(SUMO_DIR),
        "sumo_networks_dir": str(SUMO_NETWORKS_DIR),
        "sumo_routes_dir": str(SUMO_ROUTES_DIR),
        "sumo_configs_dir": str(SUMO_CONFIGS_DIR),
        "sumo_outputs_dir": str(SUMO_OUTPUTS_DIR),
        "models_dir": str(MODELS_DIR),
        "saved_models_dir": str(SAVED_MODELS_DIR),
        "results_dir": str(RESULTS_DIR),
        "sumo_home": SUMO_HOME,
    }
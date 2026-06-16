# 🚦 Adaptive Traffic RL

Sistema de simulación y optimización de tráfico urbano mediante **Reinforcement Learning**, desarrollado como proyecto Full Stack de portafolio.

El objetivo es construir una plataforma donde los usuarios puedan crear escenarios de tráfico, ejecutar simulaciones, comparar estrategias de control semafórico y analizar métricas de rendimiento utilizando inteligencia artificial.

> Este proyecto NO controla semáforos reales.
>
> Es una plataforma de simulación, experimentación y análisis construida para demostrar habilidades en IA, Backend, Frontend, Bases de Datos, DevOps y MLOps.

---

# 🎯 Objetivo

Diseñar una plataforma capaz de:

* Crear escenarios de tráfico personalizados.
* Simular redes viales utilizando SUMO.
* Ejecutar estrategias tradicionales de control semafórico.
* Entrenar agentes de Reinforcement Learning.
* Comparar resultados entre diferentes estrategias.
* Visualizar métricas de rendimiento.
* Exportar reportes para análisis posterior.

---

# 🏗️ Arquitectura General

```text
adaptive-traffic-rl/
│
├── ai-engine/          # SUMO, TraCI, Gymnasium, RL
├── backend/            # Spring Boot API
├── frontend/           # React + Tailwind Dashboard
├── infrastructure/     # Docker, Compose y despliegue
└── docs/               # Documentación y diagramas
```

---

# 🤖 Módulo de Inteligencia Artificial

El núcleo del proyecto se encuentra en `ai-engine`.

Tecnologías principales:

* Python
* SUMO
* TraCI
* Gymnasium
* Stable-Baselines3
* DQN
* PPO (futuro)
* MLflow (futuro)

Funciones:

* Generación de tráfico sintético.
* Simulación de intersecciones.
* Entrenamiento de agentes RL.
* Evaluación de estrategias.
* Exportación de métricas.

---

# ⚙️ Backend

Desarrollado con:

* Java 21
* Spring Boot
* Spring Security
* Spring Data JPA
* PostgreSQL

Responsabilidades:

* Gestión de usuarios.
* Gestión de proyectos.
* Gestión de escenarios.
* Historial de simulaciones.
* Persistencia de métricas.
* API REST para frontend.

---

# 🎨 Frontend

Desarrollado con:

* React
* Tailwind CSS
* React Query
* Zustand
* Recharts
* Leaflet

Funciones:

* Dashboard principal.
* Configuración de simulaciones.
* Visualización de métricas.
* Comparación de experimentos.
* Historial de ejecuciones.

---

# 📊 Métricas Principales

El sistema compara estrategias utilizando:

* Tiempo promedio de espera.
* Longitud máxima de cola.
* Throughput.
* Velocidad promedio.
* Recompensa acumulada.
* Duración del episodio.

---

# 🧠 Estrategias de Control

## Baseline

Semáforo de tiempo fijo.

Ejemplo:

* Verde Norte-Sur: 30 segundos
* Amarillo: 3 segundos
* Verde Este-Oeste: 30 segundos
* Amarillo: 3 segundos

## Reinforcement Learning

Agente DQN entrenado para:

* Reducir congestión.
* Reducir tiempos de espera.
* Mejorar throughput.
* Optimizar flujo vehicular.

---

| Categoría | Tecnologías                                       |
| --------- | ------------------------------------------------- |
| IA        | Python, SUMO, TraCI, Gymnasium, Stable-Baselines3 |
| Backend   | Spring Boot, Spring Security, PostgreSQL          |
| Frontend  | React, Tailwind, Recharts, Leaflet                |
| DevOps    | Docker, Docker Compose, GitHub Actions            |
| MLOps     | MLflow                                            |

---

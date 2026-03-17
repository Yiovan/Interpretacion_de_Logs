# 6to Challenge - The Huddle: Análisis de Server Logs

## Descripción

Proyecto de análisis exploratorio de datos (EDA) sobre logs de servidores de una arquitectura de microservicios. El objetivo es identificar patrones de errores, detectar ventanas críticas de tiempo con alta tasa de fallos, y comparar el comportamiento durante incidentes vs. el comportamiento normal del sistema.

## Dataset

El archivo `server_logs.csv` contiene **5,795 registros** de logs con las siguientes columnas:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `timestamp_event` | datetime | Momento en que ocurrió el evento |
| `received_at` | datetime | Momento en que se recibió el log |
| `service_name` | string | Nombre del microservicio origen |
| `severity` | string | Nivel de severidad (`INFO`, `WARN`, `ERROR`, `CRITICAL`) |
| `message` | string | Descripción del evento |
| `trace_id` | string | ID de trazabilidad |
| `request_id` | string | ID de la petición |
| `method` | string | Método HTTP |
| `endpoint` | string | Endpoint de la API |
| `status_code` | int | Código de respuesta HTTP |
| `latency_ms` | int | Latencia en milisegundos |
| `host` | string | Host del servidor |
| `env` | string | Ambiente (producción, staging, etc.) |
| `region` | string | Región del servidor |
| `log_type` | string | Tipo de log |

### Microservicios incluidos

- `api-gateway` — 1,509 logs
- `orders-service` — 1,057 logs
- `inventory-service` — 964 logs
- `payment-service` — 842 logs
- `auth-service` — 778 logs
- `notification-service` — 645 logs

## Análisis realizados

1. **Exploración general** — Carga de datos, inspección de tipos y estructura del dataset.
2. **Distribución de severidad** — Conteo de logs por nivel: INFO (3,542), WARN (1,358), ERROR (775), CRITICAL (120).
3. **Volumen por servicio** — Identificación de los servicios con mayor y menor cantidad de logs.
4. **Detección de eventos "malos"** — Clasificación de logs con severidad `ERROR`/`CRITICAL` o status code ≥ 500.
5. **Ventanas de tiempo críticas** — Agrupación por ventanas de 1 minuto para detectar picos de error rate (hasta 72.5%).
6. **Análisis de ventana más crítica** — Desglose de la ventana `2026-01-10 11:10 UTC` por servicio, mensajes y endpoints afectados.
7. **Comparación crítico vs. baseline** — Métricas comparativas: bad rate, latencia promedio y porcentaje de 5xx.
8. **Visualizaciones** — Gráficos de severidad en el tiempo y bad rate temporal con Matplotlib.

### Hallazgos clave

- La ventana más crítica tuvo un **bad rate del 72.5%** vs. un baseline del **15%**.
- La latencia promedio durante el incidente fue de **1,667 ms** (3x más que el baseline de 548 ms).
- Los servicios más afectados fueron `orders-service` e `inventory-service`.
- El error dominante: **"Order creation failed - inventory lock timeout"**.
- El endpoint más impactado: `/orders/create`.

## Tecnologías

- **Python 3.13**
- **Pandas** — Manipulación y análisis de datos
- **Matplotlib** — Visualización de datos
- **Jupyter Notebook** — Entorno interactivo de desarrollo

## Instalación y uso

### Prerrequisitos

- Python 3.10+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd 6to_the_huddle

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el notebook
jupyter notebook app.ipynb
```

## Estructura del proyecto

```
6to_the_huddle/
├── app.ipynb            # Notebook con todo el análisis
├── server_logs.csv      # Dataset de logs de servidor
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Este archivo
```

---

> Parte de la serie **Challenges Penguin — The Huddle**

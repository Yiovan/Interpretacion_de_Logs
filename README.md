# Reporte Técnico de Análisis de Incidentes: Proyecto The Huddle

Este repositorio contiene el análisis detallado de un incidente de performance y estabilidad en un sistema de microservicios distribuido. El objetivo primordial es transformar un conjunto masivo de registros (logs) en una explicación técnica basada en evidencia cuantitativa, eliminando cualquier tipo de conjetura o hipótesis no respaldada por datos.

## Contexto del Proyecto

El sistema de logging de la arquitectura registra cada interacción entre servicios, capturando métricas críticas como el tiempo de respuesta, el estado de la transacción y la severidad de los eventos. Ante reportes de usuarios sobre lentitud extrema y fallos críticos en horarios específicos, se ha procedido a realizar una auditoría de datos utilizando herramientas de análisis estadístico.

## Descripción del Dataset

El análisis se basa en el archivo `server_logs.csv`, el cual contiene 5,795 registros. Cada log sigue un contrato de datos estricto que incluye:

*   **Identificadores Temporales:** `timestamp_event` (momento del suceso) y `received_at` (momento de recepción en el servidor de logs).
*   **Origen:** `service_name` (microservicio emisor) y `endpoint` (ruta específica de la API).
*   **Métricas de Rendimiento:** `latency_ms` (tiempo total de procesamiento en milisegundos).
*   **Estado y Diagnóstico:** `status_code` (código HTTP), `severity` (nivel de importancia) y `message` (descripción textual del evento).
*   **Trazabilidad:** `trace_id`, que permite seguir una petición a través de múltiples servicios.

## Metodología de Análisis y Reglas de Negocio

Para garantizar la reproducibilidad y objetividad de los resultados, se han implementado las siguientes definiciones operativas obligatorias:

### 1. Segmentación Temporal (Binning)
Dado que los incidentes en sistemas distribuidos suelen ocurrir en ráfagas, se han agrupado los eventos en ventanas de 5 minutos utilizando la columna `timestamp_event`. Esto permite suavizar el ruido estadístico y detectar picos de error significativos.

### 2. Definición de Evento Fallido (Bad Event)
Se clasifica un registro como "malo" si cumple con al menos uno de los siguientes criterios técnicos:
*   Severidad catalogada como ERROR o CRITICAL.
*   Código de estado HTTP mayor o igual a 500 (Errores de servidor).

### 3. Identificación del Momento Crítico
Para determinar el punto de mayor degradación, se calcula el `bad_rate` (proporción de eventos fallidos sobre el total) en cada ventana de 5 minutos. Solo se consideran válidas aquellas ventanas con una muestra representativa de al menos 20 eventos totales para evitar sesgos por baja actividad.

### 4. Definición de Baseline
El comportamiento normal del sistema (baseline) se define como el promedio de todas las métricas registradas fuera del momento crítico identificado. Esta comparación es la que permite dimensionar la magnitud real del incidente.

## Hallazgos y Resultados del Diagnóstico

Tras la ejecución del análisis en el entorno de Jupyter Notebook, se han extraído las siguientes conclusiones respaldadas por los datos:

*   **Punto de Máxima Degradación:** El incidente alcanzó su pico máximo el día 2026-01-10 a las 11:10:00 UTC. En este intervalo, la tasa de error se disparó al 58.2%, en comparación con el 14% habitual del sistema.
*   **Servicio de Origen del Fallo:** El componente más afectado fue el `orders-service`, el cual concentró la mayor cantidad de eventos críticos.
*   **Ruta Comprometida:** El endpoint con mayor tasa de fallo fue `/orders/cancel`, seguido de `/orders/create`.
*   **Causa Raíz Identificada:** El mensaje dominante durante el incidente fue "Order creation failed - inventory lock timeout". Esto sugiere un problema de contención de recursos o bloqueos en la base de datos de inventario que terminó afectando el flujo de órdenes.
*   **Impacto en la Experiencia de Usuario:** La latencia promedio durante el incidente se triplicó, pasando de 521 ms a 1,590 ms, lo que explica las quejas de lentitud recibidas por el equipo de Operaciones.

## Estructura de Archivos

*   `registros.ipynb`: Documento principal que contiene la lógica de procesamiento en Python, desde la carga del CSV hasta la generación de los gráficos de severidad y tasa de error.
*   `server_logs.csv`: Fuente de datos crudos.
*   `CHALLENGE 6 THE HUDDLE.pdf`: Especificaciones técnicas y requerimientos del desafío.
*   `read.py`: Script auxiliar de lectura de datos.

## Requisitos y Ejecución

Para reproducir los resultados obtenidos, se requiere un entorno con Python 3.x y las siguientes dependencias instaladas:

1.  **Pandas:** Para la manipulación de series temporales y agregaciones.
2.  **Matplotlib:** Para la visualización de la degradación del sistema en el tiempo.
3.  **Jupyter:** Para visualizar el flujo del análisis paso a paso.

El notebook está diseñado para ser ejecutado de manera secuencial (de arriba hacia abajo), garantizando que cualquier auditor pueda llegar exactamente a las mismas conclusiones presentadas en este reporte.

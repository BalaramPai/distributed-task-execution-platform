# src/constants/workerConstants.py

NUM_WORKERS = 3

# How often a worker heartbeat is updated.
HEARTBEAT_INTERVAL = 2

# Maximum time allowed between heartbeats before the worker is considered unhealthy.
HEARTBEAT_TIMEOUT = 6
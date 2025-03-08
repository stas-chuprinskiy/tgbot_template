import multiprocessing

from core.config import get_settings

bind = f"{get_settings().app_host}:{get_settings().app_port}"
worker_class = "uvicorn_worker.UvicornWorker"
workers = multiprocessing.cpu_count()

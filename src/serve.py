#!/usr/bin/env python
# This file starts nginx and gunicorn with the correct configurations and then simply waits until
# gunicorn exits.
#
# The fastapi server is specified to be the app object in main.py
#
# We set the following parameters:
#
# Parameter                Environment Variable              Default Value
# ---------                --------------------              -------------
# number of workers        MODEL_SERVER_WORKERS              the number of CPU cores
# timeout                  MODEL_SERVER_TIMEOUT              60 seconds
import argparse
import multiprocessing
import os
import signal
import structlog
import subprocess
import sys

cpu_count = multiprocessing.cpu_count()
model_server_timeout = os.environ.get('MODEL_SERVER_TIMEOUT', 60)
model_server_workers = int(os.environ.get('MODEL_SERVER_WORKERS', cpu_count))
APP = "main:app"
logger = structlog.get_logger(src="serve.py")


def sigterm_handler(nginx_pid, gunicorn_pid):
    try:
        os.kill(nginx_pid, signal.SIGQUIT)
    except OSError:
        pass
    try:
        os.kill(gunicorn_pid, signal.SIGTERM)
    except OSError:
        pass

    sys.exit(0)


def start_server():
    logger.info('Starting the server with {} workers.'.format(model_server_workers))

    # link the log streams to stdout/err so they will be logged to the container logs
    subprocess.check_call(['ln', '-sf', '/dev/stdout', '/var/log/nginx/access.log'])
    subprocess.check_call(['ln', '-sf', '/dev/stderr', '/var/log/nginx/error.log'])

    nginx = subprocess.Popen(['nginx', '-c', '/opt/program/nginx.conf'])
    gunicorn = subprocess.Popen(["gunicorn",
                                 "--bind", "unix:/tmp/gunicorn.sock",
                                 "--workers", str(model_server_workers),
                                 "--worker-class", "uvicorn.workers.UvicornWorker",
                                 f"{APP}"
                                 ]
                                )

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(nginx.pid, gunicorn.pid))

    # Exit the inference server upon exit of either subprocess
    pids = {nginx.pid, gunicorn.pid}
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(nginx.pid, gunicorn.pid)
    logger.info('Server exiting')


def start_server_local():
    logger.info('Starting the server with {} workers.'.format(model_server_workers))

    gunicorn = subprocess.Popen(["gunicorn",
                                 "--bind", "127.0.0.1:8000",
                                 "--workers", "1",
                                 "--worker-class", "uvicorn.workers.UvicornWorker",
                                 f"{APP}",
                                 "--reload"
                                 ]
                                )

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(1, gunicorn.pid))

    # Exit the inference server upon exit of either subprocess
    pids = {1, gunicorn.pid}
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(1, gunicorn.pid)
    logger.info('Server exiting')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", "-e", type=str, default="live")
    args = parser.parse_args()

    if args.env == "dev":
        start_server_local()
    else:
        start_server()

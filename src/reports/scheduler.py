"""
scheduler.py
Planificador de tareas en segundo plano para ToDo.
"""

import threading
import time
from datetime import datetime


class ScheduledJob:

    def __init__(self, name, interval, callback):
        self.name = name
        self.interval = interval
        self.callback = callback
        self.last_run = None
        self.enabled = True

    def run(self):
        self.last_run = datetime.now()
        self.callback()


class Scheduler:

    def __init__(self):
        self.jobs = []
        self._running = False
        self._thread = None

    def add_job(self, name, interval_seconds, callback):
        job = ScheduledJob(name, interval_seconds, callback)
        self.jobs.append(job)
        return job

    def remove_job(self, name):
        self.jobs = [j for j in self.jobs if j.name != name]

    def list_jobs(self):
        return [{
            "name": j.name,
            "interval": j.interval,
            "enabled": j.enabled,
            "last_run": (
                j.last_run.strftime("%Y-%m-%d %H:%M:%S")
                if j.last_run else None
            )
        } for j in self.jobs]

    def start(self):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        next_run = {}

        while self._running:

            now = time.time()

            for job in self.jobs:

                if not job.enabled:
                    continue

                if now >= next_run.get(job.name, 0):

                    try:
                        job.run()
                    except Exception as exc:
                        print(f"[Scheduler] Error en {job.name}: {exc}")

                    next_run[job.name] = now + job.interval

            time.sleep(1)


if __name__ == "__main__":

    scheduler = Scheduler()

    scheduler.add_job(
        "heartbeat",
        5,
        lambda: print("Heartbeat", datetime.now())
    )

    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()

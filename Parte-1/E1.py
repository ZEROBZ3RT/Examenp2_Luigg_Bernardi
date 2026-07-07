
import multiprocessing
import threading
import time
import random



class TaskProcessor:
    def __init__(self):
        # Contador para hilos
        self.tasks_completed_threads = 0
        self.thread_lock = threading.Lock()

        # Contador para procesos
        self.tasks_completed_processes = multiprocessing.Value('i', 0)

    def process_task(self, task_id, difficulty):
        """Simula el procesamiento de una tarea"""

        print(f"Iniciando tarea {task_id} (Dificultad: {difficulty})")

        processing_time = difficulty * 0.3
        time.sleep(processing_time)

        result = task_id * difficulty

        print(f"Tarea {task_id} completada. Resultado = {result}")

        return result

    # Worker para hilos
    def _worker_thread(self, task_id, difficulty):
        self.process_task(task_id, difficulty)

        with self.thread_lock:
            self.tasks_completed_threads += 1

    # Worker para procesos
    def _worker_process(self, task_id, difficulty):
        self.process_task(task_id, difficulty)

        with self.tasks_completed_processes.get_lock():
            self.tasks_completed_processes.value += 1

    def run_with_threads(self, tasks):
        threads = []

        inicio = time.time()

        for task_id, difficulty in tasks:
            thread = threading.Thread(
                target=self._worker_thread,
                args=(task_id, difficulty)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        fin = time.time()

        print(f"\nTareas completadas con hilos: {self.tasks_completed_threads}")
        print(f"Tiempo total con hilos: {fin - inicio:.2f} segundos")

    def run_with_processes(self, tasks):
        processes = []

        inicio = time.time()

        for task_id, difficulty in tasks:
            process = multiprocessing.Process(
                target=self._worker_process,
                args=(task_id, difficulty)
            )
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        fin = time.time()

        print(f"\nTareas completadas con procesos: {self.tasks_completed_processes.value}")
        print(f"Tiempo total con procesos: {fin - inicio:.2f} segundos")


if __name__ == "__main__":

    # Generar 4 tareas con dificultad aleatoria
    tasks = []

    for i in range(1, 5):
        dificultad = random.randint(1, 5)
        tasks.append((i, dificultad))

    print("Tareas generadas:")
    for tarea in tasks:
        print(f"Tarea {tarea[0]} -> Dificultad {tarea[1]}")

    processor = TaskProcessor()

    print("\n========== HILOS ==========")
    processor.run_with_threads(tasks)

    print("\n========== PROCESOS ==========")
    processor.run_with_processes(tasks)

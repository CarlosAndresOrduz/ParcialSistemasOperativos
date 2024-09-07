class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.start_time = None
        self.finish_time = None


def read_processes(file_name):
    processes = []
    with open(file_name, "r") as file:
        for line in file:
            pid, arrival_time, burst_time, priority = map(int, line.split())
            processes.append(Process(pid, arrival_time, burst_time, priority))
    return processes


def mlq_rr_preemptive(processes, tq1, tq2):
    queue1 = []  # Priority Queue 1 (TQ = tq1)
    queue2 = []  # Priority Queue 2 (TQ = tq2)

    # Sort processes by arrival time initially
    processes.sort(key=lambda x: x.arrival_time)

    time = 0
    schedule = []
    waiting_times = []
    turnaround_times = []

    current_process = None
    time_slice = 0

    while processes or queue1 or queue2 or current_process:
        # Add processes to the appropriate queue based on priority and arrival time
        while processes and processes[0].arrival_time <= time:
            process = processes.pop(0)
            if process.priority == 1:
                queue1.append(process)
            else:
                queue2.append(process)

        # Preempt current process if a higher-priority process arrives
        if current_process and queue1 and current_process.priority > 1:
            queue2.insert(0, current_process)  # Preempt and return to queue 2
            current_process = None

        if current_process is None:
            if queue1:  # Get process from queue 1
                current_process = queue1.pop(0)
                time_slice = tq1
            elif queue2:  # Get process from queue 2
                current_process = queue2.pop(0)
                time_slice = tq2

        if current_process:
            if current_process.start_time is None:
                current_process.start_time = max(time, current_process.arrival_time)

            # Execute for the time slice or remaining time, whichever is smaller
            execution_time = min(current_process.remaining_time, time_slice)
            schedule.append((current_process.pid, time, time + execution_time))
            time += execution_time
            current_process.remaining_time -= execution_time

            # Check if the current process has finished
            if current_process.remaining_time == 0:
                current_process.finish_time = time
                waiting_time = current_process.finish_time - current_process.burst_time - current_process.arrival_time
                turnaround_time = current_process.finish_time - current_process.arrival_time
                waiting_times.append(waiting_time)
                turnaround_times.append(turnaround_time)
                current_process = None
            else:
                time_slice -= execution_time
                # If time slice ends, return the process to the queue
                if time_slice == 0:
                    if current_process.priority == 1:
                        queue1.append(current_process)
                    else:
                        queue2.append(current_process)
                    current_process = None
        else:
            if processes:
                time = processes[0].arrival_time

    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)

    return schedule, avg_waiting_time, avg_turnaround_time


# Ejemplo de uso
if __name__ == "__main__":
    processes = read_processes("processes.txt")

    # Time quantum para cada cola
    tq1 = 4  # Quantum de la cola 1 (prioridad 1)
    tq2 = 3  # Quantum de la cola 2 (prioridad 2)

    # Ejecutar la planificación MLQ con RR y expropiación
    schedule, avg_waiting_time, avg_turnaround_time = mlq_rr_preemptive(processes, tq1, tq2)

    # Imprimir el orden de ejecución
    print("Orden de Ejecución:")
    for pid, start, finish in schedule:
        print(f"Proceso {pid}: Tiempo de Inicio = {start}, Tiempo de Finalización = {finish}")

    # Imprimir tiempos promedio
    print(f"\nTiempo de Espera Promedio: {avg_waiting_time:.2f}")
    print(f"Tiempo de Turnaround Promedio: {avg_turnaround_time:.2f}")

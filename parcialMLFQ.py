class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.start_time = None
        self.finish_time = None
        self.current_queue = 1  # Inicia en la cola de mayor prioridad (1)


def read_processes(file_name):
    processes = []
    with open(file_name, "r") as file:
        for line in file:
            pid, arrival_time, burst_time, priority = map(int, line.split())
            processes.append(Process(pid, arrival_time, burst_time, priority))
    return processes


def mlfq_preemptive(processes, tq1, tq2, tq3):
    # Tres colas (se puede agregar más si es necesario)
    queue1 = []  # Cola 1 (TQ = tq1)
    queue2 = []  # Cola 2 (TQ = tq2)
    queue3 = []  # Cola 3 (TQ = tq3)

    # Ordenar procesos por tiempo de llegada
    processes.sort(key=lambda x: x.arrival_time)

    time = 0
    schedule = []
    waiting_times = []
    turnaround_times = []

    current_process = None
    time_slice = 0

    while processes or queue1 or queue2 or queue3 or current_process:
        # Añadir procesos a la cola adecuada según el tiempo de llegada
        while processes and processes[0].arrival_time <= time:
            process = processes.pop(0)
            queue1.append(process)  # Todos los nuevos procesos empiezan en la cola 1

        # Preempt current process if necessary
        if current_process is None:
            if queue1:
                current_process = queue1.pop(0)
                time_slice = tq1
            elif queue2:
                current_process = queue2.pop(0)
                time_slice = tq2
            elif queue3:
                current_process = queue3.pop(0)
                time_slice = tq3

        if current_process:
            if current_process.start_time is None:
                current_process.start_time = max(time, current_process.arrival_time)

            # Ejecutar el proceso por el tiempo de quantum o tiempo restante, lo que sea menor
            execution_time = min(current_process.remaining_time, time_slice)
            schedule.append((current_process.pid, time, time + execution_time))
            time += execution_time
            current_process.remaining_time -= execution_time

            # Si el proceso termina su ejecución
            if current_process.remaining_time == 0:
                current_process.finish_time = time
                waiting_time = current_process.finish_time - current_process.burst_time - current_process.arrival_time
                turnaround_time = current_process.finish_time - current_process.arrival_time
                waiting_times.append(waiting_time)
                turnaround_times.append(turnaround_time)
                current_process = None
            else:
                time_slice -= execution_time
                # Si el quantum termina y el proceso no ha terminado, moverlo a una cola inferior
                if time_slice == 0:
                    if current_process.current_queue == 1:
                        current_process.current_queue = 2
                        queue2.append(current_process)
                    elif current_process.current_queue == 2:
                        current_process.current_queue = 3
                        queue3.append(current_process)
                    current_process = None
        else:
            if processes:
                time = processes[0].arrival_time

    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)

    return schedule, avg_waiting_time, avg_turnaround_time


# Ejemplo de uso
def main():
    processes = read_processes("processes.txt")

    # Time quantum para cada cola
    tq1 = 4  # Quantum de la cola 1 (alta prioridad)
    tq2 = 3  # Quantum de la cola 2 (media prioridad)
    tq3 = 2  # Quantum de la cola 3 (baja prioridad)

    # Ejecutar la planificación MLFQ
    schedule, avg_waiting_time, avg_turnaround_time = mlfq_preemptive(processes, tq1, tq2, tq3)

    # Imprimir el orden de ejecución
    print("Orden de Ejecución:")
    for pid, start, finish in schedule:
        print(f"Proceso {pid}: Tiempo de Inicio = {start}, Tiempo de Finalización = {finish}")

    # Imprimir tiempos promedio
    print(f"\nTiempo de Espera Promedio: {avg_waiting_time:.2f}")
    print(f"Tiempo de Turnaround Promedio: {avg_turnaround_time:.2f}")

main()
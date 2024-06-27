import subprocess
import datetime

# Получаем результат выполнения команды ps aux
result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)

# Разбиваем вывод на строки
lines = result.stdout.split('\n')

# Первая строка - заголовок, последняя строка - пустая
header = lines[0].split()
lines = lines[1:-1]

# Словарь для хранения количества процессов по пользователю
user_processes = {}

# Переменные для хранения общего количества памяти и CPU
total_memory = 0
total_cpu = 0

# Словарь для хранения процессов и их использования памяти и CPU
process_memory = {}
process_cpu = {}

# Проход по всем строкам вывода
for line in lines:
    data = line.split()

    user = data[0]
    memory = float(data[3])
    cpu = float(data[2])
    process = data[10]

    # Обновляем общее использование памяти и CPU
    total_memory += memory
    total_cpu += cpu

    # Обновляем количество процессов по пользователю
    user_processes[user] = user_processes.get(user, 0) + 1

    # Обновляем использование памяти и CPU для каждого процесса
    if process in process_memory:
        process_memory[process] += memory
    else:
        process_memory[process] = memory

    if process in process_cpu:
        process_cpu[process] += cpu
    else:
        process_cpu[process] = cpu

# Находим процесс с максимальным использованием памяти и CPU
max_memory_process = max(process_memory, key=process_memory.get)
max_cpu_process = max(process_cpu, key=process_cpu.get)

# Сортировка пользовательских процессов
sorted_users = sorted(user_processes.keys(), key=user_processes.get, reverse=True)

# Вывод отчёта в стандартный вывод
print("Отчёт о состоянии системы:")
print(f"Пользователи системы: {', '.join(user_processes.keys())}")
print(f"Процессов запущено: {sum(user_processes.values())}")
print("\nПользовательских процессов:")
for user in sorted_users:
    print(f"{user}: {user_processes[user]}")

print(f"\nВсего памяти используется: {total_memory:.1f}%")
print(f"Всего CPU используется: {total_cpu:.1f}%")
print(f"Больше всего памяти использует: ({process_memory[max_memory_process]:.1f}%, {max_memory_process[:20]})")
print(f"Больше всего CPU использует: ({process_cpu[max_cpu_process]:.1f}%, {max_cpu_process[:20]})")

# Записываем отчёт в файл (в названии добавил секунды, т.к. файлы в одной минуте перезаписывались)
now = datetime.datetime.now()
filename = now.strftime("report/%m-%d-%Y-%H:%M:%S-scan.txt")
with open(filename, 'w') as file:
    file.write("Отчёт о состоянии системы:\n")
    file.write(f"Пользователи системы: {', '.join(user_processes.keys())}\n")
    file.write(f"Процессов запущено: {sum(user_processes.values())}\n\n")
    file.write("Пользовательских процессов:\n")
    for user in sorted_users:
        file.write(f"{user}: {user_processes[user]}\n")
    file.write(f"\nВсего памяти используется: {total_memory:.1f}%\n")
    file.write(f"Всего CPU используется: {total_cpu:.1f}%\n")
    file.write(
        f"Больше всего памяти использует: ({process_memory[max_memory_process]:.1f}%, {max_memory_process[:20]})\n")
    file.write(f"Больше всего CPU использует: ({process_cpu[max_cpu_process]:.1f}%, {max_cpu_process[:20]})\n")

print(f"Отчёт сохранён в файле: {filename}")

import json
import time
import threading
from datetime import datetime

def load_data(filename="students.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_top_grades(data, results, lock):
    print("[Таймер] Запуск расчета топ-10 по успеваемости...")
    time.sleep(0.5)  # Имитация задержки
    
    students_avg = []
    for student_id, student_data in data.items():
        students_avg.append((student_id, student_data["name"], student_data["average"]))
    
    students_avg.sort(key=lambda x: x[2], reverse=True)
    
    with lock:
        results["top_grades"] = students_avg[:10]
    print("[Таймер] Расчет топ-10 по успеваемости завершен")

def calculate_top_absences(data, results, lock):
    print("[Таймер] Запуск расчета топ-10 по прогулам...")
    time.sleep(0.3)  # Имитация задержки
    
    students_absences = []
    for student_id, student_data in data.items():
        students_absences.append((student_id, student_data["name"], student_data["total_absences"]))
    
    students_absences.sort(key=lambda x: x[2], reverse=True)
    
    with lock:
        results["top_absences"] = students_absences[:10]
    print("[Таймер] Расчет топ-10 по прогулам завершен")

def calculate_hardest_subjects(data, results, lock):
    print("[Таймер] Запуск расчета самых трудных предметов...")
    time.sleep(0.7)  # Имитация задержки
    
    subject_difficulty = {}
    for student_id, student_data in data.items():
        for subject, info in student_data["grades"].items():
            if subject not in subject_difficulty:
                subject_difficulty[subject] = []
            subject_difficulty[subject].append(info["difficulty"])
    
    avg_difficulty = []
    for subject, difficulties in subject_difficulty.items():
        avg = sum(difficulties) / len(difficulties)
        avg_difficulty.append((subject, round(avg, 2)))
    
    avg_difficulty.sort(key=lambda x: x[1], reverse=True)
    
    with lock:
        results["hardest_subjects"] = avg_difficulty[:10]
    print("[Таймер] Расчет самых трудных предметов завершен")

def print_results(results):
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА УСПЕВАЕМОСТИ СТУДЕНТОВ (ТАЙМЕРЫ)")
    print("="*60)
    
    print("\nТОП-10 ПО УСПЕВАЕМОСТИ (средний балл):")
    print("-"*60)
    for i, (student_id, name, avg) in enumerate(results["top_grades"], 1):
        print(f"{i:2}. {name} ({student_id}): {avg:.2f}")
    
    print("\nТОП-10 ПО ПРОГУЛАМ (общее количество):")
    print("-"*60)
    for i, (student_id, name, absences) in enumerate(results["top_absences"], 1):
        print(f"{i:2}. {name} ({student_id}): {absences} прогулов")
    
    print("\n10 САМЫХ ТРУДНЫХ ПРЕДМЕТОВ (средняя сложность):")
    print("-"*60)
    for i, (subject, difficulty) in enumerate(results["hardest_subjects"], 1):
        print(f"{i:2}. {subject}: {difficulty:.2f}")

def main():
    print("Загрузка данных...")
    data = load_data()
    print(f"Загружено данных о {len(data)} студентах")
    
    print("\nВыполнение расчетов с использованием таймеров...")
    start_time = time.time()
    
    results = {}
    lock = threading.Lock()
    
    # Создаем и запускаем таймеры для каждой задачи
    timer1 = threading.Timer(0.1, calculate_top_grades, args=(data, results, lock))
    timer2 = threading.Timer(0.2, calculate_top_absences, args=(data, results, lock))
    timer3 = threading.Timer(0.1, calculate_hardest_subjects, args=(data, results, lock))
    
    timer1.start()
    timer2.start()
    timer3.start()
    
    # Ждем завершения всех таймеров
    timer1.join()
    timer2.join()
    timer3.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print_results(results)
    print(f"\nВремя выполнения: {execution_time:.4f} секунд")

if __name__ == "__main__":
    main()

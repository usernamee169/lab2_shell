import json
import time
import threading
from datetime import datetime

def load_data(filename="students.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_top_grades(data, results, lock):
    print("[Поток 1] Запуск расчета топ-10 по успеваемости...")
    
    students_avg = []
    for student_id, student_data in data.items():
        students_avg.append((student_id, student_data["name"], student_data["average"]))
    
    students_avg.sort(key=lambda x: x[2], reverse=True)
    
    with lock:
        results["top_grades"] = students_avg[:10]
    print("[Поток 1] Расчет топ-10 по успеваемости завершен")

def calculate_top_absences(data, results, lock):
    print("[Поток 2] Запуск расчета топ-10 по прогулам...")
    
    students_absences = []
    for student_id, student_data in data.items():
        students_absences.append((student_id, student_data["name"], student_data["total_absences"]))
    
    students_absences.sort(key=lambda x: x[2], reverse=True)
    
    with lock:
        results["top_absences"] = students_absences[:10]
    print("[Поток 2] Расчет топ-10 по прогулам завершен")

def calculate_hardest_subjects(data, results, lock):
    print("[Поток 3] Запуск расчета самых трудных предметов...")
    
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
    print("[Поток 3] Расчет самых трудных предметов завершен")

def print_results(results):
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА УСПЕВАЕМОСТИ СТУДЕНТОВ (ПОТОКИ)")
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
    
    print("\nВыполнение расчетов в потоках...")
    start_time = time.time()
    
    results = {}
    lock = threading.Lock()
    
    # Создаем потоки для каждой задачи
    thread1 = threading.Thread(target=calculate_top_grades, args=(data, results, lock))
    thread2 = threading.Thread(target=calculate_top_absences, args=(data, results, lock))
    thread3 = threading.Thread(target=calculate_hardest_subjects, args=(data, results, lock))
    
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Ждем завершения всех потоков
    thread1.join()
    thread2.join()
    thread3.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print_results(results)
    print(f"\nВремя выполнения: {execution_time:.4f} секунд")

if __name__ == "__main__":
    main()

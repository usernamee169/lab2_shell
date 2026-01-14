import json
import time
from datetime import datetime

def load_data(filename="students.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_all(data):
    results = {}
    
    # 1. Топ 10 по успеваемости (средний балл)
    students_avg = []
    for student_id, student_data in data.items():
        students_avg.append((student_id, student_data["name"], student_data["average"]))
    
    students_avg.sort(key=lambda x: x[2], reverse=True)
    results["top_grades"] = students_avg[:10]
    
    # 2. Топ 10 по прогулам
    students_absences = []
    for student_id, student_data in data.items():
        students_absences.append((student_id, student_data["name"], student_data["total_absences"]))
    
    students_absences.sort(key=lambda x: x[2], reverse=True)
    results["top_absences"] = students_absences[:10]
    
    # 3. 10 самых трудных предметов
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
    results["hardest_subjects"] = avg_difficulty[:10]
    
    return results

def print_results(results):
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА УСПЕВАЕМОСТИ СТУДЕНТОВ")
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
    
    print("\nВыполнение расчетов...")
    start_time = time.time()
    
    results = calculate_all(data)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print_results(results)
    print(f"\nВремя выполнения: {execution_time:.4f} секунд")

if __name__ == "__main__":
    main()

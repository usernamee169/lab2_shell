import json
import time
import multiprocessing as mp
from functools import partial

def load_data(filename="students.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def top_by_average_task(data, n=10):
    """Задача для процесса: топ по успеваемости"""
    students = [(sid, info['name'], info['average']) 
               for sid, info in data.items()]
    return sorted(students, key=lambda x: x[2], reverse=True)[:n]

def top_by_absences_task(data, n=10):
    """Задача для процесса: топ по прогулам"""
    students = [(sid, info['name'], info['total_absences']) 
               for sid, info in data.items()]
    return sorted(students, key=lambda x: x[2], reverse=True)[:n]

def difficult_subjects_task(data, n=10):
    """Задача для процесса: сложные предметы"""
    subject_stats = {}
    
    for info in data.values():
        for subject, grades in info['grades'].items():
            if subject not in subject_stats:
                subject_stats[subject] = {'total': 0, 'count': 0}
            subject_stats[subject]['total'] += grades['difficulty']
            subject_stats[subject]['count'] += 1
    
    result = [(subj, stats['total']/stats['count']) 
             for subj, stats in subject_stats.items()]
    return sorted(result, key=lambda x: x[1], reverse=True)[:n]

def run_multiprocess():
    print("=== Многопроцессный анализ ===")
    start = time.time()
    
    # Загружаем данные
    data = load_data()
    
    # Создаем пул процессов
    with mp.Pool(processes=3) as pool:
        # Запускаем задачи параллельно
        future1 = pool.apply_async(top_by_average_task, (data, 5))
        future2 = pool.apply_async(top_by_absences_task, (data, 5))
        future3 = pool.apply_async(difficult_subjects_task, (data, 5))
        
        # Получаем результаты
        top_avg = future1.get()
        top_abs = future2.get()
        top_subj = future3.get()
    
    # Выводим результаты
    print("\nТоп 5 по успеваемости:")
    for i, (sid, name, avg) in enumerate(top_avg, 1):
        print(f"{i}. {name} ({sid}): {avg}")
    
    print("\nТоп 5 по прогулам:")
    for i, (sid, name, absences) in enumerate(top_abs, 1):
        print(f"{i}. {name} ({sid}): {absences} прогулов")
    
    print("\nТоп 5 сложных предметов:")
    for i, (subject, difficulty) in enumerate(top_subj, 1):
        print(f"{i}. {subject}: сложность {difficulty:.1f}")
    
    print(f"\nВремя: {time.time() - start:.3f} сек")

if __name__ == "__main__":
    run_multiprocess()

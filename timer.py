import json
import time
import threading
from common_functions import *


def calculate_average_grade(grades):
    """Расчет среднего балла студента"""
    if not grades:
        return 0
    return sum(grades.values()) / len(grades)

def calculate_total_missed(attendance):
    """Расчет общего количества прогулов"""
    total_missed = 0
    for subject_data in attendance.values():
        total_missed += subject_data['missed']
    return total_missed

def calculate_subject_difficulty(students_data):
    """Расчет сложности предметов (средний балл по предмету)"""
    subject_stats = {}
    
    for student_id, student_data in students_data['students'].items():
        for subject, grade in student_data['grades'].items():
            if subject not in subject_stats:
                subject_stats[subject] = {'total_grade': 0, 'count': 0}
            subject_stats[subject]['total_grade'] += grade
            subject_stats[subject]['count'] += 1
    
    difficulty = {}
    for subject, stats in subject_stats.items():
        difficulty[subject] = stats['total_grade'] / stats['count']
    
    return difficulty

def get_top10_by_grades(students_data):
    """Топ 10 студентов по успеваемости"""
    student_scores = []
    
    for student_id, student_data in students_data['students'].items():
        avg_grade = calculate_average_grade(student_data['grades'])
        student_scores.append({
            'id': student_id,
            'name': student_data['name'],
            'average_grade': avg_grade
        })
    
    # Сортировка по убыванию среднего балла
    student_scores.sort(key=lambda x: x['average_grade'], reverse=True)
    return student_scores[:10]

def get_top10_by_absences(students_data):
    """Топ 10 студентов по прогулам"""
    student_absences = []
    
    for student_id, student_data in students_data['students'].items():
        total_missed = calculate_total_missed(student_data['attendance'])
        student_absences.append({
            'id': student_id,
            'name': student_data['name'],
            'total_missed': total_missed
        })
    
    # Сортировка по убыванию прогулов
    student_absences.sort(key=lambda x: x['total_missed'], reverse=True)
    return student_absences[:10]

def get_top10_difficult_subjects(students_data):
    """10 самых трудных предметов (самые низкие средние баллы)"""
    difficulty = calculate_subject_difficulty(students_data)
    
    # Сортировка по возрастанию среднего балла (самые низкие = самые сложные)
    sorted_difficulty = sorted(difficulty.items(), key=lambda x: x[1])
    return sorted_difficulty[:10]






def analyze_grades_timer(students_data, results):
    """Анализ успеваемости с таймером"""
    print("Таймер: Анализ успеваемости начат")
    time.sleep(0.5)  # Имитация задержки
    results['grades'] = get_top10_by_grades(students_data)
    print("Таймер: Анализ успеваемости завершен")

def analyze_absences_timer(students_data, results):
    """Анализ прогулов с таймером"""
    print("Таймер: Анализ прогулов начат")
    time.sleep(0.5)
    results['absences'] = get_top10_by_absences(students_data)
    print("Таймер: Анализ прогулов завершен")

def analyze_difficulty_timer(students_data, results):
    """Анализ сложности предметов с таймером"""
    print("Таймер: Анализ сложности предметов начат")
    time.sleep(0.5)
    results['difficulty'] = get_top10_difficult_subjects(students_data)
    print("Таймер: Анализ сложности предметов завершен")

def timer_based_analysis(filename='students_data.json'):
    """Анализ с использованием таймеров"""
    print("\n=== Анализ с таймерами ===")
    start_time = time.time()
    
    # Загрузка данных
    students_data = load_from_json(filename)
    results = {}
    
    # Создание и запуск потоков с таймерами
    thread1 = threading.Timer(0.1, analyze_grades_timer, args=(students_data, results))
    thread2 = threading.Timer(0.2, analyze_absences_timer, args=(students_data, results))
    thread3 = threading.Timer(0.3, analyze_difficulty_timer, args=(students_data, results))
    
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Ожидание завершения всех потоков
    thread1.join()
    thread2.join()
    thread3.join()
    
    end_time = time.time()
    
    # Вывод результатов
    print("\nТоп 10 по успеваемости:")
    for i, student in enumerate(results['grades'], 1):
        print(f"{i}. {student['name']}: {student['average_grade']:.2f}")
    
    print("\nТоп 10 по прогулам:")
    for i, student in enumerate(results['absences'], 1):
        print(f"{i}. {student['name']}: {student['total_missed']}%")
    
    print("\n10 самых трудных предметов:")
    for i, (subject, avg_grade) in enumerate(results['difficulty'], 1):
        print(f"{i}. {subject}: {avg_grade:.2f}")
    
    print(f"\nВремя выполнения: {end_time - start_time:.4f} секунд")
    
    return end_time - start_time

if __name__ == "__main__":
    timer_based_analysis()

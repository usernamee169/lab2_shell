'''
1. Используя тип данных dict описать предметную область "успеваемость студентов". Реализовать сохранение и чтение данных из формата json. 
Реализовать запросы: "топ 10 по успеваемости", "топ 10 по прогулам", "10 самых трудных предметов".
Необходимо представить линейное решение задачи и с применением распараллеливания при помощи а) однопоточное программирование, б) процессов.
'''

import json
import random

# генерация данных
def generate_data(num_students=50):
    subjects = ["Математика", "Физика", "Химия", "Информатика", "История"]
    students = {}
    
    for i in range(1, num_students + 1):
        student_id = f"ST{i:03d}"
        grades = {}
        
        for subject in subjects:
            grades[subject] = {
                "grade": random.randint(2, 5),
                "absences": random.randint(0, 10),
                "difficulty": random.randint(1, 10) 
            }
        
        # Общие показатели
        avg_grade = sum(g[1]["grade"] for g in grades.items()) / len(subjects)
        total_absences = sum(g[1]["absences"] for g in grades.items())
        
        students[student_id] = {
            "name": f"Студент {i}",
            "grades": grades,
            "average": round(avg_grade, 2),
            "total_absences": total_absences
        }
    
    return students

def save_json(data, filename="students.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filename="students.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    data = generate_data(30)
    save_json(data)
    print(f"Создано {len(data)} студентов")



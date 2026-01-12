'''
1. Используя тип данных dict описать предметную область "успеваемость студентов". Реализовать сохранение и чтение данных из формата json. 
Реализовать запросы: "топ 10 по успеваемости", "топ 10 по прогулам", "10 самых трудных предметов".
Необходимо представить линейное решение задачи и с применением распараллеливания при помощи а) однопоточное программирование, б) процессов.
'''

import json
import time

class SingleThreadAnalyzer:
    def __init__(self, filename="students.json"):
        with open(filename, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def top_by_average(self, n=10):
        """Топ по среднему баллу"""
        students = [(sid, info['name'], info['average']) 
                   for sid, info in self.data.items()]
        return sorted(students, key=lambda x: x[2], reverse=True)[:n]
    
    def top_by_absences(self, n=10):
        """Топ по прогулам"""
        students = [(sid, info['name'], info['total_absences']) 
                   for sid, info in self.data.items()]
        return sorted(students, key=lambda x: x[2], reverse=True)[:n]
    
    def difficult_subjects(self, n=10):
        """Самые сложные предметы"""
        subject_stats = {}
        
        for info in self.data.values():
            for subject, grades in info['grades'].items():
                if subject not in subject_stats:
                    subject_stats[subject] = {'total': 0, 'count': 0}
                subject_stats[subject]['total'] += grades['difficulty']
                subject_stats[subject]['count'] += 1
        
        result = [(subj, stats['total']/stats['count']) 
                 for subj, stats in subject_stats.items()]
        return sorted(result, key=lambda x: x[1], reverse=True)[:n]
    
    def run(self):
        print("=== Однопоточный анализ ===")
        start = time.time()
        
        print("\nТоп 5 по успеваемости:")
        for i, (sid, name, avg) in enumerate(self.top_by_average(5), 1):
            print(f"{i}. {name} ({sid}): {avg}")
        
        print("\nТоп 5 по прогулам:")
        for i, (sid, name, absences) in enumerate(self.top_by_absences(5), 1):
            print(f"{i}. {name} ({sid}): {absences} прогулов")
        
        print("\nТоп 5 сложных предметов:")
        for i, (subject, difficulty) in enumerate(self.difficult_subjects(5), 1):
            print(f"{i}. {subject}: сложность {difficulty:.1f}")
        
        print(f"\nВремя: {time.time() - start:.3f} сек")

if __name__ == "__main__":
    analyzer = SingleThreadAnalyzer()
    analyzer.run()

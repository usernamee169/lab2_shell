import time
import subprocess

def run_single():
    print("Запуск однопоточного анализа...")
    start = time.time()
    subprocess.run(["python", "single.py"], capture_output=True)
    return time.time() - start

def run_multi():
    print("Запуск многопроцессного анализа...")
    start = time.time()
    subprocess.run(["python", "multiprocess.py"], capture_output=True)
    return time.time() - start

def main():
    print("=== Сравнение производительности ===")
    
    single_time = run_single()
    print(f"Однопоточный: {single_time:.3f} сек\n")
    
    multi_time = run_multi()
    print(f"Многопроцессный: {multi_time:.3f} сек\n")
    
    print("="*40)
    print(f"Ускорение: {single_time/multi_time:.2f}x")
    
    if single_time > multi_time:
        print("✓ Многопроцессная обработка быстрее!")
    else:
        print("⚠ Для малого объема данных однопоточный быстрее")

if __name__ == "__main__":
    main()

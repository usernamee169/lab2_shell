#!/bin/bash
echo -e "\nОднопоточный анализ:"
python3 onepotok.py

echo -e "\nОднопоточный анализ:"
python3 mnogopotok.py
 
echo -e "\nМногопроцессный анализ:"
python3 multiprocc.py

echo -e "\nСравнение производительности:"
python3 timer.py

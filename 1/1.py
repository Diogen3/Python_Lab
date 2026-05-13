raw_input = input("Введите числа через запятую: ")
str_list = raw_input.split(",")# разделяем строку в лист с разделителями ,

porog = int(input("Порог: "))
result = []

for item in str_list:
    num = int(item) # каждый элемент переводим в число
    
    if num < porog:
        result.append(porog)# добавляем в список пороговое число, если оно меньше порогового
    else:
        result.append(num)# добавляем число если оно больше порогового

print("Вывод: ")
print(*result, sep=", ")# вывод списка по элементно с разделителем ,
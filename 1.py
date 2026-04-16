raw_input = input("Введите числа через запятую: ")
str_list = raw_input.split(",")# разделяем строку в лист с разделителями ,

porog = int(input("Порог: "))
result = []

for item in str_list:
    num = int(item.strip())
    
    if num < porog:
        result.append(porog)# добавляем 
    else:
        result.append(num)

print("Вывод: ")
print(*result, sep=", ")
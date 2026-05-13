import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import time  

sampling_rate, signal = wavfile.read('44100.wav')

# Если аудио стерео (2 канала), оставляем только один
if len(signal.shape) > 1:
    signal = signal[:, 0]

# Ввод данных
n_points = int(input("Введите количество отсчетов: "))

# начало отсчета времени на выполнение программы
start_time = time.time()

subset = signal[:n_points] # Берем первые N отсчетов

# Столбчатая диаграмма
plt.figure(figsize=(10, 4))
plt.bar(range(n_points), subset, color='blue')
plt.title('Дискретные отсчеты (Столбчатая диаграмма)')
plt.xlabel('Номер отсчета (n)')
plt.ylabel('Амплитуда (A)')
plt.grid()

# Осциллограмма
time_axis = np.linspace(0, len(signal) / sampling_rate, num=len(signal))
plt.figure(figsize=(10, 4))
plt.plot(time_axis, signal, color='red')
plt.title('Осциллограмма сигнала')
plt.xlabel('Время (секунды)')
plt.ylabel('Амплитуда (A)')
plt.grid()

# Спектральный анализ
spectrum = np.fft.fft(signal) # Выполняет быстрое преобразование Фурье (FFT), переводя сигнал из времени в частоты
spectrum_squared = np.abs(spectrum)**2 # Вычисляет мощность спектра: берет модуль (амплитуду) и возводит в квадрат
freqs = np.fft.fftfreq(len(signal), 1/sampling_rate) # Создает массив частот (шкалу Герц), соответствующий полученному спектру
half = len(freqs) // 2 # Находит индекс середины массива, чтобы оставить только положительные частоты

plt.figure(figsize=(10, 4)) # Создает новое окно для графика размером 10 на 4 дюйма
plt.plot(freqs[:half], spectrum_squared[:half], color='green') # Рисуем график: freqs — по горизонтали, spectrum_squared — по вертикали
plt.title('Спектр мощности ($Re^2 + Im^2$)') # Заголовок над графиком
plt.xlabel('Частота (Герцы)') # Подписывает Ось X
plt.ylabel('Мощность')
plt.grid() # Включает отображение сетки на заднем фоне

# Гистограмма
plt.figure(figsize=(10, 4)) 
plt.hist(signal, bins=100, color='purple', edgecolor='black') 
plt.title('Гистограмма распределения значений')
plt.xlabel('Амплитудный интервал (A)')
plt.ylabel('Количество попаданий')
plt.grid()

end_time = time.time()
execution_time = end_time - start_time

print("Программа выполнена за:",execution_time, "сек")
# Отображение всех окон
plt.show()
print("Добро пожаловать в программу 'Софа математичка'!")
print()

name = input("Введите ваше имя: ")
print(f"Привет, {name}! Давайте решим несколько задач.")
print()

print("Задача 1: Сумма двух чисел")
try:
    num1 = float(input("Введите первое число: "))
    num2 = float(input("Введите второе число: "))
    print(f"Сумма {num1} и {num2} равна: {num1 + num2}")
except ValueError:
    print("Ошибка! Введите корректные числа.")
print()

print("Задача 2: Основные арифметические операции")
try:
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))

    print(f"Сложение: {a} + {b} = {a + b}")
    print(f"Вычитание: {a} - {b} = {a - b}")
    print(f"Умножение: {a} * {b} = {a * b}")

    if b != 0:
        print(f"Деление: {a} / {b} = {a / b}")
        print(f"Целочисленное деление: {a} // {b} = {a // b}")
        print(f"Остаток от деления: {a} % {b} = {a % b}")
    else:
        print("Деление на ноль невозможно!")

    print(f"Возведение в степень: {a} ** {b} = {a ** b}")
except ValueError:
    print("Ошибка! Введите корректные числа.")
print()

print("Задача 3: Проверка чётности числа")
try:
    number = int(input("Введите целое число: "))
    if number % 2 == 0:
        print(f"Число {number} является чётным.")
    else:
        print(f"Число {number} является нечётным.")
except ValueError:
    print("Ошибка! Введите целое число.")
print()

print("Задача 4: Определение знака числа")
try:
    number = float(input("Введите число: "))
    if number > 0:
        print(f"Число {number} положительное.")
    elif number < 0:
        print(f"Число {number} отрицательное.")
    else:
        print("Число равно нулю.")
except ValueError:
    print("Ошибка! Введите корректное число.")
print()

print("Задача 5: Таблица умножения")
try:
    number = int(input("Введите число для таблицы умножения: "))
    print(f"Таблица умножения для числа {number}:")
    for i in range(1, 11):
        print(f"{number} × {i} = {number * i}")
except ValueError:
    print("Ошибка! Введите целое число.")
print()

print("Задача 6: Вычисление факториала")
try:
    n = int(input("Введите неотрицательное целое число: "))

    if n < 0:
        print("Факториал отрицательных чисел не определён.")
    else:
        factorial = 1
        for i in range(1, n + 1):
            factorial *= i
        print(f"{n}! = {factorial}")

        # Вариант с math.factorial
        # import math
        # print(f"{n}! = {math.factorial(n)}")
except ValueError:
    print("Ошибка! Введите целое число.")
print()

print("Задача 7: Проверка на простое число")
try:
    n = int(input("Введите целое число больше 1: "))

    if n <= 1:
        print("Число должно быть больше 1.")
    else:
        is_prime = True
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                is_prime = False
                break

        if is_prime:
            print(f"Число {n} является простым.")
        else:
            print(f"Число {n} является составным.")
except ValueError:
    print("Ошибка! Введите целое число.")
print()

print("Задача 8: Поиск минимума и максимума из трёх чисел")
try:
    num1 = float(input("Введите первое число: "))
    num2 = float(input("Введите второе число: "))
    num3 = float(input("Введите третье число: "))

    if num1 <= num2 and num1 <= num3:
        minimum = num1
    elif num2 <= num1 and num2 <= num3:
        minimum = num2
    else:
        minimum = num3

    if num1 >= num2 and num1 >= num3:
        maximum = num1
    elif num2 >= num1 and num2 >= num3:
        maximum = num2
    else:
        maximum = num3

        """"
            # Находим минимум
            minimum = min(num1, num2, num3)
            # Находим максимум
            maximum = max(num1, num2, num3)

            print(f"Наименьшее число: {minimum}")
            print(f"Наибольшее число: {maximum}")
        """


except ValueError:
    print("Ошибка! Введите корректные числа.")
print()

print(f"Спасибо, {name}! Все задачи выполнены. приходите к Софе математичке еще!")

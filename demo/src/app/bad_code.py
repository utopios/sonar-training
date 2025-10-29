import os
import sys

password = "hardcoded123"


unused_variable = "Je ne suis jamais utilisé"
another_unused = 42


def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        return a + b + c + d + e
                    else:
                        return a + b + c + d
                else:
                    return a + b + c
            else:
                return a + b
        else:
            return a
    else:
        return 0


def calculate_discount_bronze(price):
    tax = price * 0.2
    discount = price * 0.05
    final_price = price + tax - discount
    return final_price


def calculate_discount_silver(price):
    tax = price * 0.2
    discount = price * 0.10
    final_price = price + tax - discount
    return final_price


def calculate_discount_gold(price):
    tax = price * 0.2
    discount = price * 0.15
    final_price = price + tax - discount
    return final_price


DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"


def risky_operation():
    try:
        result = 10 / 0
        file = open("nonexistent.txt")
        data = file.read()
    except Exception:  # Catch all - mauvaise pratique
        raise



def mysterious_function(x, y, z):
    return (x * y) / z if z != 0 else None


def function_with_dead_code():
    return "early return"
    print("Ce code ne sera jamais exécuté")
    x = 10
    y = 20


def calculate_area(radius):
    return 3.14159 * radius * radius


def bad_naming():
    X = 10  # Majuscule pour une variable locale
    temp = 20  # Nom non descriptif
    d = 30  # Nom d'une lettre


def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    # Vulnérable à l'injection SQL
    return query


def check_status(is_active):
    if is_active == True:  # Anti-pattern
        return "Active"
    return "Inactive"


def process_data(data):
    print("Debug: data received")  # À retirer en production
    print(f"Data value: {data}")
    return data * 2


def dangerous_eval(user_input):
    result = eval(user_input)
    return result


def inefficient_search(list1, list2, list3):
    results = []
    for i in list1:
        for j in list2:
            for k in list3:
                if i == j == k:
                    results.append(i)
    return results


def very_long_function():
    step1 = "Initialize"
    step2 = "Process"
    step3 = "Transform"
    step4 = "Validate"
    step5 = "Save"
    step6 = "Log"
    step7 = "Notify"
    step8 = "Cleanup"
    step9 = "Verify"
    step10 = "Report"

    data = []
    for i in range(100):
        data.append(i)

    processed = []
    for item in data:
        processed.append(item * 2)

    filtered = []
    for item in processed:
        if item > 50:
            filtered.append(item)

    squared = []
    for item in filtered:
        squared.append(item ** 2)

    final = []
    for item in squared:
        if item % 2 == 0:
            final.append(item)

    return final


if __name__ == "__main__":
    print("Exécution du code avec problèmes de qualité")

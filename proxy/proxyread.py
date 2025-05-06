import re

def parse_line(line):
    # Шаблон:
    # 1. Поле в угловых скобках <...>
    # 2. Поле в кавычках "..."
    # 3. Обычные непробельные слова
    pattern = r'<[^>]*>|"[^"]*"|\S+'

    # Найти все поля
    matches = re.findall(pattern, line)

    # Удалить кавычки, кроме полей в угловых скобках
    cleaned = []
    for field in matches:
        if field.startswith('<') and field.endswith('>'):
            cleaned.append(field)
        else:
            cleaned.append(field.strip('"'))
    return cleaned

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, 1):
            fields = parse_line(line.strip())
            print(f'Строка {line_number}:')
            for i, field in enumerate(fields):
                print(f'  Поле {i+1}: {field}')
            print()

# Запуск
process_file("F:\\Documents\\python\\FLV\\input\\proxy.csv")
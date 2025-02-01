defcheck_indentation(file_path):
    withopen(file_path, 'r') as file:
        lines = file.readlines()

    for i, line inenumerate(lines):
        if'\t'in line:
            print(f"Tab found on line {i+1}: {line.strip()}")
        elif line.startswith(' ') andlen(line) - len(line.lstrip()) % 4 != 0:
            print(f"Inconsistent spaces on line {i+1}: {line.strip()}")

check_indentation('/Users/rainstar/Project/Python/DogAI/Pages/main.py')

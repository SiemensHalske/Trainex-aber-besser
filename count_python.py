import os

def count_lines(root_path):
    total_lines = 0
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    line_count = len(lines)
                    total_lines += line_count
                    print(f"{file_path}: {line_count} Zeilen")
    return total_lines

# Verwende den Pfad, den du durchsuchen möchtest
root_path = '/home/hendrik/Trainex-aber-besser'
total_lines = count_lines(root_path)
print(f"Total python lines: {total_lines}")

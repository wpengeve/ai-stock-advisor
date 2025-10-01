#!/usr/bin/env python3

# Read the file
with open('app.py', 'r') as f:
    lines = f.readlines()

# Find the main function start
main_start = -1
for i, line in enumerate(lines):
    if line.strip() == 'def main():':
        main_start = i
        break

if main_start == -1:
    print("Main function not found")
    exit(1)

# Find where the main function should end
main_end = -1
for i in range(len(lines)):
    if lines[i].strip().startswith('if __name__ == "__main__":'):
        main_end = i
        break

if main_end == -1:
    print("Main execution block not found")
    exit(1)

print(f"Main function: lines {main_start + 1} to {main_end}")

# Fix indentation for all lines inside main function
for i in range(main_start + 1, main_end):
    line = lines[i]
    if line.strip():  # Only process non-empty lines
        # Remove any existing indentation and add 4 spaces
        lines[i] = '    ' + line.lstrip()

# Write back
with open('app.py', 'w') as f:
    f.writelines(lines)

print("Fixed indentation for entire main function")

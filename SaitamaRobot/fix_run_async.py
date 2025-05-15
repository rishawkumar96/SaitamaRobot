import os
import re

HANDLER_CLASSES = [
    "CommandHandler",
    "MessageHandler",
    "RegexHandler",
    "CustomCommandHandler",
]

def remove_run_async_lines(lines):
    # Remove lines that only have @run_async (with optional whitespace)
    return [line for line in lines if not re.match(r'^\s*@run_async\s*$', line)]

def add_run_async_param(line):
    # Add run_async=True to handler constructor calls if not present
    for handler in HANDLER_CLASSES:
        pattern = rf'({handler}\s*\([^)]*)\)'
        if handler in line:
            # Check if run_async= is already in the parentheses
            if "run_async" not in line:
                # Insert run_async=True before the closing parenthesis
                line = re.sub(pattern, r'\1, run_async=True)', line)
    return line

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = remove_run_async_lines(lines)
    lines = [add_run_async_param(line) for line in lines]

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)

def main():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                print(f"Processing {full_path}")
                process_file(full_path)

if __name__ == "__main__":
    main()

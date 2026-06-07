#!/usr/bin/env python3
"""
Скрипт для создания текстового снапшота репозитория.
Обходит все файлы, игнорируя бинарные и временные данные,
и сохраняет их относительные пути и содержимое в snapshot.txt.
"""

import os
import sys
from pathlib import Path

# Директории, которые полностью исключаются из обхода
IGNORE_DIRS = {
    '__pycache__', '.git', '.idea', 'venv', 'env', '.venv', '.mypy_cache',
    '.pytest_cache', '__pycache__', '.vscode', '.tox', '.eggs', 'build', 'dist'
}

# Расширения файлов, которые считаются бинарными и пропускаются
IGNORE_EXTENSIONS = {
    '.pyc', '.pyo', '.so', '.dll', '.exe', '.bin', '.obj', '.o',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.tiff',
    '.mp3', '.mp4', '.avi', '.mov', '.mkv', '.flv',
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar',
    '.iso', '.img', '.dmg', '.psd', '.ai', '.pdf'
}

# Имя выходного файла (исключается из снапшота)
OUTPUT_FILE = "snapshot.txt"


def is_text_file(file_path: str) -> bool:
    """Проверяет, является ли файл текстовым (UTF-8)."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            # Если нет нулевых байтов и декодируется, считаем текстовым
            if b'\0' in chunk:
                return False
            chunk.decode('utf-8')
        return True
    except (UnicodeDecodeError, OSError):
        return False


def should_ignore_file(file_path: str) -> bool:
    """Определяет, нужно ли игнорировать файл по расширению или имени."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in IGNORE_EXTENSIONS:
        return True
    # Игнорируем сам выходной файл, если он существует
    if os.path.basename(file_path) == OUTPUT_FILE:
        return True
    return False


def collect_files(root_dir: str):
    """Генератор, возвращающий (относительный_путь, абсолютный_путь) для каждого значимого файла."""
    root_path = Path(root_dir).resolve()
    for current_dir, dirs, files in os.walk(root_path):
        # Удаляем игнорируемые директории на месте, чтобы os.walk в них не заходил
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            abs_path = Path(current_dir) / file
            rel_path = abs_path.relative_to(root_path)

            # Пропускаем файлы, которые не нужно включать
            if should_ignore_file(str(abs_path)):
                continue

            # Проверяем, текстовый ли файл (иначе пропускаем)
            if not is_text_file(str(abs_path)):
                print(f"Пропущен бинарный файл: {rel_path}", file=sys.stderr)
                continue

            yield rel_path, abs_path


def create_snapshot(root_dir: str = "."):
    """Создаёт snapshot.txt со всеми текстовыми файлами репозитория."""
    root_path = Path(root_dir).resolve()
    output_path = root_path / OUTPUT_FILE

    # Если файл снапшота уже существует, временно переименуем его,
    # чтобы не читать самого себя. (Проще: просто пропустим при обходе)
    # Но we already ignore by name in should_ignore_file.

    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write(f"# Snapshot of repository: {root_path}\n")
        out_f.write(f"# Created by snapshot script\n\n")

        count = 0
        for rel_path, abs_path in collect_files(root_dir):
            try:
                with open(abs_path, 'r', encoding='utf-8') as in_f:
                    content = in_f.read()
            except Exception as e:
                content = f"[Ошибка чтения файла: {e}]"

            out_f.write(f"\n{'=' * 60}\n")
            out_f.write(f"FILE: {rel_path}\n")
            out_f.write(f"{'=' * 60}\n")
            out_f.write(content)
            out_f.write("\n")  # добавить финальный перевод строки
            count += 1
            print(f"Обработан: {rel_path}")

    print(f"\nСнапшот сохранён в {output_path}")
    print(f"Всего обработано файлов: {count}")


def main():
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "."

    if not os.path.isdir(repo_path):
        print(f"Ошибка: '{repo_path}' не является директорией", file=sys.stderr)
        sys.exit(1)

    create_snapshot(repo_path)


if __name__ == "__main__":
    main()
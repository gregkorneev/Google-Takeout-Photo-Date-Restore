import os
import sys
import json
from datetime import datetime

folder_path = sys.argv[1]

print(f"Получен путь: {folder_path}")

all_files = os.listdir(folder_path)

# Расширения фото и видео
media_extensions = ('.jpg', '.jpeg', '.png', '.heic', '.webp', '.mp4', '.mov', '.avi', '.mkv', '.3gp')

# Отбираем медиа-файлы
media_files = [f for f in all_files if f.lower().endswith(media_extensions)]
json_files = [f for f in all_files if f.lower().endswith('.json')]

# Формируем список имён медиа, которые должны иметь JSON
json_media_names = set(f[:-5] for f in json_files)  # убираем только ".json"

updated_count = 0
skipped_count = 0

for media in media_files:
    if media in json_media_names:
        json_file = os.path.join(folder_path, media + '.json')
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Берём дату из JSON (Google Photo формат)
            if 'photoTakenTime' in data and 'timestamp' in data['photoTakenTime']:
                timestamp = int(data['photoTakenTime']['timestamp'])
            elif 'creationTime' in data and 'timestamp' in data['creationTime']:
                timestamp = int(data['creationTime']['timestamp'])
            else:
                print(f'⚠️ В JSON {json_file} не найдена дата.')
                skipped_count += 1
                continue

            media_path = os.path.join(folder_path, media)

            # Устанавливаем дату создания и изменения файла
            os.utime(media_path, (timestamp, timestamp))
            print(f'✅ Обновлена дата файла: {media}')
            updated_count += 1

        except Exception as e:
            print(f'⚠️ Ошибка при обработке {json_file}: {e}')
            skipped_count += 1
    else:
        print(f'⛔ Пропущен файл (нет соответствующего JSON): {media}')
        skipped_count += 1

print(f'\n✅ Готово! Обновлено файлов: {updated_count}, пропущено: {skipped_count}')
input("\nНажмите Enter для выхода...")

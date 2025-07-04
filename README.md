# WordGLAM: Эксперименты GNN-модели для анализа структуры документов

Эксперименты по обучению модели решающей задачу по распознаванию и анализу структурных элементов в научных публикациях. Основана на наборе данных PubLayNet с интеграцией с библиотекой PageR.

В папках экспериментах файл test_result_*.txt - это результат эксперимента.

## 🌟 Особенности
- Автоматизация подготовки аннотированных данных
- Гибкая система экспериментов
- Визуализация результатов
- Поддержка PDF и изображений

## ⚙️ Зависимости
Требуется установка [PageR](https://github.com/YRL-AIDA/PageR)

## 📂 Набор данных
Используется [PubLayNet](https://github.com/ibm-aur-nlp/PubLayNet):
- PDF-документы
- Растровые изображения страниц
- Разметка структурных элементов

## 🚀 Рабочий процесс
### 0. Настройка параметров системы 
Конфигурация экспериментов задается через папки экспериментов и файл .env:

```bash
EXPERIMENT="exp_04_countTag_and_size_k_big/exp_4_kTag_2"  # Текущий эксперимент

PATH_WORDS_AND_STYLES_JSONS=""  # Не используется (заглушка)
PATH_GRAPHS_JSONS="/home/daniil/micro_publaynet/tmp/big_graph_pdf"  # Директория для JSON-файлов графов

START=0  # Не используется (заглушка)
FINAL=1000  # Не используется (заглушка)

SAVE_FREQUENCY=10  # Частота сохранения модели (каждые 10 эпох)

# Модель классификации стилей (подробнее в документации PageR)
PATH_STYLE_MODEL="/home/daniil/project/PageR/models/style_classmodel_20250121"

# Конфигурация набора данных
PATH_PUBLAYNET="/home/daniil/micro_publaynet/publaynet"  # Корневая директория PubLayNet
PATH_PDF="/home/daniil/micro_publaynet/pdfs/"  # Хранилище PDF-документов
PATH_TEST_DATASET="/home/daniil/micro_publaynet/publaynet"  # Тестовый датасет
PATH_TEST_IMAGES="/home/daniil/micro_publaynet/publaynet/val"  # Валидационные изображения
PATH_TEST_JSON="/home/daniil/micro_publaynet/publaynet/val.json"  # Аннотации валидации
PATH_TEST_PDF="/home/daniil/micro_publaynet/pdfs/dev"  # PDF-файлы для тестирования

GLAM_NODE_MODEL=""  # Не используется (заглушка)
GLAM_EDGE_MODEL=""  # Не используется (заглушка)
GLAM_MODEL="glam_model"  # Имя модели (позволяет тестировать разные этапы обучения)

```

### 1. Подготовка данных
```bash
# Генерация JSON-аннотаций
python script_create_json_publaynet.py
# Извлечение и обогащение признаков
python publaynet_extractor.py
```

### 2. Запуск экспериментов
Способ 1: Через конфигурацию .env

```bash
# Укажите EXPERIMENT в .env
python script_train.py  # обучение
python script_test.py   # тестирование
```

Способ 2: Прямой запуск эксперимента

```bash
# Для экспериментов с автоматической генерацией
python exp_03_countTag_and_size_k/start_more_exp.py

# Внимание! Для exp_03 и exp_04 требуется предварительная очистка:
# Удалите предыдущие результаты экспериментов
```

3. Анализ результатов
```bash
# Визуализация функции потерь
python script_plot_learning.py

# Проверка качества на PDF-документах
python script_plot_document.py -i path/to/document.pdf
```

Рекомендуется использовать виртуальное окружение Python
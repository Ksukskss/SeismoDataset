#### ЗАДАЧА 0 ####
Знакомство с отправной точкой набора данных (http://scardec.projects.sismo.ipgp.fr) #дедлайн 25 ноября 
   
   0. Прочитать статью✅ 
   1. Разобраться со структурой базы данных 
   2. Извлечь список из 2782 в табличном? формате
   3. Придумать наиболее удобный формат, после анализа 1 
#### Задача 1 ####
Придумать способ (функцию) сопоставлению элементов списка 1 из isc.ac.uk 
   
#### ПЛАН ####
1. Изучить инфу #ориентировочный дедлайн? 21 ноября
   - SciKit-Learn
   - Polars
   - ObsPy
   - ...пока все?.. 
2. <details>
   <summary>Настройка окружения ✅</summary> #ориентировочный дедлайн? 23 ноября
    Лучше всего начать с этого, так что пораньше бы - можно попробовать такой набор для старта:
   
   ```bash
   #1. Должен появиться каталог .venv
   uv venv --clear --python 3.12 
   #2. Активация
   source .venv/bin/activate
   #3. Создать каталог проекта и зайти в него
   mkdir ~/project/
   cd ~/project
   #4. Создание окружения и добавление библиотек
   uv init
   uv add polars datasets scikit-learn torch obspy cartopy jupyter
   ```
   </details>
3. Подготовка датасета #ориентировочный дедлайн? 1 декабря
      - Верификация - можем ли мы верить этому "датасету"? Где найти информацию о цунамогенных землетряссениях?
      - Знакомство с `git submodule` ?
      - Выгрузка зеркального каталога для набора данных с ISC (см. ниже) в формате QuakeML.
      - Разбиение набора данных на подмножества (train, validation, test)
4. Базовые подходы ML (стартовый фокус):
   - Naive Bayes (простенький вероятностный)
   - Линейная регрессия
   - Логистическая регрессия
   - Decision trees (бустинг)
#### СКЛАД РЕСУРСОВ ####
- https://huggingface.co/datasets/mnemoraorg/seismic-tsunami-event-linkage - датасет
- https://www.kaggle.com/datasets/ahmeduzaki/global-earthquake-tsunami-risk-assessment-dataset/code - куча тетрадок для этого же датасета на каггле (есть ли там полезные?)
- https://www.isc.ac.uk/iscbulletin/search/catalogue/ - выгрузка полноценного каталога землетрясений (CSV / QuakeML)
- https://developers.google.com/machine-learning/crash-course - структурированный курс от гугл по ml
- https://education.yandex.ru/handbook/ml - хэндбук от яндекс (база ml)

#### Repo structure (предложение) ####
```s
Aboba/
├── 📁 analysis/            # Obsidian vault - thinking & reasoning
│   ├── 0.exploration.md
│   ├── 1.definition.md  
│   └── ...
├── 📁 data/                # Normally I keep data separately but the dataset here is small (just a 40 Kb .csv)
│   ├── 📁 seismic-tsunami-event-linkage   # and since it is on huggingface/kaggle we can use `git submodule` ?
│   ├── 📁 waveform                        # in contrast - these can be rather big binaries - we can gitignore it.
│   └── ...
├── 📁 src/aboba            # Python packaging
│   ├── __init__.py
│   ├── utils.py            # Shared code utilities (prototype phase)
│   └── ...
├── 📁 workflow/            # Notebooks (code cells only) - execution
│   ├── 0.exploration.ipynb
│   ├── 1.definition.ipynb
│   └── ...
├── pyproject.toml
└── README.md
```

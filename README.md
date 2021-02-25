# Сервисы получения продуктовой статистики и предсказания пола клиентов

В рамках проекта создается прототип модели предсказания пола пользователя и реализовывается 2 REST сервиса.

## Прототипирование модели

Код для обработки данных и обучения модели предсказания пола пользователя по данным просмотра продукции на сайте оформлен в виде [Jupyter] блокнота. Внутри блокнота отчет по оценке качества работы модели и файл с самой моделью. В блокноте описана метрика оценки качества модели и методика тестирования.

## Разработка сервисов

В качестве библиотеки для разработки сервисов используется Flask-RESTful.

Схема URL, запросов и ответов изложена ниже.

Оба сервиса реализованы в модуле /src/app.py

## Сервис доступа к данным

1. Создается слой доступа к данным на базе библиотеки SQLAlchemy
2. Реализуется REST сервис, возвращающий количество просмотров в каждой категории `category` в рамках сессии `session_id`. В зависимости от параметра, возвращается либо относительное количество в процентах от общего, либо абсолютные величины

## Предиктивный сервис

Разрабатывается сервис, который принимает на вход идентификатор сессии `session_id`, рассчитывает необходимые параметры для входного вектора модели и возвращает предсказание пола пользователя.

## Инициализация проекта
Для того, чтобы установить необходимое окружение:

1. Создай `stats_and_gender_prediction` с помощью [conda]:
   ```
   conda env create -f environment.yml
   ```
2. Активируй виртуальное окружение с помощью команды:
   ```
   conda activate stats_and_gender_prediction
   ```
## Схема запросов и ответов REST сервисов
| Метод HTTP     | URI  | Действие |
|:---------------|:-----|:---------|
| GET            | http://[hostname]/stats/[session_id]?format=[absolute\|percents] | Возвращает количество посмотров каждой категории для пользователя с сессией session_id. По-умолчанию в абсолютных значениях, но в параметре запроса format можно указать процентное представление.         |
| GET            | http://[hostname]/prediction-gender/[session_id] | Возвращает предсказание пола посетителя на основе данных о просмотре категорий пользователя с сессией session_id         |

### Ответы сервиса статистики
Для absolute:
{
  "views_a": "1", 
  "views_b": "1", 
  "views_c": "1", 
  "views_d": "2"
}
Для percents:
{
  "views_a": "20.0%", 
  "views_b": "20.0%", 
  "views_c": "20.0%", 
  "views_d": "40.0%"
}
### Ответ сервиса предсказания пола
{
  "gender": "female"
}
## Структура проекта

```
├── AUTHORS.md              <- List of developers and maintainers.
├── CHANGELOG.md            <- Changelog to keep track of new features and fixes.
├── LICENSE.txt             <- License as chosen on the command-line.
├── README.md               <- The top-level README for developers.
├── configs                 <- Directory for configurations of model & application.
├── data
│   ├── external            <- Data from third party sources.
│   ├── interim             <- Intermediate data that has been transformed.
│   ├── processed           <- The final, canonical data sets for modeling.
│   └── raw                 <- The original, immutable data dump.
├── docs                    <- Directory for Sphinx documentation in rst or md.
├── environment.yml         <- The conda environment file for reproducibility.
├── models                  <- Trained and serialized models, model predictions,
│                              or model summaries.
├── notebooks               <- Jupyter notebooks. Naming convention is a number (for
│                              ordering), the creator's initials and a description,
│                              e.g. `1.0-fw-initial-data-exploration`.
├── references              <- Data dictionaries, manuals, and all other materials.
├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures             <- Generated plots and figures for reports.
├── scripts                 <- Analysis and production scripts which import the
│                              actual PYTHON_PKG, e.g. train_model.
├── setup.cfg               <- Declarative configuration of your project.
├── setup.py                <- Use `python setup.py develop` to install for development or
|                              or create a distribution with `python setup.py bdist_wheel`.
├── src
│   └── stats_and_gender_prediction <- Actual Python package where the main functionality goes.
├── tests                   <- Unit tests which can be run with `py.test`.
├── .coveragerc             <- Configuration for coverage reports of unit tests.
├── .isort.cfg              <- Configuration for git hook that sorts imports.
└── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
```

[conda]: https://docs.conda.io/
[Jupyter]: https://jupyter.org/
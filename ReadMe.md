# BlogDjango

Это приложение написанное на языке python с помощью django

## Структура проекта
### Проект состоит из следующих основных частей
1. Приложения:
 - `app_blog` - Основное приложение, в котором описана вся логика работы проекта.
Основные элементы app_blog:
 - `static` - Директория для хранения статических объектов;
 - `templates` - Директория для хранения всех шаблонов приложения;
 - `templatetags` - Пакет для хранения пользовательских тэгов;
 - `tests` - Пакет, содержащий тесты для приложения.
2. Документация:
 - `ReadMe.md` - Описание проекта;
 - `requirements.txt` - Текстовый файл, содержащий все зависимости;

## Установка проекта
Чтобы установить исходный код проекта, клонируйте репозиторий с GitHub или введите следующую команду:
```
https://github.com/Khamer-Ivan/Online-Store_Django.git
```
Для того чтобы проект работал корректно, вам необходимо установить зависимости с помощью команды:
```
pip install -r requirements.txt
```

Теперь вы можете запустить сервер, введя команду
```
python manage.py runserver
```

You will be taken to the main menu of the store and will be able to use the entire interface.
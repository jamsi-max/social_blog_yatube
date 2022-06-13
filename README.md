# ✨Social blog yatube✨
### **Cоциальная сеть для блогеров**
##### Стек технологий: 
##### Frontend - **HTML, CSS, JS**
##### Backend - **Django, PostgreSQL**
#
###### **Домашняя страница:** https://dedau.pythonanywhere.com

![](https://github.com/jamsi-max/social_blog_yatube/blob/main/yatube/core/yatube_home_page.png?raw=true)

###### В проекте реализовано

- регистрация и отправка приветственного письма (формат письма с использованием HTML, CSS) на почту;
- подписки на авторов;
- отображения самых просматриваемых постов;
- система лайков;
- счётчик и виджет просмотра постов;
- комментарии постов;
- виджет и счётчик по ip-адресам уникальных посетителей сайта;
- быстрый поиск при первом нажатии клавиш;
- бесконечный скролл с кнопкой «загрузить ещё».

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone https://github.com/jamsi-max/social_blog_yatube.git
```

Cоздать виртуальное окружение:
```sh
python -m venv env
```

Активировать виртуальное окружение:
```sh
venv\Scripts\acrivate
```
Обновить pip:
```sh
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```
Выполнить миграции:
```sh
python manage.py migrate
```
Запустить проект:
```sh
python manage.py runserver
```
#### Автор: 
**© jamsi-max**

Связь с автором(телеграмм): https://t.me/Jony2024

#### Лицензия

MIT
#

# Tree menu
Django app для отображение древовидного меню с любым уровнем вложения.

<details>
<summary>Что делает приложение?</summary>
Функционал:

* Работа с бд PostgreSQL
* Создавать меню можно только в админке. Создавать, удалять, изменять и читать.
* В админ панель добавлены 2 кнопки для удаления и обновление всех объектов. Чтобы корректно отображались пункты меню при изменение объектов.
![2024-03-12_12-58-33](https://github.com/Plutarxi99/tree_menu/assets/132927381/e89ff870-8b57-4a9d-bb60-f72fcfcf38ea)
* Отображение меню одним запросом к базе данных

</details>

> [!IMPORTANT]
> Добавлен файл .env-sample (для использования надо привести к ввиду **<.env>**) с помощью, которого можно настроить работу проекта. В нем лежат настройки (далее идут примеры заполнения полей):
<details>
<summary>Настройки, которые надо установить для работы приложения</summary>

| Значение | Содержание | Примечание |
|-----|-----------|-----:|
|     **SECRET_KEY**| ahrfgyu34hfy3qh4fy4hufy3qfyb3k4f       |     код генерируется командой, которая указана ниже|
|     **POSTGRES_DB**| NAME_BD   |     название базы данных |
|     **POSTGRES_USER**| USER_BD   |     название пользователя базы данных |
|     **POSTGRES_PASSWORD**| PASSWORD_BD   |     пароль базы данных |
|     **POSTGRES_SERVER**| HOST_BD   |     подключение к базе данных |
|     **POSTGRES_DRIVER**| postgresql   |     типы подключение к базе данных PostgreSQL |
|     **SUPERUSER_EMAIL**| email_superuser       |     установить почту суперюзера|
|     **SUPERUSER_PASSWORD**| password_superuser       |     установить пароль суперюзера|
|     **ENV_TYPE**| local/server       |     для докеризации приложения(в будущем)|
|     **HOST_IP**| *       |     установить доверительное ip-адрес|



</details>

<details>

<summary>Как использовать?</summary>

* Переходим в папку где будет лежать код

* Копируем код с git:
  <pre><code>git clone git@github.com:Plutarxi99/tree_menu.git</code></pre>

* Создаем виртуальное окружение:
  <pre><code>python3 -m venv env</code></pre>
  <pre><code>source env/bin/activate</code></pre>

* После установки нужных настроeк в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt </code></pre>

* Создать секретный ключ:
  <pre><code>python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'</code></pre>

* Создать базу данных:
  <pre><code>psql -U postgres</code></pre>
  <pre><code>create database tree_menu;</code></pre>

* Заполнить файл .env и приложение готово к запуску;

* Установить миграции:
  <pre><code>python3 manage.py migrate</code></pre>

* Создать первого пользователя в сервеси. Перейти в файл и исполнить его
  <pre><code>python3 manage.py createsuperuser</code></pre>

* Установить тестовые данные
  <pre><code>python3 manage.py loaddata data_test_menu.json </code></pre>

</details>

<details>

<summary>Что использовалось в приложение?</summary>
Функционал:

* Подключено PostgreSQL
* Установлен dotenv для создания файла .env
</details>

<details>

<summary>Как использовалось в приложение?</summary>
Руководство к действию:

* Переходим по пути menu.views.MenuView и добавляем названия меню, которые хотим добавить
![Screenshot from 2024-03-12 13-08-00](https://github.com/Plutarxi99/tree_menu/assets/132927381/df86b51c-ae66-4a27-abab-62ab24381a9c)
* Добавляем в отображение в html-документ menu/templates/menu/index.html
![Screenshot from 2024-03-12 13-09-42](https://github.com/Plutarxi99/tree_menu/assets/132927381/0e520e44-0bca-4411-8917-d193f3214178)

</details>

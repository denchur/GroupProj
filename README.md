# Проект YaMDb

1. Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

2. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
3. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
4. Добавлять произведения, категории и жанры может только администратор.
5. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
6. Пользователи могут оставлять комментарии к отзывам.
7. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи

# Установка

## Клонирование репозитория

Чтобы склонировать репозиторий на свой локальный компьютер, выполните следующие шаги:

1. Откройте командную строку (терминал) на вашем компьютере.
2. Перейдите в каталог, в который вы хотите склонировать репозиторий.
3. В командной строке выполните следующую команду:

   ```
   git clone git@github.com:Faraday13/api_yamdb.git
   ```

4. Git склонирует репозиторий на ваш компьютер. После завершения процесса вы увидите склонированный репозиторий в выбранном вами каталоге.

## Активация виртуального окружения

1. Перейдите в корневую папку репозитория.
2. Создайте новое виртуальное окружение, выполнив следующую команду:

   ```
   python -m venv env
   ```

3. Активируйте виртуальное окружение. Для Windows выполните:

   ```
   env\Scripts\activate
   ```

   Для macOS и Linux выполните:

   ```
   source env/bin/activate
   ```

   После активации виртуального окружения вы увидите префикс `(env)` в командной строке, указывающий, что вы находитесь внутри виртуального окружения.

## Установка пакетов из requirements.txt

Для установки необходимых пакетов зависимостей проекта выполните следующие шаги:

1. Убедитесь, что ваше виртуальное окружение активировано (см. предыдущий раздел).
2. В командной строке перейдите в корневую папку репозитория (где находится файл `requirements.txt`).
3. Выполните следующую команду для установки всех необходимых пакетов:

   ```
   pip install -r requirements.txt
   ```

Команда `pip install` установит все пакеты, перечисленные в файле `requirements.txt`, и их зависимости.

## Запуск проекта через manage.py

   ```
   python manage.py runserver
   ```
   
# О репозитории

Этот репозиторий содержит код для проекта на Django REST framework. Он предоставляет различные представления (views) и точки (endpoints) для управления жанрами, категориями, названиями (titles), отзывами (reviews), комментариями (comments) и пользователями (users). 

Проект включает следующие файлы:

## views.py

В этом файле содержатся классы представлений для обработки различных API-точек. Он включает следующие классы:

- `GenreViewSet`: набор представлений для управления жанрами.
- `CategoryViewSet`: набор представлений для управления категориями.
- `TitleViewSet`: набор представлений для управления названиями.
- `ReviewViewSet`: набор представлений для управления отзывами.
- `UserViewSet`: набор представлений для управления пользователями.
- `UserRegisterView`: представление для регистрации пользователей.
- `UserReceiveTokenView`: представление для получения токенов аутентификации.
- `CommentViewSet`: набор представлений для управления комментариями.

## urls.py

В этом файле содержатся конфигурации URL для проекта. Он включает следующие URL:

- `/v1/genres`: URL-шаблоны для управления жанрами.
- `/v1/categories`: URL-шаблоны для управления категориями.
- `/v1/titles`: URL-шаблоны для управления названиями.
- `/v1/users`: URL-шаблоны для управления пользователями.
- `/v1/titles/<title_id>/reviews`: URL-шаблоны для управления отзывами, связанными с определенным названием.
- `/v1/titles/<title_id>/reviews/<review_id>/comments`: URL-шаблоны для управления комментариями, связанными с определенным отзывом.
- `/v1/auth/signup/`: URL для регистрации пользователей.
- `/v1/auth/token/`: URL для получения токенов аутентификации.

Обратите внимание, что эти URL относятся к базовому URL проекта.

## Разрешения и сериализаторы

Код также включает пользовательские классы моделей, разрешений и сериализаторы, которые используются в представлениях. 

Чтобы использовать этот код, убедитесь, что у вас установлены Django и Django REST framework. Затем вы можете включить URL из `urls.py` в конфигурацию URL вашего проекта, чтобы использовать API-эндпойнты.

## Авторы
- Данил Гановичев - Auth/Users
- Владимир Золотарев - Review/Comment
- Денис Чуриков  - Categories/Genres/Titles/Models

# Проект Foodgram

## Описание

Приложение-соцсеть с рецептами. Тут можно делиться вашими рецептами, смотреть чужие рецепты, отслеживать любимых авторов, составить список покупок для чужих (или своих) рецептов и много чего еще.

## Технологии
* :snake: Python
  * :lizard: Django + DRF
* :yellow_square: JS (React)
* :elephant: Postgres
* :whale: Docker
* :green_square: Nginx + Gunicorn

## Запуск

1. Клонируйте репо

```
git clone https://github.com/mxshs/foodgram-project-react.git
```

2. Создайте postgres базу данных и заполните .env файл в папке infra

```
psql -U <ваш_пользователь>
CREATE DATABASE <название>
```

```
cd foogram-project-react/infra
touch .env
nano/vi/code .env
```

3. Создайте образы и поднимите контейнер

```
docker-compose up -d
```

:warning: Если у вас не установлен Docker - посетите https://docs.docker.com/engine/install/ :warning:

:warning: На Windows машине перед запуском компоуза запустите Docker :warning:

4. Соберите миграции и подготовьте статику из контейнера web (infra_web_1)

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
```

5. При желании сгрузите дамп в базу данных

```
docker-compose exec web python manage.py shell
```

   * В шелле

```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```

   * В терминале

```
docker cp fixtures.json infra_web_1:/app
docker-compose exec web python manage.py loaddata fixtures.json
```

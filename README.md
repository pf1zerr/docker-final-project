# Фінальний проєкт Docker — III рівень

## Опис
Простий сайт «Мої завдання»: додавання, перегляд та видалення завдань. Дані зберігаються в PostgreSQL навіть після перезапуску контейнерів.

## Структура
- `frontend/` — HTML, CSS, JavaScript, Dockerfile, Nginx reverse proxy.
- `backend/` — Flask API, Dockerfile, requirements.txt.
- `docker-compose.yml` — запуск frontend, backend, PostgreSQL в одній мережі.

## Запуск
1. Встановити Docker Desktop та запустити його.
2. Відкрити термінал у цій папці.
3. Виконати:

```bash
docker compose up --build -d
docker compose ps
```

4. Відкрити http://localhost:8081/.
5. Додати завдання, оновити сторінку — воно залишиться у списку.

## Перевірка
```bash
docker compose ps
docker compose logs backend
docker compose exec backend python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/api/tasks').read().decode())"
```

## Зупинка
```bash
docker compose down
```

Не використовуйте `docker compose down -v`, якщо хочете зберегти базу даних.

## Взаємодія контейнерів
Браузер -> frontend (Nginx, порт 8081) -> backend (Flask, порт 5000 у мережі Docker) -> db (PostgreSQL, порт 5432 у мережі Docker).

Порти backend та db не відкриті назовні. Усі сервіси з'єднані через мережу `app-network`. Для PostgreSQL створено volume `postgres_data`.

## Скриншоти для здачі
1. `docker compose ps` — три працюючі контейнери.
2. Відкритий сайт `http://localhost:8081/` зі списком завдань.
3. Перевірка додавання завдання та збереження після оновлення сторінки.
4. За потреби — `docker compose logs backend`.

**Примітка:** проєкт призначений для локальної навчальної роботи. Пароль БД наведений у Compose для простоти прикладу, для публічного розгортання потрібні secrets/env-файли та інші налаштування безпеки.

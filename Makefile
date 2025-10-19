.PHONY: help install migrate run test clean docker-build docker-up docker-down

help:
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Установить зависимости
	pip install --upgrade pip
	pip install -r requirements.txt

migrate:  ## Применить миграции
	python manage.py migrate

makemigrations:  ## Создать миграции
	python manage.py makemigrations

createsuperuser:  ## Создать суперпользователя
	python manage.py createsuperuser

run:  ## Запустить сервер разработки
	python manage.py runserver

collectstatic:  ## Собрать статические файлы
	python manage.py collectstatic --noinput

test:  ## Запустить тесты
	pytest

test-cov:  ## Запустить тесты с покрытием
	pytest --cov=tasks --cov-report=html --cov-report=term-missing

lint:  ## Проверить код линтером
	flake8 tasks/ task_manager/

format:  ## Форматировать код
	black tasks/ task_manager/

clean:  ## Очистить временные файлы
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage

docker-build:  ## Собрать Docker образы
	docker-compose build

docker-up:  ## Запустить Docker контейнеры
	docker-compose up

docker-up-d:  ## Запустить Docker контейнеры в фоне
	docker-compose up -d

docker-down:  ## Остановить Docker контейнеры
	docker-compose down

docker-logs:  ## Показать логи Docker
	docker-compose logs -f

docker-shell:  ## Открыть shell в контейнере
	docker-compose exec web /bin/bash

docker-migrate:  ## Применить миграции в Docker
	docker-compose exec web python manage.py migrate

docker-test:  ## Запустить тесты в Docker
	docker-compose exec web pytest

docker-clean:  ## Удалить все Docker контейнеры и volumes
	docker-compose down -v

shell:  ## Открыть Django shell
	python manage.py shell

dbshell:  ## Открыть database shell
	python manage.py dbshell

backup:  ## Создать бэкап базы данных
	python manage.py dumpdata > backup_$(shell date +%Y%m%d_%H%M%S).json

restore:  ## Восстановить из бэкапа (использование: make restore FILE=backup.json)
	python manage.py loaddata $(FILE)


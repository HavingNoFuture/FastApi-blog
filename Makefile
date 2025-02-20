makemigrations:
	alembic revision --autogenerate -m "$(msg)"

migrate:
	alembic upgrade $${step:-head}

downgrade:
	alembic downgrade "$(rev)"

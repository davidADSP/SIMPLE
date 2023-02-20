docker-compose exec -e PYTHONPATH=/app:/app/environments/remote/remote app python3 environments/remote/export.py
docker cp $(docker-compose ps -q app | tr -d '\n'):/app/best_model.tflite .

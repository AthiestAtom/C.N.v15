FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_INPUT_BASE_PATH=/model_input \
    MODEL_OUTPUT_BASE_PATH=/model_output \
    MODEL_BIN_PATH=/run_mobility_model

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "mobility_model_api.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

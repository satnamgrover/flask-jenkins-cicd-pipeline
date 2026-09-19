FROM python:3.12-slim

RUN groupadd --system appuser && \
	useradd --system --gid appuser --create-home appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 


COPY --chown=appuser:appuser app/ ./app/

USER appuser


EXPOSE 5000

RUN pip install --no-cache-dir --user gunicorn==23.0.0
ENV PATH="/home/appuser/.local/bin:${PATH}"

CMD ["gunicorn", "--bind", "0.0.0.0:5000","--workers", "2","app.main:app"]

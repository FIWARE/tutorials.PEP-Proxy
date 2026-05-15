FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask PyJWT
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]

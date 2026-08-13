FROM python:3.10-slim

WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Flask application port
EXPOSE 5000

# Start application
CMD ["python", "app.py"]

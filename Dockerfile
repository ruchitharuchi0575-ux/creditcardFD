# Base Python image
FROM python:3.13-slim

# Set container working directory
WORKDIR /app

# Install system utilities (SQLite runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit dashboard port
EXPOSE 8501

# Default startup command
CMD ["streamlit", "run", "scripts/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
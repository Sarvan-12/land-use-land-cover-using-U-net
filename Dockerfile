FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install dashboard requirements
COPY requirements-dashboard.txt .
RUN pip install --no-cache-dir -r requirements-dashboard.txt

# Copy necessary dashboard files and assets
COPY scripts/ ./scripts/
COPY data/analysis_results/area_analysis1.csv ./data/analysis_results/area_analysis1.csv

# Hugging Face Spaces port requirement
EXPOSE 7860

# Start server
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "scripts.dash1:server"]

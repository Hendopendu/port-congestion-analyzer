# FROM python:3.9-slim

# WORKDIR /app

# # Upgrade pip first
# RUN pip install --upgrade pip

# # Copy requirements and install
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Create data directory
# RUN mkdir -p /app/data

# # Copy our scripts
# COPY scripts/ ./scripts/

# # Run the real scraper
# CMD ["python", "scripts/real_scrapper.py"]*/

FROM python:3.9-slim
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/data
COPY scripts/ ./scripts/
# Note: We removed the CMD so you can choose which script to run
FROM python:3.11.6-slim

# Set environment variable to prevent buffering
ENV PYTHONUNBUFFERED 1

# Install system dependencies: curl, php, node, yarn
RUN apt-get update && \
    apt-get install -y curl gnupg2 lsb-release php php-cli php-common php-mbstring php-xml php-curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn typescript && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app

# Expose port
EXPOSE 8000

# Run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

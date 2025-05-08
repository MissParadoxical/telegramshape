FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r docker_resources/requirements.txt

# Environment variables
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "main.py"]
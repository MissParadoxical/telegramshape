FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY docker_resources/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Create data directory for database
RUN mkdir -p data

# Make the start script executable
RUN chmod +x start_bot.sh

# Environment variables
ENV PYTHONUNBUFFERED=1

# Run the bot using our start script
CMD ["./start_bot.sh"]
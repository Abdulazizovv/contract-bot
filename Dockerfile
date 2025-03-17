FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
COPY .env .env

# Run migrations and start the Django bot
CMD ["sh", "-c", "python manage.py migrate && python manage.py app"]

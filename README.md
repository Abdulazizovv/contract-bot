# Telegram Bot & EIMZO Integration

This project consists of two services running inside Docker containers:
- **Telegram Bot**: A Django-based bot handling requests.
- **EIMZO**: A Java-based digital signature service.

## 📂 Project Structure
```
telegram-bot/
├── bot/
├── botapp/
├── core/
├── didoxTokenGenerator/
│   ├── keys/
│   ├── lib/
│   ├── TokenGenerator-1.0-SNAPSHOT.jar
│   ├── Dockerfile
├── documents/
├── media/
├── static/
├── .env
├── .gitignore
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
├── service-account.json
```

## 🚀 Getting Started

### 1️⃣ **Clone the Repository**
```sh
git clone <your-repo-url>
cd telegram-bot
```

### 2️⃣ **Set Up Environment Variables**
Create a `.env` file inside the project root and add necessary configurations.

### 3️⃣ **Build & Run the Docker Containers**
```sh
docker-compose up --build -d
```

### 4️⃣ **Check Running Services**
```sh
docker-compose ps
```
Ensure that both `telegram_bot` and `eimzo` services are running.

## 🛠 Configuration
### **Docker Compose File (`docker-compose.yml`)**
```yaml
version: "3.8"

services:
  telegram_bot:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: telegram_bot
    env_file:
      - .env
    depends_on:
      - eimzo
    restart: unless-stopped

  eimzo:
    build:
      context: ./didoxTokenGenerator
      dockerfile: Dockerfile
    container_name: eimzo_service
    ports:
      - "8080:8080"
    volumes:
      - ./didoxTokenGenerator/keys:/app/keys
    restart: unless-stopped
```

### **Telegram Bot Dockerfile**
```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env .env

CMD ["sh", "-c", "python manage.py migrate && python manage.py app"]
```

### **EIMZO Dockerfile**
```dockerfile
FROM eclipse-temurin:21-jdk

WORKDIR /app

COPY TokenGenerator-1.0-SNAPSHOT.jar /app/TokenGenerator-1.0-SNAPSHOT.jar
COPY lib /app/lib
COPY keys /app/keys

EXPOSE 8080

CMD ["java", "-cp", "TokenGenerator-1.0-SNAPSHOT.jar:lib/*", "org.springframework.boot.loader.JarLauncher"]
```

## 🔄 Restarting Services
If any changes are made, restart the services:
```sh
docker-compose down
docker-compose up --build -d
```

## 🛠 Troubleshooting
### **Telegram Bot Cannot Connect to EIMZO?**
Update API request in Telegram bot:
```python
requests.post("http://eimzo:8080/generate", json=payload)
```

### **Check EIMZO Logs**
```sh
docker-compose logs -f eimzo
```

## 📜 License
This project is licensed under the MIT License.


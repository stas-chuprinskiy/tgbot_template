# Telegram Bot Template

A robust and scalable template for building Telegram bots using FastAPI, featuring webhook support, PostgreSQL and Redis integration, and comprehensive logging.

## 🚀 Features

- **FastAPI Integration**: High-performance asynchronous API with webhook support
- **Database Support**: PostgreSQL for persistent storage and Redis for caching
- **Monitoring & Logging**: 
  - Sentry integration for error tracking
  - Loguru for structured logging
  - Request ID tracking for better debugging
- **Security**: 
  - Webhook secret validation
  - Configurable security settings
- **Infrastructure**: 
  - Docker support
  - Gunicorn configuration for production
  - Environment-based configuration

## 🛠 Requirements

- Python 3.10+
- PostgreSQL
- Redis
- Docker (optional)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tgbot_template.git
cd tgbot_template
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and configure your settings:
```bash
cp src/.env.example src/.env
```

## ⚙️ Configuration

Configure the following environment variables in your `.env` file:

### Required Settings
- `BOT_TOKEN`: Your Telegram Bot token
- `WEBHOOK_BASE_URL`: Base URL for webhook callbacks

### Optional Settings
- Sentry settings for error tracking
- Logging configuration
- Application host/port settings
- Database configurations (PostgreSQL and Redis)

## 📂 Project Structure

```
src/
├── bot/ # Bot-specific logic
│ ├── bot.py # Bot initialization and core setup
│ └── handlers.py # Message handlers
├── core/ # Core functionality
├── schemas/ # Pydantic models
├── services/ # Business logic
├── storages/ # Database interactions
├── main.py # Application entry point
└── cli.py # CLI commands
```

## 🚀 Usage

### Development

Run the bot locally with hot reload:
```bash
python src/main.py
```

### Production

Using Gunicorn:
```bash
gunicorn main:app -c gunicorn.conf.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

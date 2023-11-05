# Telegram bot to send notifications from RabbitMQ

<a href="https://hub.docker.com/r/leontheprofess/aiogram_notice_rabbitmq"><img src="https://img.shields.io/badge/aiogram__notice__rabbitmq
-docker%20hub-blue"></a>

This bot sends notifications received from the RabbitMQ queue. The received message from queue must be in JSON format:

```json
{
  "user_tg_id": "123456789",
  "message": "Hello world!"
}
```

## Requirements:
* Python 3.9 and newer;   
* Systemd init system (optional);  
* Docker (optional).

## Installation:

### Just to test (not recommended)
1. Clone this repo;
2. `cd` to cloned directory;
3. Install all dependencies from `requirements.txt` file;
4. Copy `env_example` to `.env` (with the leading dot), open `.env` and edit the variables;
5. In the terminal: `python -m /bot/bot.py`

### Systemd 
1. Perform steps 1-4 from "just to test" option above;
2. Copy `notice-bot.example.service` to `notice-bot.service` (or whatever your prefer), open it and edit `WorkingDirectory` 
and `ExecStart` directives;
3. Copy (or symlink) that service file to `/etc/systemd/system/` directory;
4. Enable your service `sudo systemctl enable notice-bot --now`;
5. Check that service is running: `systemctl status notice-bot` (can be used without root privileges).

### Docker + Docker Compose
1. Get `docker-compose.example.yml` file and rename it as `docker-compose.yml`;
2. Get `env_example` file, rename it as `.env` (with the leading dot), open it and edit the variables;
3. Run the bot: `docker compose up -d`;
4. Check that container is up and running: `docker compose ps`
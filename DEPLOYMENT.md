# Инструкция по развертыванию Google Word Start

## 📋 Подготовка

### 1. Установка зависимостей

```bash
cd /root/андрей/жена/Гугл\ ворд\ старт
pip3 install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env`:

```bash
cp .env.example .env
nano .env
```

Заполните:
```
GOOGLE_ADS_API_KEY=ваш-api-ключ
GOOGLE_ADS_CUSTOMER_ID=ваш-customer-id
SECRET_KEY=случайный-секретный-ключ
DEBUG=False
PORT=5002
```

### 3. Получение Google Ads API ключей

1. Зайдите в [Google Ads](https://ads.google.com/)
2. Перейдите в раздел API Center
3. Создайте OAuth приложение
4. Получите Client ID и Client Secret
5. Настройте токены доступа

## 🚀 Развертывание на сервере

### Вариант 1: Systemd Service

1. Создайте файл сервиса:

```bash
sudo nano /etc/systemd/system/google-wordstart.service
```

Содержимое:

```ini
[Unit]
Description=Google Word Start Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/root/андрей/жена/Гугл ворд старт
Environment="PATH=/usr/bin:/usr/local/bin"
EnvironmentFile=/root/андрей/жена/Гугл ворд старт/.env
ExecStart=/usr/bin/python3 /root/андрей/жена/Гугл\ ворд\ старт/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Запустите сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable google-wordstart
sudo systemctl start google-wordstart
sudo systemctl status google-wordstart
```

### Вариант 2: Nginx + Gunicorn

1. Установите Gunicorn:

```bash
pip3 install gunicorn
```

2. Создайте файл `gunicorn_config.py`:

```python
bind = "127.0.0.1:5002"
workers = 4
worker_class = "sync"
timeout = 120
```

3. Запустите через Gunicorn:

```bash
gunicorn -c gunicorn_config.py app:app
```

4. Настройте Nginx:

```bash
sudo nano /etc/nginx/sites-available/2msp.online
```

Добавьте в блок server:

```nginx
location /thamini/wordstart {
    proxy_pass http://127.0.0.1:5002;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Для WebSocket (если нужно)
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

Перезагрузите Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 📝 Интеграция с WordPress

### 1. Создание страницы wordstart

1. Войдите в админку WordPress
2. Создайте новую страницу с slug `wordstart`
3. Вставьте содержимое из `wordpress-page.html` в редактор (режим HTML/Code)
4. Опубликуйте страницу

### 2. Добавление карточки на главную страницу

1. Откройте главную страницу thamini для редактирования
2. Вставьте содержимое из `wordpress-card.html` в нужное место
3. Сохраните изменения

Или через виджет:

1. Внешний вид → Виджеты
2. Добавьте виджет "HTML"
3. Вставьте код из `wordpress-card.html`

## 🔧 Проверка работы

1. Проверьте, что сервис запущен:

```bash
sudo systemctl status google-wordstart
```

2. Проверьте логи:

```bash
sudo journalctl -u google-wordstart -f
```

3. Проверьте доступность API:

```bash
curl http://localhost:5002/health
```

4. Откройте в браузере:

- Локально: `http://localhost:5002`
- На сайте: `https://2msp.online/thamini/wordstart`

## 🐛 Решение проблем

### Проблема: Сервис не запускается

```bash
# Проверьте логи
sudo journalctl -u google-wordstart -n 50

# Проверьте права доступа
sudo chown -R www-data:www-data /root/андрей/жена/Гугл\ ворд\ старт

# Проверьте переменные окружения
sudo systemctl show google-wordstart --property=Environment
```

### Проблема: 502 Bad Gateway

1. Проверьте, что приложение запущено:
```bash
sudo systemctl status google-wordstart
```

2. Проверьте порт:
```bash
netstat -tlnp | grep 5002
```

3. Проверьте firewall:
```bash
sudo ufw status
```

### Проблема: API не отвечает

1. Проверьте API ключи в `.env`
2. Проверьте доступность Google Ads API
3. Проверьте логи приложения

## 📊 Мониторинг

### Просмотр логов в реальном времени

```bash
sudo journalctl -u google-wordstart -f
```

### Перезапуск сервиса

```bash
sudo systemctl restart google-wordstart
```

### Остановка сервиса

```bash
sudo systemctl stop google-wordstart
```

## 🔄 Обновление

1. Остановите сервис:
```bash
sudo systemctl stop google-wordstart
```

2. Обновите код:
```bash
cd /root/андрей/жена/Гугл\ ворд\ старт
git pull  # или скопируйте новые файлы
```

3. Обновите зависимости:
```bash
pip3 install -r requirements.txt --upgrade
```

4. Запустите сервис:
```bash
sudo systemctl start google-wordstart
```

## 🔐 Безопасность

1. **Не храните API ключи в коде** - используйте `.env`
2. **Ограничьте доступ к `.env` файлу**:
```bash
chmod 600 .env
```

3. **Используйте HTTPS** для работы с API
4. **Регулярно обновляйте зависимости**:
```bash
pip3 list --outdated
pip3 install --upgrade package-name
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `sudo journalctl -u google-wordstart -n 100`
2. Проверьте конфигурацию Nginx
3. Проверьте доступность порта
4. Проверьте переменные окружения


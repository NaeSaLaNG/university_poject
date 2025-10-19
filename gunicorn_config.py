"""
Конфигурация Gunicorn для Task Manager API.
"""
import multiprocessing

# Сервер
bind = "0.0.0.0:8000"
backlog = 2048

# Воркеры
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 5

# Логирование
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Процесс
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (если нужно)
# keyfile = "/path/to/key.pem"
# certfile = "/path/to/cert.pem"

# Хуки
def on_starting(server):
    """Вызывается при запуске сервера."""
    print("Gunicorn server is starting...")

def on_reload(server):
    """Вызывается при перезагрузке."""
    print("Gunicorn server is reloading...")

def when_ready(server):
    """Вызывается когда сервер готов принимать запросы."""
    print("Gunicorn server is ready!")

def pre_fork(server, worker):
    """Вызывается перед созданием воркера."""
    pass

def post_fork(server, worker):
    """Вызывается после создания воркера."""
    pass

def post_worker_init(worker):
    """Вызывается после инициализации воркера."""
    pass

def worker_int(worker):
    """Вызывается при получении SIGINT или SIGQUIT."""
    pass

def worker_abort(worker):
    """Вызывается при падении воркера."""
    pass

def pre_exec(server):
    """Вызывается перед новым мастер процессом."""
    pass

def pre_request(worker, req):
    """Вызывается перед обработкой запроса."""
    pass

def post_request(worker, req, environ, resp):
    """Вызывается после обработки запроса."""
    pass

def child_exit(server, worker):
    """Вызывается при выходе воркера."""
    pass

def worker_exit(server, worker):
    """Вызывается при выходе воркера."""
    pass

def nworkers_changed(server, new_value, old_value):
    """Вызывается при изменении количества воркеров."""
    pass

def on_exit(server):
    """Вызывается при остановке сервера."""
    print("Gunicorn server is shutting down...")


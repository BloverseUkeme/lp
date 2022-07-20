from decouple import config as env_config
# from config.settings import SERVER_PORT, SERVER_HOST

SERVER_PORT=env_config("SERVER_PORT")
SERVER_HOST=env_config("SERVER_HOST")

bind = f"{SERVER_HOST}:{SERVER_PORT}"
accesslog = "-"
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'
)

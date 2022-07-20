from decouple import config as env_config

DEBUG=True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG



CELERY_BROKER_URL=env_config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND=env_config("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT=["json"]
CELERY_TASK_SERIALIZER="json"
CELERY_RESULT_SERIALIZER="json"
CELERY_CREATE_MISSING_QUEUES=True
CELERY_REDIS_MAX_CONNECTIONS=15
CELERY_IGNORE_RESULT=True
CELERY_STORE_ERRORS_EVEN_IF_IGNORED=True


## defining queus, exchanges and routes
CELERY_QUEUES = {
        "lpage": {
            "exchange": "lpage",
            "exchange_type": "topic",
            "binding_key": "lpage.#"
        },        
}

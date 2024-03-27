CELERY_BROKER_URL = 'redis://mS8Pfiy9qBCBa8AkBNw2tf4FlxlT4S7Y@redis-10133.c259.us-central1-2.gce.cloud.redislabs.com:10133'
CELERY_RESULT_BACKEND = 'redis://mS8Pfiy9qBCBa8AkBNw2tf4FlxlT4S7Y@redis-10133.c259.us-central1-2.gce.cloud.redislabs.com:10133'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
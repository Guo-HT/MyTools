BROKER_URL = 'redis://:guoht990520_2_redis@127.0.0.1:6379/1'  # 中间件 地址
CELERY_RESULT_BACKEND = "redis://:guoht990520_2_redis@127.0.0.1:6379/15"  # 结果存放地址

CELERY_TIMEZONE="Asia/Shanghai"

CELERY_IMPORTS=(
    "celery_tasks.tasks",

)

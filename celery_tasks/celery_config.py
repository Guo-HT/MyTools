from secret import *

BROKER_URL = f'redis://:{redis_passwd}@{redis_ip}:{redis_port}/1'  # 中间件 地址
CELERY_RESULT_BACKEND = f"redis://:{redis_passwd}@{redis_ip}:{redis_port}/15"  # 结果存放地址

CELERY_TIMEZONE="Asia/Shanghai"

CELERY_IMPORTS=(
    "celery_tasks.tasks",

)

from datetime import timedelta

REDIS_PASSWORD = "admin"
REDIS_HOST = "172.20.149.99"
REDIS_PORT = "6379"

# 任务队列
broker_url = (
    f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    if REDIS_PASSWORD
    else f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
)
# celery_task 的定义模块
imports = (
    "todolist.tasks.schedules",
    "todolist.tasks.async_task",
)
# 结果存储
result_backend = (
    f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    if REDIS_PASSWORD
    else f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
)
worker_redirect_stdouts = True
worker_redirect_stdouts_level = "DEBUG"
# celery worker 每次去 redis 取任务的数量
worker_prefetch_multiplier = 10
# 每个 worker 执行了多少次任务后就会死掉，建议数量大一些
worker_max_tasks_per_child = 12000
# celery 任务执行结果的超时时间
result_expires = 3600
# 单个任务的运行时间限制，否则会被杀死
# task_time_limit = 600
# 单个任务的运行时间限制，会报错，可以捕获。
# task_soft_time_limit = 3600
# 任务完成前还是完成后进行确认
task_acks_late = True
task_send_sent_event = True
# celery worker 的并发数，默认是服务器的内核数目, 也是命令行 -c 参数指定的数目
# worker_concurrency = 4
timezone = "Asia/Shanghai"
enable_utc = False
# 任务失败或者超时也确认
task_acks_on_failure_or_timeout = True
broker_connection_retry_on_startup = True
# worker 将不会存储任务状态并返回此任务的值
task_ignore_result = True
# celery 是否拦截系统根日志
# worker_hijack_root_logger = False
# worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
# worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s]%(task_name)s: %(message)s"


# 任务的限制，key 是 celery_task 的 name，值是限制配置
task_annotations = {
    # 删除历史 workflow，以及相关任务
    "task.delete_workflow": {
        "rate_limit": "1/h",
        "soft_time_limit": 600,  # 运行时长限制 soft_time_limit 可以内 catch
        "expires": 3600,  # 上一次的直接跳过
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
    # 检查运行定时 pipeline
    "task.make_timerun_config": {
        "rate_limit": "1/m",
        "soft_time_limit": 300,
        "expires": 300,
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
    # 异步任务，检查在线构建镜像的 docker pod
    "task.check_docker_commit": {
        "rate_limit": "1/s",
        "soft_time_limit": 600,
        "expires": 600,
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
    # 异步任务，检查 notebook 在线构建 pod
    "task.check_notebook_commit": {
        "rate_limit": "1/s",
        "soft_time_limit": 600,
        "expires": 600,
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
    # 异步升级服务
    "task.upgrade_service": {
        "rate_limit": "1/s",
        "soft_time_limit": 3600,
        "expires": 3600,
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
    # 上传 workflow 信息
    "task.upload_workflow": {
        "rate_limit": "10/s",
        "soft_time_limit": 600,
        "expires": 600,
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
    "task.check_pod_terminating": {
        "rate_limit": "1/s",
        "soft_time_limit": 600,
        "expires": 600,
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
    "task.exec_command": {
        "rate_limit": "1/s",
        "soft_time_limit": 600,
        "expires": 600,
        "max_retries": 0,
        "reject_on_worker_lost": False,
    },
}

# 定时任务的配置项，key 为 celery_task 的 name，值是调度配置
beat_schedule = {
    "task_delete_workflow": {
        "task": "task.delete_workflow",  # 定时删除旧的 workflow
        "schedule": timedelta(seconds=2),
    },
    "task_delete_debug_docker": {
        "task": "task.delete_debug_docker",  # 定时删除 debug 的 pod
        "schedule": timedelta(seconds=2),
    },
    "task_make_timerun_config": {
        "task": "task.make_timerun_config",  # 定时产生定时任务的 yaml 信息
        "schedule": timedelta(seconds=2),
    },
    "task_delete_old_data": {
        "task": "task.delete_old_data",  # 定时删除旧数据
        "schedule": timedelta(seconds=2),
    },
    "task_check_pipeline_run": {
        "task": "task.check_pipeline_run",  # 定时检查 pipeline 的运行时长
        "schedule": timedelta(seconds=2),
    },
    "task_watch_gpu": {
        "task": "task.watch_gpu",  # 定时推送 gpu 的使用情况
        "schedule": timedelta(seconds=2),
    },
    "task_watch_pod_utilization": {
        "task": "task.watch_pod_utilization",  # 定时推送低负载利用率的 pod
        "schedule": timedelta(seconds=2),
    },
    "task_check_pod_terminating": {
        "task": "task.check_pod_terminating",
        "schedule": timedelta(seconds=2),
    },
    # 'task_adjust_node_resource': {
    #     'task': 'task.adjust_node_resource',  # 定时在多项目组间进行资源均衡
    #     'schedule': crontab(minute='*/10'),
    # },
    # 'task_push_workspace_size': {
    #     'task': 'task.push_workspace_size',   # 定时推送用户文件大小
    #     'schedule': crontab(minute='10', hour='10'),
    # },
}

# broker_url = 'redis://:admin@172.20.149.99//'
# result_backend = 'rpc://'
# task_serializer = 'json'
# accept_content = ['json']
# result_serializer = 'json'
# timezone = 'Europe/London'
# enable_utc = True
# imports = (
#     "todolist.tasks.schedules"
# )

# beat_schedule = {
#     'task1': {
#         'task': 'myapp.tasks.task1',
#         'schedule': crontab(minute=0, hour=3),  # 每天凌晨 3 点执行
#         'args': (1, 2),
#     },
#     'task2': {
#         'task': 'task.task2',
#         'schedule': timedelta(seconds=2),    # 每隔 10 分钟执行一次
#     },
# }

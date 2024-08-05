import logging

from .celery import app as celery_app


# 删除过期任务
@celery_app.task(name="task.delete_workflow", bind=True)
def delete_workflow(task):
    logging.info("delete_workflow")


@celery_app.task(name="task.delete_debug_docker", bind=True)
def delete_debug_docker(task):
    logging.info("delete_debug_docker")


# 产生定时任务各个时间点的任务配置
@celery_app.task(name="task.make_timerun_config", bind=True)
def make_timerun_config(task):
    logging.info("make_timerun_config")


# 删除过期垃圾数据
@celery_app.task(name="task.delete_old_data", bind=True)
def delete_old_data(task):
    logging.info("delete_old_data")


@celery_app.task(name="task.check_pipeline_run", bind=True)
def check_pipeline_run(task):
    logging.info("check_pipeline_run")


@celery_app.task(name="task.watch_gpu", bind=True)
def watch_gpu(task):
    logging.info("watch_gpu")


@celery_app.task(name="task.watch_pod_utilization", bind=True)
def watch_pod_utilization(task=None):
    logging.info("watch_pod_utilization")


@celery_app.task(name="task.check_pod_terminating", bind=True)
def check_pod_terminating(task):
    logging.info("check_pod_terminating")


# 各项目组之间相互均衡的方案，一台机器上可能并不能被一个项目组占完，所以可能会跑多个项目组的任务
# @celery_app.task(name="task.adjust_node_resource", bind=True)
# def adjust_node_resource(task):
#     logging.info("adjust_node_resource")


# @celery_app.task(name="task.push_workspace_size", bind=True)
# def push_workspace_size(task):
#     logging.info('push_workspace_size')


if __name__ == "__main__":
    pass

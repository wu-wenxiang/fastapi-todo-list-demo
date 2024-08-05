import logging

from .celery import app as celery_app


@celery_app.task(name="task.check_docker_commit", bind=True)
def check_docker_commit(task):
    logging.info("check_docker_commit")


@celery_app.task(name="task.check_notebook_commit", bind=True)
def check_notebook_commit(task):
    logging.info("check_notebook_commit")


@celery_app.task(name="task.upgrade_service", bind=True)
def upgrade_service(task):
    logging.info("upgrade_service")


@celery_app.task(name="task.update_todoelem", bind=True)
def update_todoelem(task):
    logging.info("update_todoelem")


# 真正去做上传动作。
@celery_app.task(name="task.upload_workflow", bind=True)
def upload_workflow(task, timerun_id, pipeline_id):
    logging.info("upload_workflow")


if __name__ == "__main__":
    pass

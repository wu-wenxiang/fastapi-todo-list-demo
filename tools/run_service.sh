set -ex

/usr/local/bin/gunicorn -c /etc/todolist/gunicorn.py todolist.main:app

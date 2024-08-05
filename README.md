# TodoList

## todolist api server

```bash
# 生成配置文件
tox -e genconfig

# pep8-format
tox -e pep8-format

# pep8 及 mypy 检查
tox -e pep8

# 本地开发运行服务
# virtualenv -p /usr/bin/python3.9 .venv
virtualenv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r test-requirements.txt
pip install -e .

sudo mkdir -p /etc/todolist
# cp etc/todolist/todolist.conf.sample /etc/todolist/todolist.conf
cp etc/todolist/todolist.conf.sample etc/todolist/todolist.conf
sudo ln -s `pwd`/etc/todolist/todolist.conf /etc/todolist/todolist.conf
# 按需修改相关信息
uvicorn --reload todolist.main:app --host 0.0.0.0 --port 8000
# 打开浏览器，访问 http://xxx:8000
```

## celery beat and worker

```bash
# 运行 beat 服务
celery --app=todolist.tasks beat --loglevel=info

# 运行 worker 服务
celery -A todolist.tasks worker --loglevel=info --pool=prefork -Ofair -c 20 -n worker@%h
```

## watch service

```bash
# 注意，需要安装 supervisor 包，下面是在 ubuntu 20.04 为例
apt install -y supervisor

# 运行服务
mkdir -p /etc/todolist
cp etc/todolist/supervisord.conf.sample /etc/todolist/supervisord.conf
# 按需编辑 directory 字段值
supervisord -c etc/todolist/supervisord.conf
```

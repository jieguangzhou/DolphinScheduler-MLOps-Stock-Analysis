# DolphinScheduler-MLOps-Stock-Analysis
Stock analysis MLOps system based on DolphinScheduler


Some data will be save to Mysql, so we have to set the mysql Config as environment variables or modify the CONFIG class in file dmsa/db.py directly


**set environment variables**

```shell
export MYSQL_USER=root
export MYSQL_PASSWORD=123456
export MYSQL_HOST=xxxxxxxxxxxxxxx
export MYSQL_PORT=3306
export MYSQL_DATABASE=dolphinscheduler_mlops_stock
```

**modify the CONFIG class**

```python
class CONFIG:
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_HOST = 'xxxxxxxxxxxxxxxx'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'dolphinscheduler_mlops_stock'

```

After preparing the configuration, we need to prepare the python environment

```shell
virtualenv -p /usr/bin/python3 env
source env/bin/activate
pip install -r requirements.txt
```

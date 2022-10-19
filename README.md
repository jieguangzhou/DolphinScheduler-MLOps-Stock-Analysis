# DolphinScheduler-MLOps-Stock-Analysis
Stock analysis MLOps system based on DolphinScheduler

### DMSA

Some data will be save to Mysql, so we have to set the mysql Config as environment variables or modify the CONFIG class in file dmsa/db.py directly

**modify the CONFIG class**

```python
class CONFIG:
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_HOST = 'xxxxxxxxxxxxxxxx'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'dolphinscheduler_mlops_stock'

```

Some data will be save to AWS S3, so we have to add a aws configuration `~/.aws/config`

```
[default]
aws_access_key_id = <YOUR AWS ACCESS KEY> 
aws_secret_access_key = <YOUR AWS SECRET KEY>
region = <YOUR AWS SECRET KEY>
```

After preparing the configuration, we need to prepare the python environment

```shell
virtualenv -p /usr/bin/python3 env
source env/bin/activate
pip install -r requirements.txt
```


### Install DolphinScheduler 3.1.0

[Install DolphinScheduler](https://dolphinscheduler.apache.org/en-us/docs/latest/user_doc/guide/installation/standalone.html)


Before launching the dolphinscheduer, we need to configure the access keys for the SageMaker task plugin. 

Modify the file `standalone-server/conf/common.properties`.

```
# The AWS access key. if resource.storage.type=S3 or use EMR-Task, This configuration is required 
resource.aws.access.key.id=<YOUR AWS ACCESS KEY> 
# The AWS secret access key. if resource.storage.type=S3 or use EMR-Task, This configuration is required 
resource.aws.secret.access.key=<YOUR AWS SECRET KEY>
# The AWS Region to use. if resource.storage.type=S3 or use EMR-Task, This configuration is required 
resource.aws.region=<AWS REGION>
```


### Create SageMaker Pipeline

[pipeline notebook](pydolphin_stock.ipynb)


### Run system

In [PyDolphinScheduler 3.1.0](https://dolphinscheduler.apache.org/python/3.1.0/tutorial.html), we can use YAML files to define workflow.

For example: [dmsa yaml files](pyds)


In this example, we can run `bash pydolphin_init.sh` to run workflow in DolphinScheduler.

After we run the command, we can open '[http://localhost:12345/dolphinscheduler/ui](http://localhost:12345/dolphinscheduler/ui)' to fine the project and workflow.



In fact, we just need to run the pydolphinscheduler to create the workflow


```shell
# Configuration variables, which are applied in yaml files
export STOCK_PROJECT=$(pwd)
# create workflows
pydolphinscheduler yaml -f pyds/run_system.yaml
```

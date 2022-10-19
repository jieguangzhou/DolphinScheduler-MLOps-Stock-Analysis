# /bin/bash

# init config
user=Stock-Analysis
password=123456
tenant=$USER
project_name=pydolphin
api_address=127.0.0.1
api_port=25333

pydolphinscheduler config --set java_gateway.address $api_address
pydolphinscheduler config --set java_gateway.port $api_port

pydolphinscheduler config --set default.user.name $user
pydolphinscheduler config --set default.user.password $password 
pydolphinscheduler config --set default.user.tenant $tenant 

pydolphinscheduler config --set default.workflow.user $user
pydolphinscheduler config --set default.workflow.tenant $tenant 
pydolphinscheduler config --set default.workflow.project $project_name
pydolphinscheduler config --set default.workflow.queue default


export STOCK_PROJECT=$(pwd)
# create workflows
pydolphinscheduler yaml -f pyds/run_system.yaml

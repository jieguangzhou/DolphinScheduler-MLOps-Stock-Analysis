# /bin/bash

# init config
user=sagemaker
password=123456
tenant=lucky
project_name=ds-sagemaker_mlops

pydolphinscheduler config --set default.user.name $user
pydolphinscheduler config --set default.user.password $password 
pydolphinscheduler config --set default.user.tenant $tenant 

pydolphinscheduler config --set default.workflow.user $user
pydolphinscheduler config --set default.workflow.tenant $tenant 
pydolphinscheduler config --set default.workflow.project $project_name
pydolphinscheduler config --set default.workflow.queue default


# create workflows
python pydolphin/create_dag.py -yaml_file pydolphin/config/prepare_datas.yaml
python pydolphin/create_dag.py -yaml_file pydolphin/config/training_model.yaml
python pydolphin/create_dag.py -yaml_file pydolphin/config/recommend_stock.yaml
python pydolphin/create_dag.py -yaml_file pydolphin/config/run_system.yaml


# /bin/bash

# init config
user=sagemaker
password=123456
tenant=lucky
project_name=test_mlops

pydolphinscheduler config --set default.user.name $user
pydolphinscheduler config --set default.user.password $password 
pydolphinscheduler config --set default.user.tenant $tenant 

pydolphinscheduler config --set default.workflow.user $user
pydolphinscheduler config --set default.workflow.tenant $tenant 
pydolphinscheduler config --set default.workflow.project $project_name


# create workflows
python pydophin/create_dag.py -yaml_file pydophin/config/prepare_datas.yaml
python pydophin/create_dag.py -yaml_file pydophin/config/training_model.yaml
python pydophin/create_dag.py -yaml_file pydophin/config/run_system.yaml


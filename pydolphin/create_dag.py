import os
import re

import click
from pydolphinscheduler import tasks
from pydolphinscheduler.core.process_definition import ProcessDefinition
from ruamel import yaml


def load_yaml(yaml_file) -> dict:
    with open(yaml_file, "r") as r_f:
        config = yaml.safe_load(r_f)
    return config


@click.command()
@click.option("-yaml_file")
def create_process_definition(yaml_file):
    config = load_yaml(yaml_file)
    process_params = config["Process"]
    execute = process_params.pop("execute", "submit")
    with ProcessDefinition(**process_params) as pd:
        dependencies = {}
        name2task = {}
        for task_data in config["Tasks"]:
            task_type = task_data["TaskType"]
            task_params = task_data["params"]
            parse_params(task_params)

            task_cls = getattr(tasks, task_type)
            task = task_cls(**task_params)

            deps = task_data.get("dependencies", [])
            if deps:
                dependencies[task.name] = deps
            name2task[task.name] = task

        for downstream_task_name, deps in dependencies.items():
            downstream_task = name2task[downstream_task_name]
            for upstram_task_name in deps:
                upstram_task = name2task[upstram_task_name]
                upstram_task >> downstream_task

        if execute == "submit":
            pd.submit()
        elif execute == "run":
            pd.run()
        else:
            assert False


def parse_params(params):
    for key, value in params.items():
        if isinstance(value, str):
            params[key] = parse_string_param_if_file(value)


def parse_string_param_if_file(string_param: str):
    if string_param.startswith("File"):
        path = re.findall(r"File\(\"(.*?)\"\)", string_param)[0]
        with open(path, "r") as read_file:
            string_param = "".join(read_file)
    return string_param


if __name__ == "__main__":
    create_process_definition()

import re
import os

import click
from pydolphinscheduler import tasks
from pydolphinscheduler.core.process_definition import ProcessDefinition
from ruamel import yaml


class ProcessDefinitionDraw(ProcessDefinition):
    @property
    def task_location(self):
        if not self.tasks:
            return [self.tasks]
        else:
            return [
                {"taskCode": task_code, "x": index * 200, "y": index * 200}
                for index, task_code in enumerate(self.tasks)
            ]


def load_yaml(yaml_file) -> dict:
    with open(yaml_file, "r") as r_f:
        config = yaml.safe_load(r_f)
    return config


@click.command()
@click.option("-yaml_file")
def create_process_definition(yaml_file):
    config = load_yaml(yaml_file)
    process_params = config["Process"]
    is_run = process_params.pop("run", False)
    parse_params(process_params)
    with ProcessDefinitionDraw(**process_params, release_state="offline") as pd:
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
            print(f"create {task_type} task: {task.name}")

        for downstream_task_name, deps in dependencies.items():
            downstream_task = name2task[downstream_task_name]
            for upstram_task_name in deps:
                upstram_task = name2task[upstram_task_name]
                upstram_task >> downstream_task

        pd.submit()
        if is_run:
            print(f"run process: {pd}")
            pd.run()


def parse_params(params):
    for key, value in params.items():
        if isinstance(value, str):
            value = parse_string_param_if_file(value)
            value = parse_string_param_if_env(value)
            params[key] = value

        elif isinstance(value, dict):
            parse_params(value)


def parse_string_param_if_file(string_param: str):
    if string_param.startswith("$File"):
        path = re.findall(r"\$File\{\"(.*?)\"\}", string_param)[0]
        with open(path, "r") as read_file:
            string_param = "".join(read_file)
    return string_param


def parse_string_param_if_env(string_param: str):
    if "$Env" in string_param:
        key = re.findall(r"\$Env\{(.*?)\}", string_param)[0]
        string_param = os.environ.get(key)
    return string_param


if __name__ == "__main__":
    create_process_definition()

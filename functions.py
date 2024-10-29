import json
import argparse
from datetime import datetime


TASKS_FILE: str = "tasks.json"

def init_parse() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
                                prog="task-cli",
                                description="A task tracker",
                                epilog="f"
                                )
    subparsers = parser.add_subparsers( dest="command" )

    parser_add = subparsers.add_parser( "add" , help="Add task" )
    parser_add.add_argument( "description" , type=str , help="Description about the new task" )

    parser_update = subparsers.add_parser( "update" , help="Update a taks" )
    parser_update.add_argument( "id" , type=int , help="Id of the task to be updated" )
    parser_update.add_argument( "description" , type=str , help="New description of the task to be updated" )

    parser_delete = subparsers.add_parser( "delete" , help="Delete a task" )
    parser_delete.add_argument( "id" , type=int , help="Id of the task to be deleted" )

    parser_inprogress = subparsers.add_parser( "mark-in-progress" , help="Mark a task as progress" )
    parser_inprogress.add_argument( "id" , type=int , help="Id of the task to be marked" )

    parser_done = subparsers.add_parser( "mark-done" , help="Mark a task as done" )
    parser_done.add_argument( "id" , type=int , help="Id of the task to be marked" )

    parser_list = subparsers.add_parser( "list" , help="List tasks")
    parser_list.add_argument( "filter" , choices=["all","done","todo","in_progress"] , required=False , default="all" , help="Filter tasks by status" )

    return parser

def load_tasks() -> list:
    try:
        with open( TASKS_FILE , "r" ) as file:
            return json.load(file)

    except ( FileNotFoundError, json.JSONDecodeError):
        return []


def re_count( tasks ) -> list[dict]:

    for i,task in enumerate( tasks , start=1 ):
        if task["id_"] != i:
            task["id_"] = i

    return tasks


def save_tasks( tasks ) -> None:

    with open( TASKS_FILE , "w" ) as file:
        json.dump( re_count(tasks) , file , indent=4 )


def add_task( description:str , status: str = "todo" , createdAt: datetime = datetime.now() , updatedAt: datetime = datetime.now() ) -> None:
    tasks: list[dict] = load_tasks()

    id_ = len(tasks) +1

    tasks.append( {
        "id_": id_ + len(tasks),
        "description": description,
        "status": status,           #todo | in-progress | done
        "createdAt": createdAt,
        "updatedAt": updatedAt
    } )

    save_tasks( tasks )


def list_tasks( tasks ) -> None:

    if tasks:
        for task in tasks:
            string: str = f"{task["id_"]} {task["description"]} {task["status"]}"
            print(string)
    else:
        print("Anything task")


def list_filter_tasks( conf: str = "a" ) -> None:   #a = all; d = done; t = todo; p = in-progress
    if conf not in ("a","d","t","p"):
        raise ValueError("The parameter must be valid\nparameter conf = {conf}")

    tasks: list[dict] = load_tasks()
    filter_tasks: list[dict] | None = None

    match conf:
        case "a":
            filter_tasks = tasks
        case "d":
            filter_tasks = list( filter( lambda task: task["status"] == "done" , tasks ) )
        case "t":
            filter_tasks = list( filter( lambda task: task["status"] == "todo" , tasks ) )
        case "p":
            filter_tasks = list( filter( lambda task: task["status"] == "in-progress" , tasks ) )

    list_tasks( filter_tasks )


def update_task( id_: int , new_description: str ) -> None:

    tasks: list[dict] = load_tasks()

    if 0 <= id_ <= len(tasks):
        raise ValueError("Id does not exist")

    tasks[id_ -1]["description"] = new_description

    save_tasks( tasks )


def delete_task( id_: int ) -> None:

    tasks: list[dict] = load_tasks()

    tasks.pop( id_ -1 )

    save_tasks( tasks )

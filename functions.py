import json
import argparse
from datetime import datetime


TASKS_FILE: str = "tasks.json"

def init_parse() -> argparse.ArgumentParser:
    """
    Function that create an objetc ArgumentParser, With the
    ability to receive commands add, update, delete, mark-done,
    mark-in-progress, list, exit.

    return: An object ArgumentParser with a subparser "command",
    with parses add, update, delete, list, mark-done,
    mark-in-progress, exit; and the arguments id, description,
    filter.
    """

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
    parser_list.add_argument( "filter" , choices=["all","done","todo","in-progress"] , default="all" , help="Filter tasks by status" )

    parser_exit = subparsers.add_parser( "exit" , help="Exit Program" )

    return parser

def load_tasks() -> list[dict]:
    """
    Function that create/loads data from the .json file.

    return: A list of dictionaries, each dictionary
    containing the data of a task: id_, description,
    status, createdAt, updatedAt.
    """

    try:
        with open( TASKS_FILE , "r" ) as file:
            return json.load(file)

    except ( FileNotFoundError, json.JSONDecodeError):
        with open( TASKS_FILE , "w" ) as file:
            return []

def re_count( tasks:list[dict] ) -> list[dict]:
    """
    Function that assigns an id to the tasks in ascending order.

    param: tasks: The tasks to reassign the id.
    type: tasks: list[dict]

    return: A list of dictionaries, each dictionary
    containing the data of a task: id_, description,
    status, createdAt, updatedAt.
    """

    for i,task in enumerate( tasks , start=1 ):
        if task["id_"] != i:
            task["id_"] = i

    return tasks


def save_tasks( tasks: list[dict] ) -> None:
    """
    Function that rewrites the .json with the new data.

    param: tasks: The tasks with which the .json file is to be rewritten.
    type: tasks: list[dict]
    """

    with open( TASKS_FILE , "w" ) as file:
        json.dump( re_count(tasks) , file , indent=4 )


def add_task( description: str , status: str = "todo" , createdAt: datetime = datetime.now() , updatedAt: datetime = datetime.now() ) -> None:
    """
    Function that adds a new task to the .json file
    and save it.

    param: description: Description of the new task.
    type: description: str

    param: status: Status of the taks, default: "todo".
    type: status: str

    param: createdAt: Datetime when the task was created, default: Function execution datetime
    type: datetime

    param: updatedAt: Datetime when the task was updated, default: Function execution datetime
    type: datetime
    """

    tasks: list[dict] = load_tasks()

    id_ = len(tasks) +1

    tasks.append( {
        "id_": id_ + len(tasks),
        "description": description,
        "status": status,           #todo | in-progress | done
        "createdAt": createdAt.strftime('%d/%m/%y %H:%M:%S'),
        "updatedAt": updatedAt.strftime('%d/%m/%y %H:%M:%S')
    } )

    save_tasks( tasks )


def list_tasks( tasks: list[dict] ) -> None:
    """
    Function than prints the tasks line by line.

    param: tasks: Tasks to be printed
    type: tasks: list[dict]
    """

    if tasks:
        for task in tasks:
            string: str = f"{task["id_"]} {task["description"]} {task["status"]}"
            print(string)
    else:
        print("Anything task")


def list_filter_tasks( conf: str = "a" ) -> None:
    """
    Function that filters tasks by status and prints
    them out.

    param: conf: Status by which the tasks are to be filtered.
    a = all; d = done; t = todo; p = in-progress; default: "a"
    type: conf: str

    raise: ValueError: The conf parameter is invalid
    """

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
    """
    Function that changes the description of a task and
    save it.

    param: id_: id of the task to be updated
    type: id_: int

    param: new_description: New description of the task
    type: new_description: str

    raise: ValueError: The id is out of range
    """

    tasks: list[dict] = load_tasks()

    if 0 > id_ >= len(tasks):
        raise ValueError("id does not exist")

    tasks[id_ -1]["description"] = new_description
    tasks[id_ -1]["updatedAt"] = datetime.now().strftime('%d/%m/%y %H:%M:%S')

    save_tasks( tasks )


def delete_task( id_: int ) -> None:
    """
    Function than deletes a task and saves it.

    param: id_: id of the task to be deleted
    type: id_: int

    raise: ValueError: The id is out of range
    """

    tasks: list[dict] = load_tasks()

    if 0 > id_ >= len(tasks):
        raise ValueError("id does not exist")

    tasks.pop( id_ -1 )

    save_tasks( tasks )

def mark_task( id_: int , new_status: str ) -> None:
    """
    Function that changes the status of a task and saves it.

    param: id_: id of the task to be marked
    type: id_: int

    param: new_status: New status of the task
    type: str

    raise: ValueError: The id is out of range
    """

    tasks: list[dict] = load_tasks()

    if 0 > id_ >= len(tasks):
        raise ValueError("id does not exist")

    tasks[ id_ -1 ]["status"] = new_status
    tasks[id_ -1]["updatedAt"] = datetime.now().strftime('%d/%m/%y %H:%M:%S')

    save_tasks( tasks )


def process_input( command_input: str ) -> str:
    """
    Function that changes the spaces in an input for _ if they are between ''.

    param: command_input: The text to process
    type: command_input: str

    return: Returns the processed text as a str
    """

    flag: bool = False                          #Change if detect a '
    input_list: list[str] = list( command_input )
    final_input: str | None = None

    for i,letter in enumerate( command_input ):
        if letter == "'" and not flag:
            flag = True
        elif letter == "'" and flag:
            flag = False

        if flag and letter == " ":
            input_list[i] = "_"

    final_input = "".join( input_list )

    return final_input

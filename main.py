import functions as func
import argparse


def main() -> None:

    #Obtaining the parse
    parser: argparse.ArgumentParser = func.init_parse()

    run = True
    while run:
        print()
        command_input: str = input( "task-cli " )
        #separating the commands
        command_input = func.process_input( command_input )

        try:
            args = parser.parse_args( command_input.split() )
        except:
            continue

        match args.command:
            case "add":
                func.add_task( args.description )
            case "update":
                func.update_task( args.id, args.description )
            case "delete":
                func.delete_task( args.id )
            case "mark-in-progress":
                func.mark_task( args.id , "in-progress" )
            case "mark-done":
                func.mark_task( args.id , "done" )
            case "list":
                print()
                match args.filter:
                    case "all":
                        func.list_filter_tasks()
                    case "done":
                        func.list_filter_tasks( "d" )
                    case "todo":
                        func.list_filter_tasks( "t" )
                    case "in-progress":
                        func.list_filter_tasks( "p" )

            case "exit":
                run = False

if __name__ == "__main__":
    main()

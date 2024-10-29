import functions as func


def main() -> None:

    parser = func.init_parse()

    run = True
    while run:
        command_input = input( "task-cli " )

        args = parser.parse_args( command_input.split() )

        #Continue

if __name__ == "__main__":
    main()

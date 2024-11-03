# Task-Tracker-CLI
A Python CLI program with the ability to store tasks along with their status and description in a .json file using a command line that accepts positional arguments as input.

**Use:**

    task-cli command arguments

**Commands:**

    #add: add a task to the file .json 
    task-cli add '(description of the task)'

    #update: update the description of a task
    task-cli update (id of the task) '(new description)'

    #delete: delete a task of the .json file
    task-cli delete (id of the task)

    #mark-in-progress: change the status of a task to "in-progress"
    task-cli mark-in-progress (id of the task)
        
    #mark-done: change the status of a task to "done"
    task-cli mark-done (id of the task)


    #list: print the tasks line by line
    #filters: all, done, todo, in-progress
    task-cli list (filter)    
            
    #exit: end program
    task-cli exit

https://roadmap.sh/projects/task-tracker

def time_to_dhmsm(run_time):
    """
    Converts the seconds run time to a printable run time string

    Args:
        run_time (int): The overall run time of the algorithm in seconds

    Returns:
        time_string (str): The printable string containing the formatted time
    """

    #accounts for if there is a super fast function which returns a small negative number
    if run_time < 0:
        time_time = 0

    #get the number of days
    days = int(run_time // (60 * 60 * 24))
    #remove days from total
    run_time = run_time % (60 * 60 * 24)
    #get the hours
    hours = int(run_time // (60 * 60))
    #remove the hours from total
    run_time = run_time % (60 * 60)
    #get the minutes 
    minutes = int(run_time // (60))
    #remove the minutes from total
    run_time = run_time % (60)
    #get the remaining as seconds and milliseconds
    seconds = run_time 

    #conditional printing for the length it ran
    if days > 0:
        print_string = f"{days:.0f}d, {hours}h, {minutes}m, {seconds:.3f}s"
    elif hours > 0:
        print_string = f"{hours}h, {minutes}m, {seconds:.3f}s"
    elif minutes > 0:
        print_string = f"{minutes}m, {seconds:.3f}s"
    else:
        print_string = f"{seconds:.3f}s"

    return print_string


def print_time(func, run_time):
    """
    Prints the run time of a function in an aesthetically nice way

    Args:
        func: a function object of the main function being tracked
        run_time (int): The run time of the function 
    """

    #gets the function name and returns empty string if not found
    func_name = func.__name__ if hasattr(func, "__name__") else ""
    time_string = time_to_dhmsm(run_time)

    #TODO - format this dynamically by getting screen information
    print_string = f"====== {func_name} took {time_string} to run ======"

    print(print_string)

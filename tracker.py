import os
import sys
import time

def trace_calls(frame, event, arg):
    if event == 'call':
        # Get the function's module
        module_name = frame.f_globals.get('__name__', '')
        module_file = frame.f_globals.get('__file__', '')
        
        # Determine if this is a standard library module
        is_stdlib = False
        if hasattr(sys, 'stdlib_module_names') and module_name in sys.stdlib_module_names:
            # Python 3.10+ has this attribute
            is_stdlib = True
        elif module_file:
            # For older Python versions, check if the module is in Python's installation directory
            is_stdlib = any(p in module_file for p in sys.path if p and 
                          (p.endswith('site-packages') == False and 
                           'dist-packages' not in p and
                           os.path.join('lib', 'python') in p))
        
        # Get the current file's directory to compare with imported module paths
        current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        
        # Consider it your code if:
        # 1. It's the main module
        # 2. It's in the same directory as your current script
        # 3. It's not from the standard library
        is_your_code = (module_name == '__main__' or 
                       (module_file and os.path.dirname(os.path.abspath(module_file)) == current_dir) or
                       (not is_stdlib and module_file))
        
        if is_your_code:
            print(f"Calling function: {frame.f_code.co_name}")
            print(f"Line number: {frame.f_lineno}")
            print(f"Module: {module_name}")
            print(f"File: {module_file}")
            print()
            
    return trace_calls


def time_to_dhmsm(run_time):
    """
    Converts the seconds run time to a printable run time string

    Args:
        run_time (int): The overall run time of the algorithm in seconds

    Returns:
        time_string (str): The printable string containing the formatted time
    """

    days = int(run_time // (60 * 60 * 24))
    run_time = run_time % (60 * 60 * 24)
    hours = int(run_time // (60 * 60))
    run_time = run_time % (60 * 60)
    minutes = int(run_time // (60))
    run_time = run_time % (60)
    seconds = run_time 

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
    func_name = func.f_globals.get('__name__', '')

    time_string = time_to_dhmsm(run_time)

    #TODO - format this dynamically by getting screen information
    print_string = f"====== {func_name} took {time_string} to run ======"

    print(print_string)


def tracked(func):

    def wrapper(*args, **kwargs):
        sys.settrace(trace_calls)
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        run_time = start_time - end_time
        print_time(func, run_time)
        sys.settrace(None)
        return result
    return wrapper


times = [1234.4, 2300, 3434.242]

for time in times:
    print(f"Testing time {time}s")
    converted_time = time_to_dhmsm(time)
    print(f"Converted to {converted_time}")
    print()


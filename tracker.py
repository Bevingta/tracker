import os
import sys
import time

from utils import time_utils

def trace_calls(frame, event, arg):
    if event == 'call':

        #get the functions typed name
        module_name = frame.f_globals.get('__name__', '')

        #gets the file location of the function
        module_file = frame.f_globals.get('__file__', '')
        
        #determine if this is a standard library module by checking where it is located and if it has tags
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
        
        #prints information if it is a written function
        #TODO - change this to add to a dict or something to print better
        if is_your_code:
            print(f"Calling function: {frame.f_code.co_name}")
            print(f"Line number: {frame.f_lineno}")
            print(f"Module: {module_name}")
            print(f"File: {module_file}")
            print()
            
    return trace_calls


def tracked(func):

    def wrapper(*args, **kwargs):

        #start the tracing of the function
        sys.settrace(trace_calls)

        #gets the initial time before the function starts
        start_time = time.perf_counter()

        #runs the function while tracking
        #returns the function result as well as the stack trace of data flow
        result, stack_trace = func(*args, **kwargs)

        #gets the time once the function has concluded
        end_time = time.perf_counter()

        #calculates the overall run time
        run_time = start_time - end_time

        #stops the tracking so it doesn't track the print_time function
        sys.settrace(None)

        #prints the time in a readable way
        time_utils.print_time(func, run_time)

        #return the result of the function
        return result

    #runs and returns the value from the wrapper funcion for the function
    return wrapper

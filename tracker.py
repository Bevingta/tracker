import sys
import os

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

def tracked(func):

    def wrapper(*args, **kwargs):
        sys.settrace(trace_calls)
        result = func(*args, **kwargs)
        sys.settrace(None)
        return result
    return wrapper


from tracker import tracked

def add_nums(x, y):
    return x + y

@tracked
def main_function():
    print(add_nums(3, 4))
    return 5

result = main_function()
print("file result: ", result)

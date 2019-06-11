def decorator_function(original_function):
    def wrapper_function():
        return original_function()

    return wrapper_function


def display():
    print("In Display Function")


def display2():
    print("In Display 2")


x = 'display'

mydisplay =  decorator_function(display)

mydisplay()

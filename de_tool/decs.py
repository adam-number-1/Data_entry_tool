from typing import Callable
from functools import wraps

def empty_check(func : Callable):

    @wraps(func)
    def wrapper_function(self, *args, **kwargs):
        if not self.object_list:
            return
        
        self.func(*args, **kwargs)
    
    return wrapper_function
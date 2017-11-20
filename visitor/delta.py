class GenericFunction:
    def __init__(self, dispatch_on):
        self.dispatch_on = dispatch_on
        self.handlers = {}

    def dispatch(self, arg_type):
        def decorator(f):
            self.handlers[arg_type] = f
            return f
        return decorator


class PathVisitor(object):
    def __init__(self):
        self.gf = GenericFunction('node')


def dispatch_on(arg_name):
    def dispatch_decorator(f):
        class Wrapper:
            # TODO: Factor this out? Like delta?
            def __init__(self):
                self.handlers = {}
                self.arg_index = f.__code__.co_varnames.index(arg_name)
                print('argnames', f.__code__.co_varnames)
                print('index of', arg_name, self.arg_index)

            def __call__(self, *args, **kwargs):
                # dispatch to handler for type(args[name])
                arg_type = type(args[self.arg_index-1])
                return self.handlers[arg_type](*args, **kwargs)

            def when(self, arg_type):
                def when_decorator(f):
                    self.handlers[arg_type] = f
                return when_decorator

        return Wrapper()

    return dispatch_decorator


class G:
    def __init__(self, value, *children):
        self.value = value
        self.children = children


class H:
    def __init__(self, value):
        self.value = value

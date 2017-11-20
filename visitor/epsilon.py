class Dispatcher:
    def __init__(self, f, arg_name):
        self.handlers = {}
        self.arg_index = f.__code__.co_varnames.index(arg_name)
        print('argnames', f.__code__.co_varnames)
        print('index of', arg_name, self.arg_index)

    # def __call__(self, *args, **kwargs):
    #     # dispatch to handler for type(args[name])
    #     print('Dispatcher.__call__, self', self)
    #     print('Dispatcher.__call__, args', args)
    #
    #     arg_type = type(args[self.arg_index-1])
    #     return self.handlers[arg_type](*args, **kwargs)

    def make_dispatch(self):

        def dispatch(itself, *args, **kwargs):
            # dispatch to handler for type(args[name])
            # print('dispatch(', itself, args, kwargs, ')')
            arg_type = type(args[self.arg_index-1])
            return self.handlers[arg_type](itself, *args, **kwargs)

        dispatch.when = self.when
        return dispatch

    def when(self, arg_type):
        def when_decorator(handler):
            # print('Dispatcher.when.when_decorator, handler', handler)
            # print('Dispatcher.when.when_decorator, handler', handler.__code__.co_varnames)
            self.handlers[arg_type] = handler
            return handler
        return when_decorator

# TODO: Make this a class method of Dispatcher
def dispatch_on(arg_name):
    def dispatch_decorator(f):
        # return Dispatcher(f, arg_name)
        return Dispatcher(f, arg_name).make_dispatch()
    return dispatch_decorator


class G:
    def __init__(self, value, *children):
        self.value = value
        self.children = children


class H:
    def __init__(self, value):
        self.value = value

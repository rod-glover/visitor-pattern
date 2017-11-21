"""
Generic method dispatch decorators. The clever and elegant API filched from
https://chris-lamb.co.uk/posts/visitor-pattern-in-python
"""

class Dispatcher:
    """
    Class that manages dispatching method calls from a generic handler to
    specific handlers based on the type of a named argument in the handler(s).

    This class provides decorators for methods in a client class that define
    a generic handler and specific handlers for a method.

    The decorators provide syntactic sugar for boilerplate code that
    implements a selector (if statements, or a dict) that dispatches calls
    of a generic handler to calls of specific handlers.

    Usage (generic method definition):

        class C:
            @Dispatcher.on('name')
            def method(self, ..., name, ...):
                '''Generic handler: No implementation.'''

            @method.when(Type1)
            def method(self, ..., name, ...):
                '''Specific handler: Implementation for type(name) == Type1'''
                ...

            @method.when(Type2)
            def method(self, ..., name, ...):
                '''Specific handler: Implementation for type(name) == Type2'''
                ...

    Note reuse of method name ``method`` for both generic handler and
    specific handlers. This is not required, but it makes for cleaner code.

    Usage (generic method invocation)::

        c = C()
        c.method(..., name, ...)

    Any number of generic methods can be defined in a class. Each must have
    a distinct name, but can reuse that name for generic and specific method
    definitions.

    It's easy to imagine a more sophisticated version of this class
    that dispatches based on more complicated conditions on the arguments,
    e.g., full and partial method signatures, values of arguments.
    """

    def __init__(self, method, arg_name):
        self.handlers = {}
        arg_index = method.__code__.co_varnames.index(arg_name) - 1

        def dispatch(itself, *args, **kwargs):
            """
            Dispatcher for this instance.
            Dispatches to the handler registered by ``when`` for the type
            of the arg named in ``arg_name``.
            """
            arg_type = type(args[arg_index])
            return self.handlers[arg_type](itself, *args, **kwargs)

        dispatch.when = self.when
        self.dispatch = dispatch

    @classmethod
    def on(cls, arg_name):
        """
        Return a decorator that creates an instance of this class (Dispatch)
        for the argument named ``arg_name`` and (generic) method, and
        which replaces the generic method with the dispatcher.
        """
        def decorator(method):
            return cls(method, arg_name).dispatch

        return decorator

    def when(self, arg_type):
        """
        Return a decorator that registers handlers for this instance
        for args of type ``arg_type``.
        """
        def decorator(handler):
            """
            Register the specific handler for type ``arg_type``.
            Replaces the specific handler with the dispatcher function so that
            registering can be "chained" (if desired) by reusing the name
            of the generic handler (see class method ``on``) as the name
            of each concrete handler.
            """
            self.handlers[arg_type] = handler
            return self.dispatch

        return decorator

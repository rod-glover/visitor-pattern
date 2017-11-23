"""
Generic method dispatch decorators. The clever and elegant API filched from
https://chris-lamb.co.uk/posts/visitor-pattern-in-python
"""

class Dispatcher:
    """
    Class that manages dispatching method calls from a generic handler to
    specific handlers based on either

    - the signature of the method
    - the type of a named argument in the handler(s)

    This class provides decorators for methods in a client class that define
    a generic handler and specific handlers for a method.

    The decorators provide syntactic sugar for boilerplate code that
    implements a selector (if statements, or a dict) that dispatches calls
    of a generic handler to calls of specific handlers.

    Defining a signature dispatcher::

        class C:
            @Dispatcher
            def method(self):
                '''Generic handler: No implementation.'''

            @method.signature(TypeA1, TypeA2, ...)
            def method(self, arg1, arg2, ...):
                '''Specific handler: Implementation for signature (TypeA1, TypeA2, ...)'''
                ...

            @method.signature(TypeB1, TypeB2, ...)
            def method(self, arg1, arg2, ...):
                '''Specific handler: Implementation for signature (TypeB1, TypeB2, ...)'''
                ...

    Defining a named-arg dispatcher::

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

    Note reuse of method name (``method``) for both generic handler and
    specific handlers. This is not required, but it makes for cleaner code.

    Using a dispatcher (signature or named-arg)::

        c = C()
        c.method(...)

    Any number of generic methods can be defined in a class. Each must have
    a distinct name, but can reuse that name for definitions of both generic
    and specific methods.
    """

    def __init__(self, method, arg_name=None):
        self.handlers = {}
        if arg_name:
            self.dispatch = self.make_dispatch_on_named_arg(method, arg_name)
        else:
            self.dispatch = self.make_dispatch_on_signature()

    def make_dispatch_on_signature(self):
        def dispatch_on_signature(*args, **kwargs):
            signature = tuple(map(type, args[1:]))
            return self.handlers[signature](*args, **kwargs)

        dispatch_on_signature.signature = self.signature
        return dispatch_on_signature

    def make_dispatch_on_named_arg(self, method, arg_name):
        def dispatch_on_named_arg(*args, **kwargs):
            """
            Dispatcher for this instance.
            Dispatches to the handler registered by ``when`` for the type
            of the arg named in ``arg_name``.
            """
            arg_index = method.__code__.co_varnames.index(arg_name)
            arg_type = type(args[arg_index])
            return self.handlers[arg_type](*args, **kwargs)

        dispatch_on_named_arg.when = self.when
        return dispatch_on_named_arg

    @classmethod
    def __call__(cls):
        """
        Return a decorator that creates an instance of this class for
        dispatching on method signatures.
        Replaces the generic method with the dispatcher
        """
        def decorator(method):
            return cls(method).dispatch

        return decorator

    def signature(self, *signature):
        def decorator(handler):
            """
            Register the specific handler for signature ``signature``.
            Replaces the specific handler with the dispatcher function so that
            registering can be "chained" (if desired) by reusing the name
            of the generic handler (see class method ``__call__``) as the name
            of each concrete handler.
            """
            self.handlers[signature] = handler
            return self.dispatch

        return decorator

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


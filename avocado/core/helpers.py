def listen_to(topic):
    """Basic decorator to receive events on a topic."""
    def wrapper(f):
        def wrapped_f(*args):
            f(*args)
        wrapped_f.topic = topic
        return wrapped_f
    return wrapper

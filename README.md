Avocado pub/sub experiment
==========================

This is a basic experiment for using pub/sub inside Avocado.

## Configuing

### Install dependencies and set your env

```bash
 $ pip3 install -r requirements.txt
 $ export PTYHONPATH=.:$PYTHONPATH
```

## Testing

Run the following commands in different terminals:

### Start the broker

```bash
 $ python3 avocado/core/broker.py
```

This is the core component that should be started inside Avocado, and will act
like a mailman, registering all the components subscribed to the topics and
sending events to all of them.

### Run the example

```bash
 $ python3 example.py
```

This is "emulating" a remote component, that will subnscribe to the topic
"avocado.foo" and send an event to "avocado.foo.finished". But the reply is not
forwarded becaused there is nobody listening to "avocado.foo.finished".

### Publish something

```bash
 $ python3 pub.py
```

This will send a "hello world" message to "avocado.foo" topic. Keep in mind
that it can be any data structure, as long as it is possible to serialize via
json.

import asyncio

from avocado.core.components import RemoteComponent
from avocado.core.helpers import listen_to


class MyComponent(RemoteComponent):

    @listen_to('avocado.foo')
    def handle_foo(self, data):
        print(data)
        self.publish('avocado.foo.finished', "Data received")


if __name__ == "__main__":
    component = MyComponent()
    asyncio.run(component.start())

class InitCommand():
    def __init__(self, client):
        self.client = client

    def get_name(self):
        raise NotImplementedError

    def run(self, msg):
        raise NotImplementedError


class Command(InitCommand):
    def __init__(self, client, name, text):
        self.client = client
        self.name = name
        self.text = text

    def get_name(self):
        return self.name

    def get_text(self):
        return self.text

    async def run(self, msg, args):
        await self.client.send_message(msg.channel, self.text)

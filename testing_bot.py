from discord import Client
from json import load, dump
from commands import Add, Del, Help
from base_command import Command


class DiscordClient(Client):

    async def on_ready(self):
        print("Bot logged on as: {}".format(self.user.name))
        self.prefix = "!"
        try:
            with open("commands.json", "r") as f:
                command_data = load(f)
        except FileNotFoundError:
            base_json = {'command_list': []}
            with open("commands.json", "w") as f:
                dump(base_json, f)
            with open("commands.json", "r") as f:
                command_data = load(f)
        try:
            with open("permissions.json", "r") as f:
                self.permissions_data = load(f)
        except FileNotFoundError:
            base_json = {
                "permissions": {
                    "manage_command": [],
                    "use_command": ["everyone"]
                }
            }
            with open("permissions.json", "w") as f:
                dump(base_json, f)
                f.close()
            with open("permissions.json", "r") as f:
                self.permissions_data = load(f)
                f.close()
        self.commands = [Add(self), Del(self), Help(self)]
        if len(command_data["command_list"]) >= 1:
            for c in command_data["command_list"]:
                text = command_data["commands"][c]["text"]
                self.commands.append(Command(name=c, text=text))

    async def on_message(self, msg):
        if not msg.content.startswith(self.prefix):
            return
        args = msg.content[len(self.prefix):].strip().split(" ")
        if len(args) < 1 or args[0] == "":
            return
        command = ""
        for c in self.commands:
            if c.get_name() == args[0].lower():
                command = c
        if command == "":
            return
        await command.run(msg, args)

    def save_commands(self):
        with open("commands.json", "w") as f:
            data = {"commands": {}}
            command_list = []
            for c in self.commands:
                if c.get_name() in ["add", "del", "help"]:
                    continue
                command_list.append(c.get_name())
                data["commands"][c.get_name()] = {"text": c.get_text()}
            data["command_list"] = command_list
            dump(data, f)
            f.close()


client = DiscordClient()
client.run("NDc5OTA0OTQzOTEwNjgyNjI0.Dl05XA.sR-5spvUR4hVOkZEafNjZwYOeD0")

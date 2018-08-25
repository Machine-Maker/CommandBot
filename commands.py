from base_command import InitCommand, Command


class Add(InitCommand):
    def get_name(self):
        return "add"

    async def run(self, msg, args):
        if len(args) < 3:
            await self.client.send_message(
                msg.channel, "Use format ``{}add ".format(self.client.prefix) +
                "<CommandName> <TextToOutput>``")
            return
        name = args[1].lower()
        text = " ".join(args[2:])
        self.client.commands.append(
            Command(client=self.client, name=name, text=text))
        self.client.save_commands()
        await self.client.send_message(
            msg.channel,
            "Successfully added the command ``{}{}``"
            .format(self.client.prefix, name)
        )


class Del(InitCommand):
    def get_name(self):
        return "del"

    async def run(self, msg, args):
        if len(args) != 2:
            await self.client.send_message(
                msg.channel, "Use format ``{}del ".format(self.client.prefix) +
                "<CommandName>")
            return
        name = args[1].lower()
        command = ""
        for c in self.client.commands:
            if c.get_name() == name:
                command = c

        if command == "":
            await self.client.send_message(msg.channel, "Command not found!")
            return
        self.client.commands.remove(command)
        self.client.save_commands()
        await self.client.send_message(msg.channel, "Successfully deleted" +
                                       " that command!")


class Help(InitCommand):
    def get_name(self):
        return "help"

    async def run(self, msg, args):
        pass

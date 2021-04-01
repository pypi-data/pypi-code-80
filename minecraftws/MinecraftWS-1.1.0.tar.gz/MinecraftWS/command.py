class Command:
    async def on_command_response(self, request_id: str, body: dict):
        pass

    async def execute_command(self, command_line: str):
        pass
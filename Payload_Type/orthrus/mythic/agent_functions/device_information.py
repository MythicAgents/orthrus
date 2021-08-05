from mythic_payloadtype_container.MythicCommandBase import *

class DeviceInformationArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass


class DeviceInformationCommand(CommandBase):
    cmd = "device_information"
    needs_admin = False
    help_cmd = "device_information"
    description = "Returns a bunch of generic device information including hostname, os version and serial numbers."
    version = 1
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_remove_file = False
    is_upload_file = False
    author = "@rookuu"
    argument_class = DeviceInformationArguments
    attackmapping = []

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass
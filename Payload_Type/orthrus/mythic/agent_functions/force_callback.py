from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *

class ForceCallbackArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass


class ForceCallbackCommand(CommandBase):
    cmd = "force_callback"
    needs_admin = False
    help_cmd = "force_callback"
    description = "Force a callback from an agent."
    version = 1
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_remove_file = False
    is_upload_file = False
    author = "@rookuu"
    argument_class = ForceCallbackArguments
    attackmapping = []

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        print(task.callback.agent_callback_id)

        resp = await MythicRPC().execute_c2rpc(c2_profile="mdm", function_name="force_callback", task_id=task.id, message=task.callback.agent_callback_id)
        print(resp.status)

        task.status = MythicStatus.Completed
        return task

    async def process_response(self, response: AgentResponse):
        pass
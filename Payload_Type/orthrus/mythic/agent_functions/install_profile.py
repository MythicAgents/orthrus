from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *
import json


class InstallProfileArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {
            "file": CommandParameter(
                name="file", type=ParameterType.File, description="profile to install."
            )
        }

    async def parse_arguments(self):
        if len(self.command_line) > 0:
            if self.command_line[0] == "{":
                self.load_args_from_json_string(self.command_line)
            else:
                raise ValueError("Missing JSON arguments")
        else:
            raise ValueError("Missing arguments")


class InstallProfileCommand(CommandBase):
    cmd = "install_profile"
    needs_admin = False
    help_cmd = "install_profile"
    description = "Installs a profile on the device."
    version = 1
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_remove_file = False
    is_upload_file = True
    author = "@rookuu"
    argument_class = InstallProfileArguments
    attackmapping = []

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        try:
            original_file_name = json.loads(task.original_params)["file"]

            file_resp = await MythicRPC().execute("create_file", task_id=task.id,
                file=base64.b64encode(task.args.get_arg("file")).decode(),
                saved_file_name=original_file_name,
                delete_after_fetch=True,
            )

            if file_resp.status != MythicStatus.Success:
                raise Exception("Error from Mythic: " + str(file_resp.error))
        except Exception as e:
            raise Exception("Error from Mythic: " + str(sys.exc_info()[-1].tb_lineno) + str(e))
        return task

    async def process_response(self, response: AgentResponse):
        pass
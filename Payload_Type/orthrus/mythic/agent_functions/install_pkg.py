from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *

class InstallPkgArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {
            "file": CommandParameter(
                name="file", type=ParameterType.File, description="Pkg to install, must be signed. Can use the TLS cert of the MDM server."
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


class InstallPkgCommand(CommandBase):
    cmd = "install_pkg"
    needs_admin = False
    help_cmd = "install_pkg"
    description = "Installs a pkg on the device. The pkg must be signed with the SSL cert of the mdm web server."
    version = 1
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_remove_file = False
    is_upload_file = True
    author = "@rookuu"
    argument_class = InstallPkgArguments
    attackmapping = []

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        original_file_name = json.loads(task.original_params)["file"]

        file_resp = await MythicRPC().execute("create_file", task_id=task.id,
            file=base64.b64encode(task.args.get_arg("file")).decode(),
            saved_file_name=original_file_name,
            delete_after_fetch=True,
        )
        
        if file_resp.status != MythicStatus.Success:
            raise Exception("Error from Mythic: " + response.error_message)

        return task

    async def process_response(self, response: AgentResponse):
        pass
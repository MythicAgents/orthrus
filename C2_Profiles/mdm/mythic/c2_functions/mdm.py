from mythic_c2_container.C2ProfileBase import *

class mdm(C2Profile):
    name = "mdm"
    description = "Speaks to a locally hosted MicroMDM server to issue commands using the Apple Push Nofification service."
    author = "@rookuu"
    is_p2p = False
    is_server_routed = False
    mythic_encrypts = False
    parameters = [
        C2ProfileParameter(
            name="callback_host",
            description="Callback Host",
            default_value="https://domain.com",
            verifier_regex="^https:\/\/.+",
        ),
    ]

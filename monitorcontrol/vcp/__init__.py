import sys
from .vcp_codes import VPCCommand  # noqa: F401
from .vcp_abc import (  # noqa: F401
    VCP,
    VCPError,
    VCPIOError,
    VCPPermissionError,
)

if sys.platform == "win32":
    from .vcp_windows import get_vcps  # noqa: F401
elif sys.platform.startswith("linux"):
    from .vcp_linux import get_vcps  # noqa: F401
else:
    def get_vpcs():
        raise NotImplementedError("Your OS is not supported. Supported OSs are: Windows, Linux")

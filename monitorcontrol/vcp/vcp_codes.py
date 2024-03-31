import sys
from dataclasses import dataclass
from enum import Enum, unique
from typing import Union


@unique
class VCPCodeType(Enum):
    ro = 0
    wo = 1
    rw = 2


@unique
class VCPCodeFunction(Enum):
    c = 0
    nc = 1


@dataclass(frozen=True)
class VCPCode:
    name: str
    desc: str
    value: int
    type: VCPCodeType
    function: VCPCodeFunction

    def readable(self) -> bool:
        t = VCPCodeType
        return self.type is t.ro or self.type is t.rw

    def writeable(self) -> bool:
        t = VCPCodeType
        return self.type is t.wo or self.type is t.rw


__VCP_CODES = [
    VCPCode(
        name="image_factory_default",
        desc="restore factory default image",
        value=0x04,
        type=VCPCodeType.wo,
        function=VCPCodeFunction.nc),
    VCPCode(
        name="image_luminance",
        desc="image luminance",
        value=0x10,
        type=VCPCodeType.rw,
        function=VCPCodeFunction.c),
    VCPCode(
        name="image_contrast",
        desc="image contrast",
        value=0x12,
        type=VCPCodeType.rw,
        function=VCPCodeFunction.c),
    VCPCode(
        name="image_color_preset",
        desc="image color preset",
        value=0x14,
        type=VCPCodeType.rw,
        function=VCPCodeFunction.c),
    VCPCode(
        name="active_control",
        desc="active control",
        value=0x52,
        type=VCPCodeType.ro,
        function=VCPCodeFunction.nc),
    VCPCode(
        name="input_select",
        desc="input select",
        value=0x60,
        type=VCPCodeType.rw,
        function=VCPCodeFunction.nc),
    VCPCode(
        name="image_orientation",
        desc="image orientation",
        value=0xAA,
        type=VCPCodeType.ro,
        function=VCPCodeFunction.nc),
    VCPCode(
        name="display_power_mode",
        desc="display power mode",
        value=0xD6,
        type=VCPCodeType.rw,
        function=VCPCodeFunction.nc),
]


def get_vcp_code(key: Union[str, int]) -> VCPCode:
    if not (isinstance(key, str) or isinstance(key, int)):
        raise TypeError(f"key must be string or int. Got {type(key)}.")
    for code in __VCP_CODES:
        if isinstance(key, str):
            if code.name == key:
                return code
        else:
            if code.value == key:
                return code
    raise LookupError(f"No VCP code matched key: {key}")


def add_vcp_code(newcode: VCPCode):
    for code in __VCP_CODES:
        if newcode.name == code.name:
            raise ValueError(f"VCP code with name {newcode.name} already exists")
        if newcode.value == code.value:
            raise ValueError(f"VCP code with value {newcode.value} already exists")

    __VCP_CODES.append(newcode)


#
# # f strings require python 3.6
# assert sys.version_info >= (3, 6), "f strings require python 3.6"
# # incomplete list of VCP codes from the MCCS specification
# _VCP_CODE_DEFINTIONS = {
#     "image_factory_default": {
#         "name": "restore factory default image",
#         "value": 0x04,
#         "type": "wo",
#         "function": "nc",
#     },
#     "image_luminance": {
#         "name": "image luminance",
#         "value": 0x10,
#         "type": "rw",
#         "function": "c",
#     },
#     "image_contrast": {
#         "name": "image contrast",
#         "value": 0x12,
#         "type": "rw",
#         "function": "c",
#     },
#     "image_color_preset": {
#         "name": "image color preset",
#         "value": 0x14,
#         "type": "rw",
#         "function": "nc",
#     },
#     "active_control": {
#         "name": "active control",
#         "value": 0x52,
#         "type": "ro",
#         "function": "nc",
#     },
#     "input_select": {
#         "name": "input select",
#         "value": 0x60,
#         "type": "rw",
#         "function": "nc",
#     },
#     "image_orientation": {
#         "name": "image orientation",
#         "value": 0xAA,
#         "type": "ro",
#         "function": "nc",
#     },
#     "display_power_mode": {
#         "name": "display power mode",
#         "value": 0xD6,
#         "type": "rw",
#         "function": "nc",
#     },
# }
#
#
# class VCPCode:
#     """
#     Virtual Control Panel code.  Simple container for the control
#     codes defined by the VESA Monitor Control Command Set (MCCS).
#
#     This should be used by getting the code from
#     :py:meth:`get_vcp_code_definition()`
#
#     Args:
#         name: VCP code name.
#
#     Raises:
#         KeyError: VCP code not found.
#     """
#
#     def __init__(self, name: str):
#         self.definition = _VCP_CODE_DEFINTIONS[name]
#
#     def __repr__(self) -> str:
#         return (
#             "virtual control panel code definition. "
#             f"value: {self.value} "
#             f"type: {self.type}"
#             f"function: {self.function}"
#         )
#
#     @property
#     def name(self) -> int:
#         """Friendly name of the code."""
#         return self.definition["name"]
#
#     @property
#     def value(self) -> int:
#         """Value of the code."""
#         return self.definition["value"]
#
#     @property
#     def type(self) -> str:
#         """Type of the code."""
#         return self.definition["type"]
#
#     @property
#     def function(self) -> str:
#         """Function of the code."""
#         return self.definition["function"]
#
#     @property
#     def readable(self) -> bool:
#         """Returns true if the code can be read."""
#         if self.type == "wo":
#             return False
#         else:
#             return True
#
#     @property
#     def writeable(self) -> bool:
#         """Returns true if the code can be written."""
#         if self.type == "ro":
#             return False
#         else:
#             return True

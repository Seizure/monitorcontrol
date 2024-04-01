import pytest
import voluptuous as vol
from monitorcontrol.vcp.vcp_codes import VPCCommand, _VCP_CODE_DEFINTIONS


VCP_CODE_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("value"): int,
        vol.Required("type"): vol.Any("rw", "ro", "wo"),
        vol.Required("function"): vol.Any("c", "nc", "t"),
    }
)


@pytest.fixture(scope="module", params=_VCP_CODE_DEFINTIONS.keys())
def vcp_code(request):
    return VPCCommand(request.param)


def test_vcp_code_schema(vcp_code: VPCCommand):
    VCP_CODE_SCHEMA(vcp_code.definition)


@pytest.mark.parametrize("property", ["name", "value", "type", "function"])
def test_properties(vcp_code: VPCCommand, property: str):
    getattr(vcp_code, property)


def test_repr(vcp_code: VPCCommand):
    repr(vcp_code)


@pytest.mark.parametrize(
    "test_type, readable", [("ro", True), ("wo", False), ("rw", True)]
)
def test_readable(test_type: str, readable: bool):
    code = VPCCommand("image_luminance")
    code.definition["type"] = test_type
    assert code.readable == readable


@pytest.mark.parametrize(
    "test_type, writeable", [("ro", False), ("wo", True), ("rw", True)]
)
def test_writeable(test_type: str, writeable: bool):
    code = VPCCommand("image_luminance")
    code.definition["type"] = test_type
    assert code.writeable == writeable


def test_properties_value():
    """Test that dictionary values propagate to properties."""
    test_name = "unit test"
    test_value = 0x123456789
    test_type = "unit test type"
    test_function = "unit test value"
    test_definition = {
        "name": test_name,
        "value": test_value,
        "type": test_type,
        "function": test_function,
    }
    code = VPCCommand("image_luminance")
    code.definition = test_definition
    assert code.name == test_name
    assert code.value == test_value
    assert code.type == test_type
    assert code.discreet == test_function

from . import vcp
from types import TracebackType
from typing import List, Optional, Type, Union
import enum
import sys


@enum.unique
class ColorPreset(enum.Enum):
    """Monitor color presets."""

    COLOR_TEMP_4000K = 0x03
    COLOR_TEMP_5000K = 0x04
    COLOR_TEMP_6500K = 0x05
    COLOR_TEMP_7500K = 0x06
    COLOR_TEMP_8200K = 0x07
    COLOR_TEMP_9300K = 0x08
    COLOR_TEMP_10000K = 0x09
    COLOR_TEMP_11500K = 0x0A
    COLOR_TEMP_USER1 = 0x0B
    COLOR_TEMP_USER2 = 0x0C
    COLOR_TEMP_USER3 = 0x0D


@enum.unique
class PowerMode(enum.Enum):
    """Monitor power modes."""

    #: On.
    on = 0x01
    #: Standby.
    standby = 0x02
    #: Suspend.
    suspend = 0x03
    #: Software power off.
    off_soft = 0x04
    #: Hardware power off.
    off_hard = 0x05


@enum.unique
class InputSource(enum.Enum):
    """Monitor input sources."""

    OFF = 0x00
    ANALOG1 = 0x01
    ANALOG2 = 0x02
    DVI1 = 0x03
    DVI2 = 0x04
    COMPOSITE1 = 0x05
    COMPOSITE2 = 0x06
    SVIDEO1 = 0x07
    SVIDEO2 = 0x08
    TUNER1 = 0x09
    TUNER2 = 0x0A
    TUNER3 = 0x0B
    CMPONENT1 = 0x0C
    CMPONENT2 = 0x0D
    CMPONENT3 = 0x0E
    DP1 = 0x0F
    DP2 = 0x10
    HDMI1 = 0x11
    HDMI2 = 0x12


class InputSourceValueError(ValueError):
    """
    Raised upon an invalid (out of spec) input source value.

    https://github.com/newAM/monitorcontrol/issues/93

    Attributes:
        value (int): The value of the input source that was invalid.
    """

    def __init__(self, message: str, value: int):
        super().__init__(message)
        self.value = value


class Monitor:

    def __init__(self, cp: vcp.VCP):
        self.vcp = cp

    def get_luminance(self) -> int:
        """
        Gets the monitors back-light luminance.

        Returns:
            Current luminance value.

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        print(monitor.get_luminance())

        Raises:
            VCPError: Failed to get luminance from the VCP.
        """
        code = vcp.VCPCode("image_luminance")
        return self.vcp.get_vcp_feature(code)[0]

    def set_luminance(self, value: int):
        """
        Sets the monitors back-light luminance.

        Args:
            value: New luminance value (typically 0-100).

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        monitor.set_luminance(50)

        Raises:
            ValueError: Luminance outside of valid range.
            VCPError: Failed to set luminance in the VCP.
        """
        code = vcp.VCPCode("image_luminance")
        self.vcp.set_vcp_feature(code, value)

    def get_color_preset(self) -> int:
        """
        Gets the monitors color preset.

        Returns:
            Current color preset.
            Valid values are enumerated in :py:class:`ColorPreset`.

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        print(monitor.get_color_preset())

        Raises:
            VCPError: Failed to get color preset from the VCP.
        """
        code = vcp.VCPCode("image_color_preset")
        return self.vcp.get_vcp_feature(code)[0]

    def set_color_preset(self, value: Union[int, str, ColorPreset]):
        """
        Sets the monitors color preset.

        Args:
            value:
                An integer color preset,
                or a string representing the color preset,
                or a value from :py:class:`ColorPreset`.

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors, ColorPreset

                for monitor in get_monitors():
                    with monitor:
                        monitor.set_color_preset(ColorPreset.COLOR_TEMP_5000K)

        Raises:
            VCPError: Failed to set color preset in the VCP.
            ValueError: Color preset outside valid range.
            AttributeError: Color preset string is invalid.
            TypeError: Unsupported value
        """
        if isinstance(value, str):
            mode_value = getattr(ColorPreset, value).value
        elif isinstance(value, int):
            mode_value = ColorPreset(value).value
        elif isinstance(value, ColorPreset):
            mode_value = value.value
        else:
            raise TypeError("unsupported color preset: " + repr(type(value)))

        code = vcp.VCPCode("image_color_preset")
        self.vcp.set_vcp_feature(code, mode_value)

    def get_contrast(self) -> int:
        """
        Gets the monitors contrast.

        Returns:
            Current contrast value.

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        print(monitor.get_contrast())

        Raises:
            VCPError: Failed to get contrast from the VCP.
        """
        code = vcp.VCPCode("image_contrast")
        return self.vcp.get_vcp_feature(code)[0]

    def set_contrast(self, value: int):
        """
        Sets the monitors back-light contrast.

        Args:
            value: New contrast value (typically 0-100).

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        print(monitor.set_contrast(50))

        Raises:
            ValueError: Contrast outside of valid range.
            VCPError: Failed to set contrast in the VCP.
        """
        code = vcp.VCPCode("image_contrast")
        self.vcp.set_vcp_feature(code, value)

    def get_power_mode(self) -> PowerMode:
        """
        Get the monitor power mode.

        Returns:
            Value from the :py:class:`PowerMode` enumeration.

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        print(monitor.get_power_mode())

        Raises:
            VCPError: Failed to get the power mode.
            ValueError: Set power state outside of valid range.
            KeyError: Set power mode string is invalid.
        """
        code = vcp.VCPCode("display_power_mode")
        return PowerMode(self.vcp.get_vcp_feature(code)[0])

    def set_power_mode(self, value: Union[int, str, PowerMode]):
        """
        Set the monitor power mode.

        Args:
            value:
                An integer power mode,
                or a string representing the power mode,
                or a value from :py:class:`PowerMode`.

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        monitor.set_power_mode("standby")

        Raises:
            VCPError: Failed to get or set the power mode
            ValueError: Power state outside of valid range.
            AttributeError: Power mode string is invalid.
        """
        if isinstance(value, str):
            mode_value = getattr(PowerMode, value).value
        elif isinstance(value, int):
            mode_value = PowerMode(value).value
        elif isinstance(value, PowerMode):
            mode_value = value.value
        else:
            raise TypeError("unsupported mode type: " + repr(type(value)))

        code = vcp.VCPCode("display_power_mode")
        self.vcp.set_vcp_feature(code, mode_value)

    def get_input_source(self) -> InputSource:
        """
        Gets the monitors input source

        Returns:
            Current input source.

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        print(monitor.get_input_source())

            Handling out-of-spec inputs (observed for USB type-C inputs)::

                from monitorcontrol import get_monitors, InputSourceValueError

                for monitor in get_monitors():
                    with monitor:
                        try:
                            print(monitor.get_input_source())
                        except InputSourceValueError as e:
                            print(e.value)

        Raises:
            VCPError: Failed to get input source from the VCP.
            InputSourceValueError:
                Input source value is not within the MCCS defined inputs.
        """
        code = vcp.VCPCode("input_select")
        value = self.vcp.get_vcp_feature(code)[0] & 0xFF
        try:
            return InputSource(value)
        except ValueError:
            raise InputSourceValueError(f"{value} is not a valid InputSource", value)

    def set_input_source(self, value: Union[int, str, InputSource]):
        """
        Sets the monitors input source.

        Args:
            value: New input source

        Example:
            Basic Usage::

                from monitorcontrol import get_monitors

                for monitor in get_monitors():
                    with monitor:
                        print(monitor.set_input_source("DP1"))

        Raises:
            VCPError: Failed to get the input source.
            KeyError: Set input source string is invalid.
        """

        if isinstance(value, str):
            mode_value = getattr(InputSource, value.upper()).value
        elif isinstance(value, int):
            mode_value = value
        elif isinstance(value, InputSource):
            mode_value = value.value
        else:
            raise TypeError("unsupported input type: " + repr(type(value)))

        code = vcp.VCPCode("input_select")
        self.vcp.set_vcp_feature(code, mode_value)


def get_vcps() -> List[vcp.VCP]:
    """
    Discovers virtual control panels.

    This function should not be used directly in most cases, use
    :py:func:`get_monitors` get monitors with VCPs.

    Returns:
        List of VCPs in a closed state.

    Raises:
        NotImplementedError: not implemented for your operating system
        VCPError: failed to list VCPs
    """
    if sys.platform == "win32" or sys.platform.startswith("linux"):
        return vcp.get_vcps()
    else:
        raise NotImplementedError(f"not implemented for {sys.platform}")


def get_monitors() -> List[Monitor]:
    """
    Creates a list of all monitors.

    Returns:
        List of monitors in a closed state.

    Raises:
        VCPError: Failed to list VCPs.

    Example:
        Setting the power mode of all monitors to standby::

            for monitor in get_monitors():
                with monitor:
                    monitor.set_power_mode("standby")

        Setting all monitors to the maximum brightness using the
        context manager::

            for monitor in get_monitors():
                with monitor:
                    monitor.set_luminance(100)
    """
    return [Monitor(v) for v in vcp.get_vcps()]

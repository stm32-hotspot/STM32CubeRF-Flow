from dut.commands import PacketIndicator
from dut.commands import ParameterLength
from dut.commands import OpCode
import ext.string_exts as string


# noinspection PyMethodMayBeStatic
# noinspection PyTypeChecker
# noinspection PyUnusedLocal
class BlueNRG_LP:
    name: str
    baudrate: int
    max_hse_tune_value: int
    opcode: OpCode
    packet_indicator: PacketIndicator
    parameter_length: ParameterLength

    def __init__(self, baudrate: int = 921600, max_hse_tune_value: int = 63):
        self.name = "BlueNRG-LP"
        self.baudrate = baudrate
        self.max_hse_tune_value = max_hse_tune_value
        self.opcode = OpCode()
        self.packet_indicator = PacketIndicator()
        self.parameter_length = ParameterLength(
            set_tx_power_level="0002"
        )

    def get_stack_version_command(self) -> str:
        packet_indicator = self.packet_indicator.aci
        opcode = string.hex_flip_endian(self.opcode.aci_hal_get_firmware_details)
        parameter_total_length = string.hex_flip_endian("0000")

        # ACI_HAL_GET_FIRMWARE_DETAILS
        return packet_indicator + opcode + parameter_total_length

    @staticmethod
    def get_stack_version_response(response: bytes) -> list[bytes]:
        return [response[13:14], response[14:15], response[15:16], response[18:19] + response[17:18]]

    def get_dut_uid_command(self) -> str:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    @staticmethod
    def get_dut_uid_response(response: bytes) -> bytes:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def read_rssi_command(self, connection_handle: str) -> str:
        packet_indicator = self.packet_indicator.hci
        opcode = string.hex_flip_endian(self.opcode.hci_read_rssi)
        parameter_total_length = "02"
        connection_handle = string.hex_flip_endian(connection_handle)

        # HCI_READ_RSSI
        return packet_indicator + opcode + parameter_total_length + connection_handle

    @staticmethod
    def read_rssi_response(response: bytes) -> bytes:
        return response[9:10]

    def start_hse_command(self) -> str:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def stop_hse_command(self) -> str:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def enable_mco_pin_command(self) -> list[str]:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def disable_mco_pin_command(self) -> str:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def get_hse_tune_value_command(self) -> str:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    @staticmethod
    def get_hse_tune_value_response(response: bytes) -> bytes:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def set_hse_tune_value_command(self, tune_value: str) -> list[str]:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def get_otp_index_command(self, address: int, index: int) -> str:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def get_hse_tune_value_otp_command(self, index: int) -> str:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    @staticmethod
    def get_hse_tune_value_otp_response(response: bytes) -> bytes:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

    def set_hse_tune_value_otp_command(self, uid: str, otp_index: int, otp_id: str, tune_value: str) -> list[str]:
        print("BlueNRG-LP Does Not Support this Command.")
        return None

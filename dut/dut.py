from typing import Protocol
from dut.commands import PacketIndicator
from dut.commands import ParameterLength
from dut.commands import OpCode


class DUT(Protocol):
    name: str
    baudrate: int
    max_hse_tune_value: int
    opcode: OpCode
    packet_indicator: PacketIndicator
    parameter_length: ParameterLength
    otp_size: int
    otp_address: int

    def __init__(self, baudrate: int, max_hse_tune_value: int):
        self.name = "DUT"
        self.baudrate = baudrate
        self.max_hse_tune_value = max_hse_tune_value
        self.opcode = OpCode()
        self.packet_indicator = PacketIndicator()
        self.parameter_length = ParameterLength()
        ...

    def get_stack_version_command(self) -> str:
        ...

    @staticmethod
    def get_stack_version_response(response: bytes) -> list[bytes]:
        ...

    def get_dut_uid_command(self) -> str:
        ...

    @staticmethod
    def get_dut_uid_response(response: bytes) -> bytes:
        ...

    def read_rssi_command(self, connection_handle: str) -> str:
        ...

    @staticmethod
    def read_rssi_response(response: bytes) -> bytes:
        ...

    def start_hse_command(self) -> str:
        ...

    def stop_hse_command(self) -> str:
        ...

    def enable_mco_pin_command(self) -> list[str]:
        ...

    def disable_mco_pin_command(self) -> str:
        ...

    def get_hse_tune_value_command(self) -> str:
        ...

    @staticmethod
    def get_hse_tune_value_response(response: bytes) -> bytes:
        ...

    def set_hse_tune_value_command(self, tune_value: str) -> list[str]:
        ...

    def get_otp_index_command(self, address: int, index: int) -> str:
        ...

    def get_hse_tune_value_otp_command(self, index: int) -> str:
        ...

    @staticmethod
    def get_hse_tune_value_otp_response(response: bytes) -> bytes:
        ...

    def set_hse_tune_value_otp_command(self, uid: str, otp_index: int, otp_id: str, tune_value: str) -> list[str]:
        ...

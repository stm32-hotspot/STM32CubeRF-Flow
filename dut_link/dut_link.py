from typing import Protocol
from dut.dut import DUT


class DUTLink(Protocol):
    dut = None
    serialport = None
    error_code = None

    def __init__(self, dut: DUT):
        self.dut = dut
        ...

    def connect(self):
        ...

    def disconnect(self):
        ...

    def send_command(self, command: str):
        ...

    def read_response(self) -> bytes | None:
        ...

    def __read_response_status(self, response: bytes | None) -> bytes:
        ...

    def is_connected(self) -> bytes:
        ...

    def start_tone(self, rf_channel: str = "00", offset: str = "00") -> bytes:
        ...

    def stop_tone(self) -> bytes:
        ...

    def start_transmitter(
            self, tx_channel: str = "00", length_of_test_data: str = "25", packet_payload: str = "00", phy: str = "01"
    ) -> bytes:
        ...

    def stop_transmitter(self) -> bytes:
        ...

    def start_receiver(self, rx_channel: str = "00", phy: str = "01", modulation_index: str = "00") -> bytes:
        ...

    def stop_receiver(self) -> bytes:
        ...

    def hci_reset(self) -> bytes:
        ...

    def set_tx_power_level(self, en_high_power: str = "01", pa_level: str = "07") -> bytes:
        ...

    def read_rssi(self, connection_handle: str = "0000") -> bytes:
        ...

    def get_stack_version(self) -> list[bytes]:
        ...

    def get_dut_uid(self) -> bytes:
        ...

    def start_hse(self) -> bytes:
        ...

    def stop_hse(self) -> bytes:
        ...

    def enable_mco_pin(self) -> bytes:
        ...

    def disable_mco_pin(self) -> bytes:
        ...

    def get_hse_tune_value(self) -> bytes:
        ...

    def set_hse_tune_value(self, value: int = 0) -> bytes:
        ...

    def get_otp_index(self, free_index: bool = False) -> int:
        ...

    def get_hse_tune_value_otp(self) -> bytes:
        ...

    def set_hse_tune_value_otp(self, otp_id: str, value: int = 0) -> bytes:
        ...

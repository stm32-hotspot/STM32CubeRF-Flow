from typing import Protocol


class BluetoothTester(Protocol):

    def connect(self, ip_address: str, port: int):
        ...

    def disconnect(self):
        ...

    def send_command(self):
        ...

    def read_response(self) -> str:
        ...

    def initialize(self) -> str:
        ...

    def configure_bt(self, band: str, channel: str):
        ...

    def configure_vsg(self, sampling_rate: str, frequency: str, wavefile: str, power_level: int):
        ...

    def configure_vsa(
            self, frequency: str, sampling_rate: str, capture_time: str, trigger_source: str, reference_level: str
    ):
        ...

    def initialize_vsg(self, channel: str):
        ...

    def initialize_vsa(self, channel: str):
        ...

    def configure_wlist(self, count: str, next_count: str, length: str, start_point: str):
        ...

    def calculate_power(self, packets: str) -> str:
        ...

    def calculate_power_average(self, packets: str) -> str:
        ...

    def calculate_power_peak(self, packets: str) -> str:
        ...

    def calculate_spectrum(self, packets: str, bandwidth: int) -> str:
        ...

    def calculate_spectrum_average(self, packets: str, bandwidth: int) -> str:
        ...

    def calculate_tx_quality(self, packets: str) -> str:
        ...



from dataclasses import dataclass


@dataclass(frozen=True)
class PacketIndicator:
    hci: str = "01"
    hci_m4: str = "20"
    aci: str = "81"
    start_tone: str = aci
    stop_tone: str = aci
    set_tx_power_level: str = aci


@dataclass(frozen=True)
class OpCode:
    hci_reset: str = "0C03"
    hci_read_rssi: str = "1405"
    hci_read_local_version_information: str = "1001"
    hci_le_enhanced_transmitter_test: str = "2034"
    hci_le_enhanced_receiver_test: str = "2033"
    hci_le_test_end: str = "201F"
    aci_hal_get_firmware_details: str = "FC01"
    aci_hal_tone_start: str = "FC15"
    aci_hal_tone_stop: str = "FC16"
    aci_hal_set_tx_power_level: str = "FC0F"
    aci_hal_read_rssi: str = "FC22"
    vs_hci_c1_write_register: str = "FD60"
    vs_hci_c1_read_register: str = "FD61"
    vs_hci_c1_device_information: str = "FD62"


@dataclass(frozen=True)
class ParameterLength:
    set_tx_power_level: str = "02"

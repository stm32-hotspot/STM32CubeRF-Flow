import serial
from dut.dut import DUT
import ext.string_exts as string


class USBLink:
    dut = None
    serialport = None
    error_code = b"\x91"

    def __init__(self, dut: DUT):
        self.dut = dut
        self.serialport = serial.Serial()

    def connect(
            self, port: str, baudrate: int, bytesize: int = 8, parity: str = 'N',
            stopbits: int = 1, xonxoff: bool = False, rtscts: bool = False, dsrdtr: bool = False,
            read_timeout: float = 0.1, write_timeout: float = 0
    ):
        with self.serialport as ser:
            ser.port = port
            ser.baudrate = baudrate
            ser.bytesize = bytesize
            ser.parity = parity
            ser.stopbits = stopbits
            ser.xonxoff = xonxoff
            ser.rtscts = rtscts
            ser.dsrdtr = dsrdtr
            ser.timeout = read_timeout
            ser.write_timeout = write_timeout

        try:
            self.serialport.open()
        except serial.SerialException:
            print("DUT Failed to Connect! Check if Port is Already Open.")

    def disconnect(self):
        self.serialport.close()

    def send_command(self, command: str):
        if command is not None and len(command) > 0:
            self.serialport.write(bytearray.fromhex(command))

    def read_response(self) -> bytes | None:
        return self.serialport.read(1000)

    def __read_response_status(self, response: bytes | None) -> bytes:
        if response is None or len(response) == 0:
            return self.error_code

        # Return Status Code
        return response[6:7]

    def is_connected(self) -> bytes:
        if not self.serialport.is_open:
            return self.error_code

        packet_indicator = self.dut.packet_indicator.hci
        opcode = string.hex_flip_endian(self.dut.opcode.hci_read_local_version_information)
        parameter_total_length = "00"

        # HCI_READ_LOCAL_VERSION_INFORMATION
        self.send_command(packet_indicator + opcode + parameter_total_length)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def start_tone(self, rf_channel: str = "00", offset: str = "00") -> bytes:
        packet_indicator = self.dut.packet_indicator.start_tone
        opcode = string.hex_flip_endian(self.dut.opcode.aci_hal_tone_start)
        parameter_total_length = string.hex_flip_endian("0002")

        # ACI_HAL_TONE_START
        self.send_command(packet_indicator + opcode + parameter_total_length + rf_channel + offset)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def stop_tone(self) -> bytes:
        packet_indicator = self.dut.packet_indicator.stop_tone
        opcode = string.hex_flip_endian(self.dut.opcode.aci_hal_tone_stop)
        parameter_total_length = string.hex_flip_endian("0000")

        # ACI_HAL_TONE_STOP
        self.send_command(packet_indicator + opcode + parameter_total_length)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def start_transmitter(
            self, tx_channel: str = "00", length_of_test_data: str = "25", packet_payload: str = "00", phy: str = "01"
    ) -> bytes:
        packet_indicator = self.dut.packet_indicator.hci
        opcode = string.hex_flip_endian(self.dut.opcode.hci_le_enhanced_transmitter_test)
        parameter_total_length = "04"

        # HCI_LE_ENHANCED_TRANSMITTER_TEST | HCI_LE_TRANSMITTER_TEST_V2
        self.send_command(
            packet_indicator + opcode + parameter_total_length + tx_channel + length_of_test_data + packet_payload + phy
        )

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def stop_transmitter(self) -> bytes:
        packet_indicator = self.dut.packet_indicator.hci
        opcode = string.hex_flip_endian(self.dut.opcode.hci_le_test_end)
        parameter_total_length = "00"

        # HCI_LE_TEST_END
        self.send_command(packet_indicator + opcode + parameter_total_length)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def start_receiver(self, rx_channel: str = "00", phy: str = "01", modulation_index: str = "00") -> bytes:
        packet_indicator = self.dut.packet_indicator.hci
        opcode = string.hex_flip_endian(self.dut.opcode.hci_le_enhanced_receiver_test)
        parameter_total_length = "03"

        # HCI_LE_ENHANCED_RECEIVER_TEST | HCI_LE_RECEIVER_TEST_V2
        self.send_command(packet_indicator + opcode + parameter_total_length + rx_channel + phy + modulation_index)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def stop_receiver(self) -> bytes:
        packet_indicator = self.dut.packet_indicator.hci
        opcode = string.hex_flip_endian(self.dut.opcode.hci_le_test_end)
        parameter_total_length = "00"

        # HCI_LE_TEST_END
        self.send_command(packet_indicator + opcode + parameter_total_length)

        response = self.read_response()

        if response is None or len(response) == 0:
            return self.error_code + self.error_code

        # Return Number of Packets
        return response[8:9] + response[7:8]

    def hci_reset(self) -> bytes:
        packet_indicator = self.dut.packet_indicator.hci
        opcode = string.hex_flip_endian(self.dut.opcode.hci_reset)
        parameter_total_length = "00"

        # HCI_RESET
        self.send_command(packet_indicator + opcode + parameter_total_length)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def set_tx_power_level(self, en_high_power: str = "00", pa_level: str = "00") -> bytes:
        packet_indicator = self.dut.packet_indicator.set_tx_power_level
        opcode = string.hex_flip_endian(self.dut.opcode.aci_hal_set_tx_power_level)
        parameter_total_length = string.hex_flip_endian(self.dut.parameter_length.set_tx_power_level)

        # ACI_HAL_SET_TX_POWER_LEVEL
        self.send_command(packet_indicator + opcode + parameter_total_length + en_high_power + pa_level)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def read_rssi(self, connection_handle: str = "0000") -> bytes:
        # HCI_READ_RSSI
        self.send_command(self.dut.read_rssi_command(connection_handle))

        # Return RSSI Value
        return self.dut.read_rssi_response(self.read_response())

    def get_stack_version(self) -> list[bytes]:
        self.send_command(self.dut.get_stack_version_command())

        response = self.read_response()

        if response is None or len(response) == 0 or (len(response) > 5 and response[6] != 0):
            return [self.error_code, self.error_code, self.error_code, self.error_code + self.error_code]

        # Return BLE Stack Version Major, Version Minor, Version Patch, and Variant
        return self.dut.get_stack_version_response(response)

    def get_dut_uid(self) -> bytes:
        self.send_command(self.dut.get_dut_uid_command())

        response = self.read_response()

        if response is None or len(response) == 0 or (len(response) > 5 and response[6] != 0):
            return self.error_code + self.error_code + self.error_code + self.error_code

        # Return Unique Device ID (UID64)
        return self.dut.get_dut_uid_response(response)

    def start_hse(self) -> bytes:
        self.send_command(self.dut.start_hse_command())

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def stop_hse(self) -> bytes:
        self.send_command(self.dut.stop_hse_command())

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def enable_mco_pin(self) -> bytes:
        for command in self.dut.enable_mco_pin_command():
            self.send_command(command)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def disable_mco_pin(self) -> bytes:
        self.send_command(self.dut.disable_mco_pin_command())

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def get_hse_tune_value(self) -> bytes:
        self.send_command(self.dut.get_hse_tune_value_command())

        response = self.read_response()

        if response is None or len(response) == 0:
            return self.error_code

        # Return HSE Tune Value
        return self.dut.get_hse_tune_value_response(response)

    def set_hse_tune_value(self, value: int = 0) -> bytes:
        if value < 0 or value > 63:
            return self.error_code

        value_hex = hex(value)[2:].zfill(2)

        for command in self.dut.set_hse_tune_value_command(value_hex):
            self.send_command(command)

        # Return Status Code
        return self.__read_response_status(self.read_response())

    def get_otp_index(self, free_index: bool = False) -> int:
        otp_area_size = 1024
        store_address = 0x1FFF7000
        index = 0

        while index < otp_area_size:
            self.send_command(self.dut.get_otp_index_command(store_address, index))
            if self.read_response()[7:11].hex().upper() == "FFFFFFFF":
                break
            index += 8

        if not free_index:
            index -= 8

        if index >= otp_area_size:
            return -1

        return index

    def get_hse_tune_value_otp(self) -> bytes:
        otp_index = self.get_otp_index() + 4

        self.send_command(self.dut.get_hse_tune_value_otp_command(otp_index))

        # Return HSE Tune Value
        return self.dut.get_hse_tune_value_otp_response(self.read_response())

    def set_hse_tune_value_otp(self, otp_id: str, value: int = 0) -> bytes:
        if value < 0 or value > 63:
            return self.error_code

        uid = self.get_dut_uid().hex()[4:]
        otp_index = self.get_otp_index(True)
        value_hex = hex(value)[2:].zfill(2)

        if uid[0:2] == self.error_code.hex():
            uid = "0000"
        if otp_index == -1:
            return self.error_code

        for command in self.dut.set_hse_tune_value_otp_command(uid, otp_index, otp_id, value_hex):
            self.send_command(command)

        # Return Status Code
        return self.__read_response_status(self.read_response())

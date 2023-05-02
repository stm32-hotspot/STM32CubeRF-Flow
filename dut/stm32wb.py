from dut.commands import PacketIndicator
from dut.commands import ParameterLength
from dut.commands import OpCode
import ext.string_exts as string


class STM32WB:
    name: str
    baudrate: int
    max_hse_tune_value: int
    opcode: OpCode
    packet_indicator: PacketIndicator
    parameter_length: ParameterLength

    def __init__(self, baudrate: int = 115200, max_hse_tune_value: int = 63):
        self.name = "STM32WB"
        self.baudrate = baudrate
        self.max_hse_tune_value = max_hse_tune_value
        self.opcode = OpCode()
        self.packet_indicator = PacketIndicator(
            start_tone=PacketIndicator.hci,
            stop_tone=PacketIndicator.hci,
            set_tx_power_level=PacketIndicator.hci
        )
        self.parameter_length = ParameterLength()

    def __send_command_write_register(self, bus_size_access: str, mask: str, address: str, value: str) -> str:
        packet_indicator = self.packet_indicator.hci_m4
        opcode = string.hex_flip_endian(self.opcode.vs_hci_c1_write_register)
        parameter_total_length = "0D"
        mask = string.hex_flip_endian(mask)
        address = string.hex_flip_endian(address)
        value = string.hex_flip_endian(value)

        # VS_HCI_C1_WRITE_REGISTER
        return packet_indicator + opcode + parameter_total_length + bus_size_access + mask + address + value

    def __send_command_read_register(self, bus_size_access: str, address: str) -> str:
        packet_indicator = self.packet_indicator.hci_m4
        opcode = string.hex_flip_endian(self.opcode.vs_hci_c1_read_register)
        parameter_total_length = "05"
        address = string.hex_flip_endian(address)

        # VS_HCI_C1_READ_REGISTER
        return packet_indicator + opcode + parameter_total_length + bus_size_access + address

    def get_stack_version_command(self) -> str:
        packet_indicator = self.packet_indicator.hci_m4
        opcode = string.hex_flip_endian(self.opcode.vs_hci_c1_device_information)
        parameter_total_length = "00"

        # VS_HCI_C1_DEVICE_INFORMATION
        return packet_indicator + opcode + parameter_total_length

    @staticmethod
    def get_stack_version_response(response: bytes) -> list[bytes]:
        return [response[52:53], response[51:52], response[50:51], response[49:50]]

    def get_dut_uid_command(self) -> str:
        packet_indicator = self.packet_indicator.hci_m4
        opcode = string.hex_flip_endian(self.opcode.vs_hci_c1_device_information)
        parameter_total_length = "00"

        # VS_HCI_C1_DEVICE_INFORMATION
        return packet_indicator + opcode + parameter_total_length

    @staticmethod
    def get_dut_uid_response(response: bytes) -> bytes:
        return response[20:21] + response[19:20] + response[18:19] + response[17:18]

    def read_rssi_command(self, connection_handle: str) -> str:
        packet_indicator = self.packet_indicator.hci
        opcode = string.hex_flip_endian(self.opcode.aci_hal_read_rssi)
        parameter_total_length = "00"

        # ACI_HAL_READ_RSSI
        return packet_indicator + opcode + parameter_total_length

    @staticmethod
    def read_rssi_response(response: bytes) -> bytes:
        return response[7:8]

    def start_hse_command(self) -> str:
        return self.__send_command_write_register("04", "00010000", "58000000", "00010000")

    def stop_hse_command(self) -> str:
        return self.__send_command_write_register("04", "00010000", "58000000", "00000000")

    def enable_mco_pin_command(self) -> list[str]:
        commands = list()

        # Select HSE on MCO (RCC_CFGR.MCOSEL)
        commands.append(self.__send_command_write_register("04", "0F000000", "58000008", "04000000"))

        # Enable GPIO-A IP Bus Clock (RCC_AHB2ENR.GPIOAEN)
        commands.append(self.__send_command_write_register("04", "00000001", "5800004C", "00000001"))

        # Output MCO on PA8 (GPIO_AFRH.AFSEL8)
        commands.append(self.__send_command_write_register("04", "0000000F", "48000024", "00000000"))

        # PA8 Mode Alternate Function
        commands.append(self.__send_command_write_register("04", "00030000", "48000000", "00020000"))

        # PA8 Output Type
        commands.append(self.__send_command_write_register("04", "00000100", "48000004", "00000000"))

        # PA8 Output Speed
        commands.append(self.__send_command_write_register("04", "00030000", "48000008", "00030000"))

        # PA8 Output Pull-Up/Down
        commands.append(self.__send_command_write_register("04", "00030000", "4800000C", "00010000"))

        return commands

    def disable_mco_pin_command(self) -> str:
        # Disable MCO Output (RCC_CFGR.MCOSEL)
        return self.__send_command_write_register("04", "0F000000", "58000008", "00000000")

    def get_hse_tune_value_command(self) -> str:
        return self.__send_command_read_register("04", "5800009C")

    @staticmethod
    def get_hse_tune_value_response(response: bytes) -> bytes:
        return response[8:9]

    def set_hse_tune_value_command(self, tune_value: str) -> list[str]:
        commands = list()

        # Unlock RCC_HSECR Register
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "5800009C", "CAFECAFE"))

        # Set HSE Tune Value
        commands.append(self.__send_command_write_register("04", "0000FF00", "5800009C", "0000" + tune_value + "00"))

        return commands

    def get_otp_index_command(self, address: int, index: int) -> str:
        return self.__send_command_read_register("04", hex(address + index)[2:])

    def get_hse_tune_value_otp_command(self, index: int) -> str:
        base_address = 0x1FFF7000
        # Read Upper BD Address (OTP ID + HSE Tune Value)
        return self.__send_command_read_register("04", hex(base_address + index)[2:])

    @staticmethod
    def get_hse_tune_value_otp_response(response: bytes) -> bytes:
        return response[9:10]

    def set_hse_tune_value_otp_command(self, uid: str, otp_index: int, otp_id: str, tune_value: str) -> list[str]:
        commands = list()

        otp_address = 0x1FFF7000 + otp_index
        lower_otp_address = hex(otp_address)[2:]
        upper_otp_address = hex(otp_address + 4)[2:]

        # Write 0x45670123 in FLASH_KEYR to Enable Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "58004008", "45670123"))

        # Write 0xCDEF89AB in FLASH_KEYR to Enable Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "58004008", "CDEF89AB"))

        # Write 0x08192A3B in FLASH_OPTKEYR to Enable Option Byte Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "5800400C", "08192A3B"))

        # Write 0x4C5D6E7F in FLASH_OPTKEYR to Enable Option Byte Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "5800400C", "4C5D6E7F"))

        # Set PG in FLASH_CR to Enable Flash Programming
        commands.append(self.__send_command_write_register("04", "00000001", "58004014", "00000001"))

        # Write Lower BD Address (Company ID + UID)
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", lower_otp_address, "E105" + uid))

        # Write Upper BD Address (OTP ID + HSE Tune Value + Upper BD)
        commands.append(
            self.__send_command_write_register("04", "FFFFFFFF", upper_otp_address, otp_id + tune_value + "0080")
        )

        return commands

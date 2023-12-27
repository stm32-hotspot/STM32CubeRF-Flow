from dut.stm32wb import STM32WB
from dut.commands import PacketIndicator
from dut.commands import ParameterLength
from dut.commands import OpCode
import ext.string_exts as string


class STM32WBA:
    name: str
    baudrate: int
    max_hse_tune_value: int
    opcode: OpCode
    packet_indicator: PacketIndicator
    parameter_length: ParameterLength
    otp_size: int = 512
    otp_address: int = 0x0BF90000
    stm32wb: STM32WB

    def __init__(self, baudrate: int = 115200, max_hse_tune_value: int = 63):
        self.name = "STM32WBA"
        self.baudrate = baudrate
        self.max_hse_tune_value = max_hse_tune_value
        self.opcode = OpCode()
        self.packet_indicator = PacketIndicator(
            start_tone=PacketIndicator.hci,
            stop_tone=PacketIndicator.hci,
            set_tx_power_level=PacketIndicator.hci
        )
        self.parameter_length = ParameterLength()
        self.stm32wb = STM32WB()

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
        return self.stm32wb.get_stack_version_command()

    @staticmethod
    def get_stack_version_response(response: bytes) -> list[bytes]:
        return [response[52:53], response[51:52], response[50:51], response[49:50]]

    def get_dut_uid_command(self) -> str:
        return self.stm32wb.get_dut_uid_command()

    @staticmethod
    def get_dut_uid_response(response: bytes) -> bytes:
        return response[20:21] + response[19:20] + response[18:19] + response[17:18]

    def read_rssi_command(self, connection_handle: str) -> str:
        return self.stm32wb.read_rssi_command(connection_handle)

    @staticmethod
    def read_rssi_response(response: bytes) -> bytes:
        return response[7:8]

    def start_hse_command(self) -> str:
        return self.__send_command_write_register("04", "00010000", "46020C00", "00010000")

    def stop_hse_command(self) -> str:
        return self.__send_command_write_register("04", "00010000", "46020C00", "00000000")

    def enable_mco_pin_command(self) -> list[str]:
        print("Warning: A modification of the BLE_TransparentMode project is required for the use of this function. "
              "The MCO pin PA8 is being used for UART communication, it is recommended to modify the "
              "BLE_TransparentMode project to use USART2 instead of USART1.")

        commands = list()
        rcc_base = "46020C"
        gpioa_base = "420200"

        # Select HSE on MCO (RCC_CFGR1.MCOSEL)
        commands.append(self.__send_command_write_register("04", "0F000000", rcc_base + "1C", "04000000"))

        # Enable GPIO-A IP Bus Clock (RCC_AHB2ENR.GPIOAEN)
        commands.append(self.__send_command_write_register("04", "00000001", rcc_base + "8C", "00000001"))

        # Output MCO on PA8 (GPIOA_AFRH.AFSEL8)
        commands.append(self.__send_command_write_register("04", "0000000F", gpioa_base + "24", "00000000"))

        # PA8 Mode Alternate Function (GPIOA_MODER)
        commands.append(self.__send_command_write_register("04", "00030000", gpioa_base + "00", "00020000"))

        # PA8 Output Type (GPIOA_OTYPER)
        commands.append(self.__send_command_write_register("04", "00000100", gpioa_base + "04", "00000000"))

        # PA8 Output Speed (GPIOA_OSPEEDR)
        commands.append(self.__send_command_write_register("04", "00030000", gpioa_base + "08", "00020000"))

        # PA8 Output Pull-Up/Down (GPIOA_PUPDR)
        commands.append(self.__send_command_write_register("04", "00030000", gpioa_base + "0C", "00000000"))

        return commands

    def disable_mco_pin_command(self) -> str:
        # Disable MCO Output (RCC_CFGR1.MCOSEL)
        return self.__send_command_write_register("04", "0F000000", "46020C1C", "00000000")

    def get_hse_tune_value_command(self) -> str:
        return self.__send_command_read_register("04", "46020e10")

    @staticmethod
    def get_hse_tune_value_response(response: bytes) -> bytes:
        return response[9:10]

    def set_hse_tune_value_command(self, tune_value: str) -> list[str]:
        commands = list()

        # Set HSE Tune Value
        commands.append(self.__send_command_write_register("04", "003F0000", "46020e10", "00" + tune_value + "0000"))

        return commands

    def get_otp_index_command(self, address: int, index: int) -> str:
        return self.__send_command_read_register("04", "{:08x}".format(address + index))

    def get_hse_tune_value_otp_command(self, index: int) -> str:
        # Read Upper BD Address (OTP ID + HSE Tune Value)
        return self.__send_command_read_register("04", "{:08x}".format(self.otp_address + index))

    @staticmethod
    def get_hse_tune_value_otp_response(response: bytes) -> bytes:
        return response[9:10]

    def set_hse_tune_value_otp_command(self, uid: str, otp_index: int, otp_id: str, tune_value: str) -> list[str]:
        commands = list()

        otp_address = self.otp_address + otp_index
        otp_address_1 = "{:08x}".format(otp_address)
        otp_address_2 = "{:08x}".format(otp_address + 4)
        otp_address_3 = "{:08x}".format(otp_address + 8)
        otp_address_4 = "{:08x}".format(otp_address + 12)

        # Write 0x45670123 in FLASH_NSKEYR to Enable Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "40022008", "45670123"))

        # Write 0xCDEF89AB in FLASH_NSKEYR to Enable Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "40022008", "CDEF89AB"))

        # Write 0x08192A3B in FLASH_OPTKEYR to Enable Option Byte Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "40022010", "08192A3B"))

        # Write 0x4C5D6E7F in FLASH_OPTKEYR to Enable Option Byte Programming/Erasing
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", "40022010", "4C5D6E7F"))

        # Set PG in FLASH_NSCR1 to Enable Flash Programming
        commands.append(self.__send_command_write_register("04", "00000001", "40022028", "00000001"))

        # Write Arbitrary Data (STM3 = 0x334D5453 for Example)
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", otp_address_1, "334D5453"))

        # Write Arbitrary Data (2WBA = 0x41425732 for Example)
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", otp_address_2, "41425732"))

        # Write Lower BD Address (Company ID + UID)
        commands.append(self.__send_command_write_register("04", "FFFFFFFF", otp_address_3, "E12A" + uid))

        # Write Upper BD Address (OTP ID + HSE Tune Value + Upper BD)
        commands.append(
            self.__send_command_write_register("04", "FFFFFFFF", otp_address_4, otp_id + tune_value + "0080")
        )

        # Clear PG in FLASH_NSCR1 to Disable Flash Programming
        commands.append(self.__send_command_write_register("04", "00000001", "40022028", "00000000"))

        return commands

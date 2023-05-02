from rf_flow import RFFlow
from tester.litepoint import LitePoint
from dut_link.usb_link import USBLink
from dut.stm32wb import STM32WB


if __name__ == '__main__':
    print("STM32CubeRF-Flow: Automated RF Testing\n")

    # Initialize Tester & DUT-Link
    tester = LitePoint()
    dut_link = USBLink(STM32WB())

    # Open Connections
    tester.connect("192.168.100.254", 24000)
    dut_link.connect('COM5', dut_link.dut.baudrate)

    # Initialize RF Test Flow
    rf_flow = RFFlow(tester, dut_link)

    # Perform BLE RF Tests
    rf_flow.ble_tx_power_test("01", "25", "2402e6", "80e6", "0.02", "IMM", "7", "CHAN1", "0,5", 1.8)
    rf_flow.ble_tx_spectrum_test("01", "25", "2402e6", "80e6", "0.02", "IMM", "7", "CHAN1", "0,5", 20)
    rf_flow.ble_tx_quality_test("01", "25", "2402e6", "80e6", "0.02", "IMM", "7", "CHAN1", "0,5")
    rf_flow.ble_hse_ppm_test("01", "25", "2402e6", "80e6", "0.02", "IMM", "7", "CHAN1", "0,5", 0, 64, 1, 0.1)
    rf_flow.ble_rx_per_test(
        "1", "283", "9.375e6", "2402e6", "BT/bt_le_prbs9_Fs80M.iqvsg", -70, "CHAN1", 1500, "0", "0", "0", 2
    )

    # Close Connections
    tester.disconnect()
    dut_link.disconnect()

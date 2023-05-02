from tester.bluetooth_tester import BluetoothTester
from dut_link.dut_link import DUTLink
import os.path
import time
import csv


class RFFlow:
    tester = None
    dut_link = None
    base_folder = "test_results"
    test_folder = "test_results"

    def __init__(self, tester: BluetoothTester, dut_link: DUTLink):
        self.tester = tester
        self.dut_link = dut_link
        self.folder_create()

    def folder_create(self):
        dut_uid = self.dut_link.get_dut_uid().hex()

        if dut_uid[0:2] == self.dut_link.error_code.hex():
            dut_uid = "unknown"

        self.test_folder = self.test_folder + "_" + dut_uid
        if not os.path.exists(self.base_folder + "/" + self.test_folder):
            os.makedirs(self.base_folder + "/" + self.test_folder)

    def csv_create(self, file_name: str):
        file = open(self.base_folder + "/" + self.test_folder + "/" + file_name + ".csv", 'w', newline='')
        file.close()

    def csv_write(self, file_name: str, row: list[str]):
        file = open(self.base_folder + "/" + self.test_folder + "/" + file_name + ".csv", 'a', newline='')
        writer = csv.writer(file)
        writer.writerow(row)
        file.close()

    @staticmethod
    def data_split(data: str) -> list[str]:
        return data.strip("\n").split(",") if len(data) > 0 else list()

    # Bluetooth TX Power Test
    def ble_tx_power_test(
            self, en_high_power: str,  pa_level: str, frequency: str, sampling_rate: str, capture_time: str,
            trigger_source: str, reference_level: str, channel: str, packets: str, antenna_gain: float
    ):
        csv_file = "ble_tx_power_test"

        # Create CSV File
        self.csv_create(csv_file)
        self.csv_write(csv_file, ["BLE TX Power Test"])
        print("BLE TX Power Test\n")

        # Setup DUT as Transmitter
        self.dut_link.hci_reset()
        self.dut_link.set_tx_power_level(en_high_power, pa_level)
        self.dut_link.start_transmitter()

        # Setup Tester as VSA
        self.tester.initialize()
        self.tester.configure_vsa(frequency, sampling_rate, capture_time, trigger_source, reference_level)
        self.tester.initialize_vsa(channel)

        # Calculate Results
        average = self.data_split(self.tester.calculate_power_average(packets))
        peak = self.data_split(self.tester.calculate_power_peak(packets))
        power = self.data_split(self.tester.calculate_power(packets))

        # Stop DUT Transmitter
        self.dut_link.stop_transmitter()

        # Check Pass Verdict (BLE SIG RFPHY Test Suite TRM 4.5.1)
        pass_verdict_1 = float(peak[1]) <= (float(average[1]) + 3)
        pass_verdict_2 = (float(average[1]) + antenna_gain) <= 20
        pass_verdict_3 = -20 <= float(average[1]) <= 10
        pass_verdict = "PASS" if pass_verdict_1 and pass_verdict_2 and pass_verdict_3 else "FAIL"

        # Write Results to CSV
        self.csv_write(csv_file, ["Average"] + average)
        self.csv_write(csv_file, ["Peak"] + peak)
        self.csv_write(csv_file, ["Power"] + power)
        self.csv_write(csv_file, ["Test Verdict", pass_verdict])

    # Bluetooth TX Spectrum Test
    def ble_tx_spectrum_test(
            self, en_high_power: str,  pa_level: str, frequency: str, sampling_rate: str, capture_time: str,
            trigger_source: str, reference_level: str, channel: str, packets: str,  bandwidth: int
    ):
        csv_file = "ble_tx_spectrum_test"

        # Create CSV File
        self.csv_create(csv_file)
        self.csv_write(csv_file, ["BLE TX Spectrum Test"])
        print("BLE TX Spectrum Test\n")

        # Setup DUT as Transmitter
        self.dut_link.hci_reset()
        self.dut_link.set_tx_power_level(en_high_power, pa_level)
        self.dut_link.start_transmitter()

        # Setup Tester as VSA
        self.tester.initialize()
        self.tester.configure_vsa(frequency, sampling_rate, capture_time, trigger_source, reference_level)
        self.tester.initialize_vsa(channel)

        # Calculate Results
        spectrum = self.data_split(self.tester.calculate_spectrum(packets, bandwidth))
        average = self.data_split(self.tester.calculate_spectrum_average(packets, bandwidth))

        # Stop DUT Transmitter
        self.dut_link.stop_transmitter()

        # Write Results to CSV
        self.csv_write(csv_file, ["Bandwidth"] + spectrum)
        self.csv_write(csv_file, ["Average"] + average)

    # Bluetooth TX Quality Test
    def ble_tx_quality_test(
            self, en_high_power: str,  pa_level: str, frequency: str, sampling_rate: str, capture_time: str,
            trigger_source: str, reference_level: str, channel: str, packets: str
    ):
        csv_file = "ble_tx_quality_test"

        # Create CSV File
        self.csv_create(csv_file)
        self.csv_write(csv_file, ["BLE TX Quality Test"])
        print("BLE TX Quality Test\n")

        # Setup DUT as Transmitter
        self.dut_link.hci_reset()
        self.dut_link.set_tx_power_level(en_high_power, pa_level)
        self.dut_link.start_transmitter()

        # Setup Tester as VSA
        self.tester.initialize()
        self.tester.configure_vsa(frequency, sampling_rate, capture_time, trigger_source, reference_level)
        self.tester.initialize_vsa(channel)

        # Calculate Results
        tx_quality = self.data_split(self.tester.calculate_tx_quality(packets))

        # Stop DUT Transmitter
        self.dut_link.stop_transmitter()

        # Write Results to CSV
        self.csv_write(csv_file, ["TX Quality"] + tx_quality)

    # Bluetooth HSE PPM Test
    def ble_hse_ppm_test(
            self, en_high_power: str,  pa_level: str, frequency: str, sampling_rate: str, capture_time: str,
            trigger_source: str, reference_level: str, channel: str, packets: str, hse_start: int, hse_stop: int,
            hse_step: int, time_delay: float
    ):
        csv_file = "ble_hse_ppm_test"

        # Create CSV File
        self.csv_create(csv_file)
        self.csv_write(csv_file, ["BLE HSE PPM Test"])
        print("BLE HSE PPM Test\n")

        # Setup DUT
        self.dut_link.hci_reset()
        self.dut_link.set_tx_power_level(en_high_power, pa_level)

        # Setup Tester
        self.tester.initialize()
        self.tester.configure_vsa(frequency, sampling_rate, capture_time, trigger_source, reference_level)

        # Initialize Lists of Tested Values
        tested_hse = list()
        tested_ifo = list()
        tested_ppm = list()

        # Initialize Optimal Values
        optimal_hse = 0
        optimal_ppm = 100

        # Test TX Quality at Each Selected HSE Value (HSE Step 1: 0 - 63)
        for i in range(hse_start, hse_stop, hse_step):
            # Set HSE Tune Value & Start Transmitter
            self.dut_link.stop_hse()
            self.dut_link.set_hse_tune_value(i)
            self.dut_link.start_hse()
            self.dut_link.start_transmitter()

            # Start Tester VSA
            self.tester.initialize_vsa(channel)

            time.sleep(time_delay)

            # Calculate Results
            tx_quality = self.data_split(self.tester.calculate_tx_quality(packets))
            initial_frequency_offset = float(tx_quality[1]) / 1000
            parts_per_million = (initial_frequency_offset / float(frequency[0:4])) * 1000

            # Stop DUT Transmitter
            self.dut_link.stop_transmitter()

            # Check for Optimal Value
            if abs(parts_per_million) < optimal_ppm:
                optimal_hse = i
                optimal_ppm = parts_per_million

            # Output Progress
            print("HSE: " + str(i))
            print("IFO: " + str(initial_frequency_offset))
            print("PPM: " + str(parts_per_million) + "\n")

            # Add Results to Lists of Tested Values
            tested_hse.append(str(i))
            tested_ifo.append(str(initial_frequency_offset))
            tested_ppm.append(str(parts_per_million))

        # Write Results to CSV
        self.csv_write(csv_file, ["Optimal HSE", str(optimal_hse)])
        self.csv_write(csv_file, ["Optimal PPM", str(optimal_ppm)])
        self.csv_write(csv_file, ["Tested HSE"] + tested_hse)
        self.csv_write(csv_file, ["Tested IFO"] + tested_ifo)
        self.csv_write(csv_file, ["Tested PPM"] + tested_ppm)

    # Bluetooth RX PER Test
    def ble_rx_per_test(
            self, bt_band: str, bt_channel: str, sampling_rate: str, frequency: str, wavefile: str, power_level: int,
            channel: str, packet_count: int, next_count: str, length: str, start_point: str, time_delay: float
    ):
        csv_file = "ble_rx_per_test"

        # Create CSV File
        self.csv_create(csv_file)
        self.csv_write(csv_file, ["BLE RX PER Test"])
        print("BLE RX PER Test\n")

        # Setup DUT as Receiver
        self.dut_link.hci_reset()
        self.dut_link.start_receiver()

        # Setup Tester as VSG
        self.tester.initialize()
        self.tester.configure_bt(bt_band, bt_channel)
        self.tester.configure_vsg(sampling_rate, frequency, wavefile, power_level)
        self.tester.initialize_vsg(channel)
        self.tester.configure_wlist(str(packet_count), next_count, length, start_point)

        time.sleep(time_delay)

        # Calculate Results (PER)
        total_packets = packet_count
        received_packets = int(self.dut_link.stop_receiver().hex(), 16)
        received_packets = total_packets if received_packets > total_packets else received_packets
        per = round(((total_packets - received_packets) / total_packets) * 100, 2)

        # Write Results to CSV
        self.csv_write(csv_file, ["Total Packets", str(total_packets)])
        self.csv_write(csv_file, ["Received Packets", str(received_packets)])
        self.csv_write(csv_file, ["PER", str(per)])

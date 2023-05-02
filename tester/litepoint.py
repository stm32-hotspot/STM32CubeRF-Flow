import telnetlib


class LitePoint:
    telnetsession = None

    def connect(self, ip_address: str, port: int):
        self.telnetsession = telnetlib.Telnet(ip_address, port)

    def disconnect(self):
        self.telnetsession.close()

    def send_command(self, command: str):
        self.telnetsession.write(bytes(command, encoding="utf8"))

    def read_response(self) -> str:
        self.send_command("FORM:READ:DATA ASC;\n")  # Set the Output Data Format to ASCII
        return self.telnetsession.read_until(b"\n").decode('ascii')

    def initialize(self) -> str:
        self.send_command("*IDN?\n")  # Request Product Identification
        self.send_command("*RST;\n")  # Reset to Factory Default State
        return self.read_response()

    def configure_bt(self, band: str, channel: str):
        self.send_command("BT;CONF:BAND " + band + "\n")     # Configure the Bluetooth Band
        self.send_command("BT;CONF:CHAN " + channel + "\n")  # Configure the Bluetooth Channel
        self.send_command("BT;HSET:FREQ VSG1\n")             # Program Bluetooth Band & Channel to VSG

    def configure_vsg(self, sampling_rate: str, frequency: str, wavefile: str, power_level: int):
        self.send_command("VSG1;MRST\n")                                # Reset VSG HW to Default
        self.send_command("ROUT1;PORT:RES RF1A,VSG1\n")                 # Enable Rout1 RF1A VSG1 Port
        self.send_command("VSG1;SRAT " + sampling_rate + "\n")          # Set Sampling Rate
        self.send_command("VSG1;FREQ:CENT " + frequency + "\n")         # Set Center Frequency
        self.send_command("VSG1;WAVE:LOAD '" + wavefile + "'\n")        # Load VSG Wavefile
        self.send_command("VSG1;WLIS:WSEG1:DATA '" + wavefile + "'\n")  # Load Pre-Loaded Waveform
        self.send_command("VSG1;WAVE:EXEC ON\n")                        # Enable Wavefile Play
        self.send_command("VSG1;POW:LEV " + str(power_level) + "\n")    # Set VSG1 Output Power
        self.send_command("VSG1;POW:STAT ON\n")                         # Enable VSG1 Output State

    def configure_vsa(
            self, frequency: str, sampling_rate: str, capture_time: str, trigger_source: str, reference_level: str
    ):
        self.send_command("VSA1;MRST\n")                               # Reset VSA HW to Default
        self.send_command("ROUT1;PORT:RES RF1A,VSA1\n")                # Enable Rout1 RF1A VSA1 Port
        self.send_command("VSA1;FREQ:CENT " + frequency + "\n")        # Set Center Frequency
        self.send_command("VSA1;SRAT " + sampling_rate + "\n")         # Set Sampling Rate
        self.send_command("VSA1;CAPT:TIME " + capture_time + "\n")     # Set Capture Time (Seconds)
        self.send_command("VSA1;TRIG:SOUR " + trigger_source + "\n")   # Set Trigger Source
        self.send_command("VSA1;RLEV " + reference_level + "\n")       # Set Reference Level

    def initialize_vsg(self, channel: str):
        self.send_command(channel + ";VSG1;INIT\n")  # Initialize VSG1

    def initialize_vsa(self, channel: str):
        self.send_command(channel + ";VSA1;INIT\n")  # Initialize VSA1

    def configure_wlist(self, count: str, next_count: str, length: str, start_point: str):
        self.send_command("VSG1;WLIS:COUNT " + count + "\n")             # Set WList Count
        self.send_command("VSG1;WLIS:WSEG1:NEXT " + next_count + "\n")   # Set WList Count for Next Segment
        self.send_command("VSG1;WLIS:WSEG1:LENG " + length + "\n")       # Set WList Segment Length
        self.send_command("VSG1;WLIS:WSEG1:STAR " + start_point + "\n")  # Set Wave Start Point
        self.send_command("VSG1;WLIS:COUNT:ENAB WSEG1\n")                # Enable WaveList Looping Counter Functionality
        self.send_command("VSG1;WLIS:WSEG1:SAVE\n")                      # Save Wave Segment
        self.send_command("VSG1;WAVE:EXEC ON,WSEG1\n")                   # Start Playing WaveFile

    def calculate_power(self, packets: str) -> str:
        self.send_command("BT;CALC:POW " + packets + "\n")  # Calculate Power Over Detected Packets
        self.send_command("BT;FETC:POW?\n")                 # Fetch Power for All Detected Packets
        return self.read_response()

    def calculate_power_average(self, packets: str) -> str:
        self.send_command("BT;CALC:POW " + packets + "\n")  # Calculate Power Over Detected Packets
        self.send_command("BT;FETC:POW:AVER?\n")            # Fetch Power Result Average
        return self.read_response()

    def calculate_power_peak(self, packets: str) -> str:
        self.send_command("BT;CALC:POW " + packets + "\n")  # Calculate Power Over Detected Packets
        self.send_command("BT;FETC:POW:PEAK:MAX?\n")        # Fetch Max Peak Power
        return self.read_response()

    def calculate_spectrum(self, packets: str, bandwidth: int) -> str:
        self.send_command("BT;CALC:SPEC " + packets + "\n")            # Calculate Spectrum Over Detected Packets
        self.send_command("BT;FETC:SPEC:" + str(bandwidth) + "BW?\n")  # Fetch 20dB Bandwidth for Packets
        return self.read_response()

    def calculate_spectrum_average(self, packets: str, bandwidth: int) -> str:
        self.send_command("BT;CALC:SPEC " + packets + "\n")                 # Calculate Spectrum Over Detected Packets
        self.send_command("BT;FETC:SPEC:" + str(bandwidth) + "BW:AVER?\n")  # Fetch 20dB Bandwidth for Packets
        return self.read_response()

    def calculate_tx_quality(self, packets: str) -> str:
        self.send_command("BT;CALC:TXQ " + packets + "\n")  # Calculate TX Quality Analysis for Detected Packets
        self.send_command("BT;FETC:TXQ:LEN?\n")             # Fetch BDR TX Quality Results
        return self.read_response()

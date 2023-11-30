from kivy.uix.boxlayout import BoxLayout
from popups import modbusPopup, scanPopup
from pymodbusTCP.client import ModbusClient

class MainWidget(BoxLayout):
    """
    Widget principal
    """
    def __init__(self, **kwargs):
        """
        Construtor
        """
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._scanPopup - scanPopup(self._scan_time)
        self._serverIP = kwargs.get('server_ip')
        self._serverPort = kwargs.get('server_port')
        self._modbuspopup = modbusPopup(self._serverIP, self._serverPort)
        self._modbusClient = ModbusClient(host=self._serverIP, port=self._serverPort)
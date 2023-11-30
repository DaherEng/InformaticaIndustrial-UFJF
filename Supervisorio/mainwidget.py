from kivy.uix.boxlayout import BoxLayout
# from popup import ModbusPopup, Scanpopup
# from pymodbusTCP.client import ModbusClient

class MainWidget(BoxLayout):
    """
    Widget principal
    """
    def __init__(self):
        """
        Construtor
        """
        super().__init__()
        # self._scan_time = kwargs.get('scan_time')
        # self._modbuspopup = ModbusPopup()
        # self._scanPopup - Scanpopup(self._scan_time)
from pyModbusTCP.client import ModbusClient
from pymodbus import payload as pl
from time import sleep

class ClienteMODBUS():
    """
    Classe Cliente MODBUS
    """
    def __init__(self, server_ip,porta,scan_time=1):
        """
        Construtor
        """
        self._cliente = ModbusClient(host=server_ip,port = porta)
        self._scan_time = scan_time

    def lerDado(self, tipo, addr):
        """
        Método para leitura de um dado da Tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.read_holding_registers(addr,1)[0]

        if tipo == 2:
            return self._cliente.read_coils(addr,1)[0]

        if tipo == 3:
            return self._cliente.read_input_registers(addr,1)[0]

        if tipo == 4:
            return self._cliente.read_discrete_inputs(addr,1)[0]
        
        if tipo == 5:
            decoder = pl.BinaryPayloadDecoder.fromRegisters(self._cliente.read_holding_registers(addr, 2), byteorder=pl.Endian.LITTLE)
            valorFloat = decoder.decode_32bit_float()
            return valorFloat
        if tipo ==6:
            bit = input("Qual bit deseja operar:")
            decoder = pl.BinaryPayloadDecoder.fromRegisters(self._cliente.read_holding_registers(addr), byteorder=pl.Endian.LITTLE)
            buffer = decoder.decode_bits(package_len=2)
            return buffer[int(bit)]

    def escreveDado(self, tipo, addr, valor):
        """
        Método para a escrita de dados na Tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.write_single_register(addr,int(valor))

        if tipo == 2:
            return self._cliente.write_single_coil(addr,int (valor))
        if tipo == 3:
            builder = pl.BinaryPayloadBuilder(byteorder=pl.Endian.LITTLE)
            builder.add_32bit_float(float(valor))
            payload = builder.to_registers()
            return self._cliente.write_multiple_registers(addr, payload)
        
        if tipo == 4:
            bit = input("Qual bit deseja operar: ")
            decoder = pl.BinaryPayloadDecoder.fromRegisters(self._cliente.read_holding_registers(addr), byteorder=pl.Endian.LITTLE)
            buffer = decoder.decode_bits(package_len=2)
            valor = input("Qual valor deseja escrever: ")
            buffer[int(bit)] = valor
            return self._cliente.write_single_register(addr,int(valor))
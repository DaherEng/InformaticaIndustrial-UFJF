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

    def atendimento(self):
        """
        Método para atendimento do usuário
        """
        self._cliente.open()
        try:
            atendimento = True
            while atendimento:
                sel = input("Deseja realizar uma leitura, escrita ou configuração? (1- Leitura | 2- Escrita |3- Leitura/Escrita Bitwise |4- Configuração |5- Sair): ")
                
                if sel == '1':
                    tipo = input ("""Qual tipo de dado deseja ler? (1- Holding Register uint_8) |2- Coil |3- Input Register |4- Discrete Input |5- Holding Register float|6- Holding Register Bitwise) :""")
                    addr = input (f"Digite o endereço da tabela MODBUS: ")
                    nvezes = input ("Digite o número de vezes que deseja ler: ")
                    for i in range(0,int(nvezes)):
                        print(f"Leitura {i+1}: {self.lerDado(int(tipo), int(addr))}")
                        sleep(self._scan_time)
                elif sel =='2':
                    tipo = input ("""Qual tipo de dado deseja escrever? (1- Holding Register int) |2- Coil |3- Holding Register float |4- Holding Register Bitwise) :""")
                    addr = input (f"Digite o endereço da tabela MODBUS: ")
                    valor = input (f"Digite o valor que deseja escrever: ")
                    self.escreveDado(int(tipo),int(addr),valor)

                elif sel=='3':
                    scant = input("Digite o tempo de varredura desejado [s]: ")
                    self._scan_time = float(scant)

                elif sel =='4':
                    self._cliente.close()
                    atendimento = False
                else:
                    print("Seleção inválida")
        except Exception as e:
            print('Erro no atendimento: ',e.args)

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
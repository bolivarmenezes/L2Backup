from devices.src.map.TopologyModel import NetworkTopology
from devices.src.layer7.helpersLog import ManagerLog
from pysnmp import hlapi
from devices.src.map import quicksnmp
from devices.src.map.pyconfig import sysName_named_oid, interfaces_table_named_oid, lldp_table_named_oid
from devices.src.mongodb.mongo_device import Mongo
 

class SwitchMapper:

    def __init__(self, root_node:str='st-cpd10-00'):
        '''self.topology_model = NetworkTopology()'''
        self.db = Mongo()
        self.devices = self.db.select_all_devices()
        self.ml = ManagerLog()

        '''Testa nome do switch'''
        self.root_node = str(self.testName(root_node))

    '''
    Testa e valida o nome do switch
    '''
    @staticmethod
    def testName(root_node) -> str:
        if 'st' not in root_node:
            raise "Nome do switch inválido"
        if '.net.ufsm.br' not in root_node:
            root_node = root_node + '.net.ufsm.br'
            return root_node
        else:
            return root_node

    @staticmethod
    def makeJSON(topology_model):
        '''
        Após adicionadas todas a informações, é hora de salvar em JSON
        '''
        topology_model.dumpToJSON()
        del topology_model
        return 0

    def mapper(self):
        self.ml.log("############")
        self.ml.log("# Iniciando #")
        self.ml.log("############")

        topology_model = NetworkTopology()
        '''
        busca as informações dos switches do banco
        '''
        for device in self.devices:
            status = device['online']
            disable = device['disable_st']
            disable_scan = device['disable_scan']
            name = device['name']
            test = False

            if self.root_node in name or self.root_node == name:
                test = True
            if status == '1' and disable == '0' and disable_scan == '0' and test:
                community = device['community']
                device = device['ip']
                '''
                Testando se o SNMP funciona
                '''
                try:
                    sSNMPHostname = quicksnmp.get(device, sysName_named_oid, hlapi.CommunityData(community))
                    self.ml.log(' = '.join([x.prettyPrint() for x in sSNMPHostname]))
                    self.ml.log(" This is how to get to numeric OID: " +
                        str(tuple(sSNMPHostname[0][0])))
                    self.ml.log(" This is how to get data only: " + str(name))
                except RuntimeError as e:
                    self.ml.log("Runtime Error: " + str(e))
                    continue
                except (ValueError, TypeError):
                    self.ml.log("Error " + str(TypeError))
                    continue

                self.ml.log("# A conexão SNMP está funcioando")
                '''
                Pega a tabela de interfaces
                '''
                try:
                    self.ml.log("INTERFACES TABLE: ")
                    rawInterfacesTable = quicksnmp.get_table(device, interfaces_table_named_oid,hlapi.CommunityData(community))

                    for row in rawInterfacesTable:
                        for item in row:
                            self.ml.log(' = '.join([x.prettyPrint() for x in item]))
                        self.ml.log('')

                except RuntimeError as e:
                    self.ml.log("Runtime Error: " + str(e))
                    continue
                except (ValueError, TypeError):
                    self.ml.log("Error " + str(TypeError))
                    continue
                except KeyboardInterrupt:
                    pass

                '''
                LLDP TABLE GET
                '''
                try:
                    self.ml.log("LLDP TABLE: ")
                    self.ml.log("############")
                    rawTable = quicksnmp.get_table(device, lldp_table_named_oid, hlapi.CommunityData(community))

                    for row in rawTable:
                        for item in row:
                            self.ml.log(' = '.join([x.prettyPrint() for x in item]))
                        self.ml.log('')

                except RuntimeError as e:
                    self.ml.log("Runtime Error: " + str(e))
                    continue
                except (ValueError, TypeError):
                    self.ml.log("Error " + str(TypeError))
                    continue

                ''' 
                Popula o modelo com os dados do switch                
                topology_model.addDevice(str(sSNMPHostname[0][1]))
                '''

                '''
                Adiciona o switch principal (principal nesse objeto)
                '''
                topology_model.addDevice(name)

                for row in rawInterfacesTable:
                    # index number from OID
                    oid = tuple(row[0][0])
                    self.ml.log('INDEX: ' + str(oid[-1]))
                    # ifDescr
                    self.ml.log('ifDescr: ' + str(row[0][1]))
                    # ifType
                    self.ml.log('ifType: ' + str(row[1][1]))
                    # ifMtu
                    self.ml.log('ifMtu: ' + str(row[2][1]))
                    # ifSpeed
                    self.ml.log('ifSpeed: ' + str(row[3][1]))
                    # ifPhysAddress
                    self.ml.log('ifPhysAddress: ' + str(row[4][1].prettyPrint()))
                    # ifAdminStatus
                    self.ml.log('ifAdminStatus: ' + str(row[5][1]))
                    # ifOperStatus
                    self.ml.log('ifOperStatus: ' + str(row[6][1]))
                    # ifHCInOctets
                    self.ml.log('ifHCInOctets: ' + str(row[7][1]))
                    # ifHCOutOctets
                    self.ml.log('ifHCOutOctets: ' + str(row[8][1]))
                    # ifHighSpeed
                    self.ml.log('ifHighSpeed: ' + str(row[9][1]))
                    self.ml.log("")
                    '''
                    Interfaces do switch principal
                    '''
                    topology_model.addDeviceInterface(str(name),  # deviceid
                                                      oid[-1],  # INDEX
                                                      str(row[0][1]),  # ifDescr
                                                      str(row[1][1]),  # ifType
                                                      str(row[2][1]),  # ifMtu
                                                      str(row[3][1]),  # ifSpeed
                                                      # ifPhysAddress
                                                      str(row[4][1].prettyPrint()),
                                                      str(row[5][1]),  # ifAdminStats
                                                      str(row[6][1]))  # ifOperStatus
                    '''
                    Status das Interfaces do switch principal
                    '''
                    topology_model.addInterfaceStats(str(name),  # deviceid
                                                     oid[-1],  # INDEX
                                                     str(row[0][1]),  # ifDescr
                                                     str(row[1][1]),  # ifType
                                                     str(row[6][1]),  # ifOperStatus
                                                     str(row[7][1]),  # ifHCInOctets
                                                     str(row[8][1]),  # ifHCOutOctets
                                                     str(row[9][1]))  # ifHighSpeed

                self.ml.log('links from LLDP')
                for row in rawTable:
                    # lldpRemSysName
                    self.ml.log('lldpRemSysName: ' + str(row[0][1]))
                    # lldpRemSysDesc
                    self.ml.log('lldpRemSysDesc: ' + str(row[1][1]))
                    # lldpRemPortId
                    self.ml.log('lldpRemPortId: ' + str(row[2][1]))
                    # lldpRemPortDesc
                    self.ml.log('lldpRemPortDesc: ' + str(row[3][1]))


                    oid = tuple(row[0][0])
                    local_in_index = oid[-2]
                    # Pega o nome das interfaces via LLDP local int table
                    local_interface_name = quicksnmp.get(device, [('LLDP-MIB', 'lldpLocPortId', local_in_index)],
                                                         hlapi.CommunityData(community))

                    '''
                    Mais tarde, será feito uma validação para os nomes dessas interfaces (local_interface_name)
                    '''

                    # Repairing H3Cs bad indexes by searching for index via name
                    local_in_index = topology_model.getDeviceInterfaceIndex(
                        str(name), str(local_interface_name[0][1]))

                    self.ml.log("Local_interface_name: " + str(local_interface_name[0][1]))
                    self.ml.log(' = '.join([x.prettyPrint() for x in local_interface_name]))

                    '''
                    Adiciona os links
                    '''
                    topology_model.addLink(str(name),  # node_a
                                           str(row[0][1]),  # node_b
                                           topology_model.getLinkSpeedFromName(
                                               str(row[2][1])),
                                           local_in_index,  # a_local_int_index
                                           # a_local_int_name
                                           str(local_interface_name[0][1]),
                                           str(row[2][1])  # lldpRemPortId
                                           )

                    self.ml.log("Localintindex : " + str(local_in_index))
                    topology_model.addNeighborships(str(name),
                                                    local_in_index,
                                                    str(local_interface_name[0][1]),
                                                    str(row[0][1]),
                                                    str(row[2][1]))
        '''Cria JSON'''
        self.makeJSON(topology_model)




if __name__ == "__main__":
    sm = SwitchMapper('st-agittec-10.net.ufsm.br')
    sm.mapper()
from configobj import ConfigObj
import devices.database.path_of_files as path_file
import re


class ToolsSwitch:

    @staticmethod
    def number_of_ports(vendor, model):
        template = ConfigObj(path_file.template_vendors)
        number_of_ports = 0
        all_ports = 0
        try:
            number_of_ports = template[vendor][model]
            all_ports: dict = {}
            for port in number_of_ports['range_ports']:
                all_ports[port] = 'NaN'
        except KeyError:
            print(f"Fabricante {vendor} ou o Modelo {model} não foram cadastrados!")

        return all_ports

    @staticmethod
    def format_port(port: str = '0', vendor: str = 'NaN', model: str = 'NaN') -> str:
        new_port = ''
        if port == '0':
            if vendor != 'NaN' and model != 'NaN':
                template = ConfigObj(path_file.template_vendors)
                #print(vendor, model)
                dict_data = template[vendor][model]
                return dict_data['range_ports']

        else:
            if vendor != 'NaN' and model != 'NaN':
                template = ConfigObj(path_file.template_vendors)
                try:
                    ports = template[vendor][model]
                    for new_port in ports['range_ports']:
                        if port in new_port:
                            return new_port
                except KeyError:
                    print(f"Fabricante {vendor} ou o Modelo {model} não foram cadastrados!")

            # testa se tem Giga no nome
            if "Gi" in port or "gi" in port or 'Giga' in port or 'giga' in port:
                # GigabitEthernet1/0/48
                new_port = re.findall(r'[0-9]{1,2}', port, flags=re.IGNORECASE)[-1] + 'G'
            # testa se é 10 Gb
            elif 'ten' in port or 'Ten' in port or 't' in port or 'te' in port or 'Te' in port:
                new_port = re.findall(r'[0-9]{1,2}', port, flags=re.IGNORECASE)[-1] + 'Te'
            else:
                new_port = re.findall(r'[0-9]{1,2}', port, flags=re.IGNORECASE)[-1]

        return new_port

from devices.src.switches.switch import Switch
from devices.src.switches.vendor.cisco import Cisco


class Context():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: Switch) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> Switch:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Switch) -> None:
        self._strategy = strategy

    def do_some_business_logic(self) -> None:
        result = self._strategy.get_lldp_by_snmp()
        print(result)


if __name__ == "__main__":
    # The client code picks a concrete strategy and passes it to the context.
    # The client should be aware of the differences between strategies in order
    # to make the right choice.
    vendor = Cisco('192.168.19.2')
    context = Context(vendor)
    context.do_some_business_logic()

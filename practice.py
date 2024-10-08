import pyvisa
import time
import logging
from Instrument import load_type

# pyvisa.log_to_screen()
# logging.basicConfig(level=logging.DEBUG)


def main():
    address = "USB0::6833::1230::DS1ZC232903376::0::INSTR"
    # address = "USB0::6833::3601::DL3B233700641::0::INSTR"
    rm = pyvisa.ResourceManager()
    # resource_list = rm.list_resources("?*USB*")
    resource_list = rm.list_resources()
    print(resource_list)
    # rm = pyvisa.ResourceManager()
    # resource_list = rm.list_resources()
    # print(resource_list)

    scope = rm.open_resource(address)
    scope.name = scope.query("*IDN?")
    print(scope.name)

    time.sleep(1)
    scope.close()
    rm.close()


if __name__ == "__main__":
    main()
    # scopes = load_type("Scope")
    # scope = list(scopes.values())[0]
    # print(scope.resource.query("*IDN?"))

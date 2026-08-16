from datetime import datetime

class Logger:
    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
    
    def log(self, massage: str) -> None:
        time_section = "[" + str(datetime.now().isoformat(sep=" ", timespec="seconds")) + "]"
        module_name_section = "[" + self.module_name + "]"
        massage_section = "[" + massage + "]"
        log = time_section + module_name_section + massage_section
        print(log)
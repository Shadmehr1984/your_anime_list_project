class ReportMaker:
    report_base_address = "C:/Users/Mehrshad1/Desktop/project/your anime list project/reports/"
    
    def __init__(self, report_name: str) -> None:
        self.report_name = report_name
        self.report_first_half = None
        self.item_template = None
        self.report_items = []
        self.report_second_half = None
    
    def set_report_first_half(self, report_first_half: str):
        self.report_first_half = report_first_half
    
    def set_report_second_half(self, report_second_half: str):
        self.report_second_half = report_second_half
    
    def set_item_template(self, item_template: str):
        self.item_template = item_template
    
    def add_item(self, parameters: tuple):
        if self.item_template == None : raise AttributeError("item template is not set")
        
        item = self.item_template % parameters
        
        self.report_items.append(item)
    
    def make(self):
        if self.report_first_half == None: raise AttributeError("report first half is not set")
        if self.report_second_half == None: raise AttributeError("report second half is not set")
        if len(self.report_items) == 0: raise AttributeError("report items is not set")
        
        report = self.report_first_half
        
        items = ""
        
        for item in self.report_items:
            items = f"{items}{item}"
        
        report = f"{report}{items}"
        
        report = f"{report}{self.report_second_half}"
        
        report_address = f"{ReportMaker.report_base_address}{self.report_name}"
        
        with open(report_address, "w") as report_file:
            report_file.write(report)
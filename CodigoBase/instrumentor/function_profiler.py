from abstract_profiler import Profiler
from function_instrumentor import *
from function_record import FunctionRecord

# Clase que rastrea y reporta las funciones que se ejecutan
class FunctionProfiler(Profiler):

    # Metodo que se llama cada vez que se ejecuta una funcion
    @classmethod
    def record_start(cls, functionName, args):
        cls.getInstance().fun_call_start(functionName, args)

    @classmethod
    def record_end(cls, functionName, returnValue):
        cls.getInstance().fun_call_end(functionName, returnValue)
        return returnValue

    # Este metodo inyecta codigo en el programa segun el visitor del profiler
    @classmethod
    def instrument(cls, ast):
        visitor = FunctionInstrumentor()
        return fix_missing_locations(visitor.visit(ast))
    
    # Metodos de instancia
    def __init__(self):
        self.records = {}
        self.exec_hystory = {}
        self.parent_function = None

    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    def fun_call_start(self, functionName, args):
        record = self.get_record(functionName) # Retorna objeto FunctionRecord y crea uno si no existe
        record.add_caller(self.parent_function)
        self.parent_function = record.functionName
        self.update_record_frecuency(record)
        self.update_exec_history_record(functionName, args)

    def fun_call_end(self, functionName, returnValue):
        self.parent_function = None
        self.append_value_to_exec_record(functionName, returnValue)
        self.update_record_cacheable_status(functionName)

    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10}".format('fun', 'freq', 'cache', 'callers'))
        for record in self.records.values():
            record.print_report()

    def report_executed_functions(self):
        self.print_fun_report()
        return self.records
    
    def update_record_frecuency(self, record):
        record.frequency += 1
        return record
    
    def update_exec_history_record(self, functionName, args):
        if self.exec_hystory.get(functionName) is None:
            self.create_exec_history_record(functionName)
        self.append_arg_to_exec_record(functionName, args)

    def create_exec_history_record(self, functionName):
        self.exec_hystory[functionName] = {
            "args": [],
            "value": []
        }

    def append_arg_to_exec_record(self, functionName, args):
        self.exec_hystory[functionName]["args"].append(args)

    def append_value_to_exec_record(self, functionName, value):
        self.exec_hystory[functionName]["value"].append(value)

    def update_record_cacheable_status(self, functionName):
        if self.are_there_repeted_values(self.exec_hystory[functionName]["value"]) or self.are_there_repeted_values(self.exec_hystory[functionName]["args"]):
            self.records[functionName].cacheable = False

    def are_there_repeted_values(self, list):
        if len(list) <= 1:
            return False

        first_element = list[0]
        for element in list[1:]:
            if element != first_element:
                return True
        return False 
    
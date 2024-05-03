import sys
import ast
import inspect
from types import *
import traceback
from stack_inspector import StackInspector
## Agregamos LineRecord
from line_record import LineRecord

""" Clase para la Tarea 2. Para su uso, considere:
with CoverageTracer() as covTracer:
    function_to_be_traced()

covTracer.report_executed_lines()
"""

class CoverageTracer(StackInspector):

    def __init__(self):
        super().__init__(None, self.traceit)
        # Completa el codigo necesario
        self.executed_lines = {}

    # Completa la funcion de rastreo
    def traceit(self, frame, event: str, arg):
        # Completa el codigo necesario
        if event == "line":
            function_name = frame.f_code.co_name
            lineno = frame.f_lineno
            func_key = (function_name, lineno)

            # Evitamos rastrearnos a nosotros
            # Codigo extraido de FunctionTracer
            if not self.our_frame(frame) and not self.problematic_frame(frame): 
                if func_key in self.executed_lines:
                    self.executed_lines[func_key].increaseFrequency()
                else:
                    func_name = frame.f_code.co_name
                    self.executed_lines[func_key] = LineRecord(func_name, lineno)

        return self.traceit

    def print_lines_report(self):
        print("{:<30} {:<10} {:<10}".format('fun', 'line', 'freq'))
        for line_record in sorted(self.executed_lines.values(), key=lambda a: a.lineNumber):
            line_record.print_report()
        
        

    def report_executed_lines(self):
        self.print_lines_report()
        # Completa el codigo necesario
        return [line_record for line_record in self.executed_lines.values()]

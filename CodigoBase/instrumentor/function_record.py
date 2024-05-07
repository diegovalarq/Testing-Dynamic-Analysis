class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName
        self.frequency = 0
        self.cacheable = True
        self.callers = []

    def isCacheable(self):
        return self.cacheable
        
    def print_report(self):
        print("{:<30} {:<10} {:<10} {}".format(self.functionName, self.frequency, self.cacheable, self.callers))

    def __eq__(self, other):
        if isinstance(other, FunctionRecord):
            return self.functionName == other.functionName and self.frequency == other.frequency and self.isCacheable() == other.isCacheable() and self.callers == other.callers
        return False

    @classmethod
    def new_instance_with(cls, funName, frequency, cacheable, callers):
        instance = cls(funName)
        instance.frequency = frequency
        instance.cacheable = cacheable
        instance.callers = callers
        return instance
    
    def add_caller(self, caller):
        if caller is not None and caller not in self.callers:
            self.callers.append(caller)
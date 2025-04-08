class Optimizer():
    def __init__(self, object, func: function, parameters: dict, F: dict, H: dict, G: dict):
        self.object = object
        self.func = func
        self.parameters = parameters
        self.F = F
        self.H = H
        self.G = G
    
    def evaluate(self):
        result = self.func(self.object)
        self.f = []
        self.h = []
        self.g = []
        for F in self.F:
            minimize = result.getattr(F, None)
            self.f.append(minimize)
        for H in self.H:
            equal = result.getattr(H, None)
            self.h.append(equal)
        for G in self.G:
            constraint = result.getattr(G, None)
            self.g.append(constraint)

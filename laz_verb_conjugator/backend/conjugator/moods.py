class Conjugator:
    
    def __init__(self, verb, region, subject, tense, modes, object):
        
        self.verb = verb
        self.region = region
        self.subject = subject
        self.tense = tense
        self.modes = modes
        self.object = object

    def conjugate(self):
        pass


class ImperativeConjugator(Conjugator):
    
    def conjugate(self):
        pass
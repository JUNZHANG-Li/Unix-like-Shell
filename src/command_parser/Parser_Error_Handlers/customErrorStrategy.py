from antlr4.error.ErrorStrategy import BailErrorStrategy

Parser = None


class customErrorStrategy(BailErrorStrategy):
    def __init__(self):
        super().__init__()

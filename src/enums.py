from enum import Enum

class Ticker(Enum):
    MAERSK = 'MAERSK-B.CO'
    AMBU = 'AMBU-B.CO'
    BAVA = 'BAVA.CO'
    CARL = 'CARL-B.CO'
    COLO = 'COLO-B.CO'
    DANSKE = 'DANSKE.CO'
    DEMANT = 'DEMANT.CO'
    DSV = 'DSV.CO'
    GMAB = 'GMAB.CO'
    GN = 'GN.CO'
    ISS = 'ISS.CO'
    JYSK = 'JYSK.CO'
    NKT = 'NKT.CO'
    NOVO = 'NOVO-B.CO'
    NSIS = 'NSIS-B.CO'
    PANDORA = 'PNDORA.CO'
    ROCK = 'ROCK-B.CO'
    RBREW = 'RBREW.CO'
    SYDB = 'SYDB.CO'
    TRYG = 'TRYG.CO'
    VWS = 'VWS.CO'
    ZEAL = 'ZEAL.CO'
    ORSTED = 'ORSTED.CO'

    @classmethod
    def list(cls):
        return [ticker.value for ticker in cls]
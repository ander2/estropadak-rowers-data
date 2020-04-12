import logging

logger = logging.getLogger('estropadak')
logger.setLevel('DEBUG')


def compare_rower_name(r1, r2):
    r1 = r1.lower()
    r2 = r2.lower()
    trans = str.maketrans('áéíóú', 'aeiou')
    return r1.translate(trans) == r2.translate(trans)


def calculate_alta_baja(aurtengoa, aurrekoa, team):
    '''
        Taken staff from this year and previous year, return
        how many new rowers and rowers left there are
    '''
    altak = []
    bajak = []

    aurtengo_arraunlariak = aurtengoa[team]
    aurreko_arraunlariak = aurrekoa[team]
    logger.debug('Calculating alta-baja for %s', team)
    for a in aurtengo_arraunlariak:
        izena = a.name
        badago = [
            b.name
            for b in aurreko_arraunlariak
            if compare_rower_name(a.name, b.name)
        ]
        if len(badago) == 0:
            altak.append(izena)

    for a in aurreko_arraunlariak:
        badago = [
            b.name
            for b in aurtengo_arraunlariak
            if compare_rower_name(a.name, b.name)
        ]
        if len(badago) == 0:
            bajak.append(a.name)

    logger.debug('Calculating alta-baja for %s finished', team)
    return altak, bajak

def calculate_alta_baja(aurtengoa, aurrekoa, team):
    ''' 
        Taken staff from this year and previous year, return
        how many new rowers and rowers left there are
    ''' 
    altak = []
    bajak = []

    aurtengo_arraunlariak = aurtengoa[team]
    aurreko_arraunlariak = aurrekoa[team]
    print(team)
    for a in aurtengo_arraunlariak:
        print(a.name)
        izena = a.name
        badago = [b.name for b in aurreko_arraunlariak if a.name == b.name]
        if len(badago) == 0:
            altak.append(izena)

    for a in aurreko_arraunlariak:
        badago = [b.name for b in aurtengo_arraunlariak if a.name == b.name]
        if len(badago) == 0:
            bajak.append(a.name)

    return altak, bajak
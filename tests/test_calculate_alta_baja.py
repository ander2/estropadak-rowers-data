import pickle
from utils.calculate_alta_baja import calculate_alta_baja


def test_calculate_alta_baja():
    data = None
    team = 'Hondarribia'
    with open(f'./results/act_data', 'rb') as f:
        data = pickle.load(f)
    aurtengoa = data[2016] # [team]
    aurrekoa = data[2015] #[team]
    (altak, bajak) = calculate_alta_baja(aurtengoa, aurrekoa, team)
    assert(len(altak) == 3)
    assert(len(bajak) == 2)
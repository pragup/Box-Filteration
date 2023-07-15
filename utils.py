from math import log
import numpy as np
import matplotlib.pyplot as plt
import json

def homology_group(persistence, group=1):
    persistence_filter = []
    for point in persistence:
        if point[0] == 1: persistence_filter.append(point)
    return persistence_filter
def persistence_entropy(persistence, max_group=1):

    entropy = {}
    max_life = {}
    life_sum = {}
    max_life_prob = {}

    for i in range(max_group+1):
        entropy.update({i: 0})
        max_life.update({i: 0})
        life_sum.update({i: 0})
        max_life_prob.update({i: 0})

    for point in persistence:
        if point[1][1] == np.inf: continue
        life = (point[1][1] - point[1][0])
        if max_life[point[0]] < life:
            max_life[point[0]] = life
    min_life = max_life.copy()

    for point in persistence:
        if point[1][1] == np.inf: continue
        life = (point[1][1] - point[1][0])
        if min_life[point[0]] > life:
            min_life[point[0]] = life

    # print(max_life, min_life)

    # normalize the values #
    life_norm = []
    for point in persistence:
        life = (point[1][1] - point[1][0])
        if max_life[point[0]] - min_life[point[0]] == 0:
            temp = 1
        else:
            temp = (life - min_life[point[0]])/(max_life[point[0]] - min_life[point[0]])
        life_norm.append((point[0], temp))
    max_life = entropy.copy()

    for p in life_norm:
        if p[1] == np.inf: continue
        life_sum[p[0]] = life_sum[p[0]] + p[1]
        if max_life[p[0]] < p[1]:
            max_life[p[0]] = p[1]

    # compute entropy #
    for p in life_norm:
        if p[1] == np.inf: continue
        temp = (p[1] / life_sum[p[0]]) + 10**(-12)
        temp = temp * log(temp, 2)
        entropy[p[0]] = entropy[p[0]] - temp

    # compute max hole property #
    for i in range(max_group + 1):
        max_life_prob[i] = max_life[i]/life_sum[i]

    return {"entropy":entropy, "max_life_prob":max_life_prob}


def plot_entropy(params, y_name, hgroup=1):

    with open("output_vr/vrPersistenceEntropy.json", 'r') as myfile:
        data = myfile.read()
    # parse file
    vr_dict = json.loads(data)

    with open("output_dtm/dtmPersistenceEntropy.json", 'r') as myfile:
        data = myfile.read()
    # parse file
    dtm_dict = json.loads(data)

    with open("output_bf/bfPersistenceEntropy.json", 'r') as myfile:
        data = myfile.read()
    # parse file
    bf_dict = json.loads(data)


    y_bf = []
    y_dtm = []
    for param in params:
        y_bf.append(bf_dict[str(param)][y_name][str(hgroup)])
        param = np.round(1 - param, 1)
        y_dtm.append(dtm_dict[str(param)][y_name][str(hgroup)])

    plt.axhline(y=vr_dict[y_name][str(hgroup)], color='r', linestyle='-', label="VR")
    plt.plot(params, y_bf, color='b', linestyle='-', label="BF")
    plt.plot(params, y_dtm, color='g', linestyle='-', label="DTM")
    plt.xlabel("alpha (BF), 1 - m (DTM)")
    plt.ylabel(y_name)
    plt.legend(loc="upper right", fontsize=8)
    plt.title("H_"+str(hgroup))
    return plt

def plot_max_prob(hgroup=1):
    pass

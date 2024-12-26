import math
import numpy as np

condition = [
    [4, 1, 8, 7, 4, 5, 3, 6, 1],
    [9, 3, 3, 9, 7, 6, 4, 10, 8],
    [6, 8, 5, 5, 10, 4, 8, 7, 1],
    [4, 8, 4, 6, 7, 2, 2, 7, 3],
    [1, 8, 6, 4, 4, 3, 10, 6, 8],
    [8, 4, 5, 2, 7, 2, 3, 7, 2],
    [7, 7, 7, 8, 2, 7, 4, 8, 4],
    [4, 4, 5, 3, 3, 3, 10, 4, 10],
    [6, 3, 1, 3, 8, 7, 5, 4, 4],
    [2, 7, 6, 5, 2, 10, 9, 5, 1],
    [5, 4, 3, 2, 7, 9, 10, 8, 9],
    [5, 4, 7, 7, 9, 6, 6, 2, 4],
    [1, 1, 1, 3, 10, 10, 10, 6, 2],
    [3, 2, 8, 7, 5, 8, 9, 2, 9],
    [7, 3, 10, 2, 3, 2, 1, 1, 9]
]

weight = [0.07, 0.19, 0.17, 0.13, 0.11, 0.01, 0.19, 0.01, 0.12]


optimization1 = ["max", "max", "max", "max", "max", "max","max", "max", "max"]

v = 1

def check_optimization(optimization):
    isAllMax = True
    for i in range(0, len(optimization)):
        if optimization[i] != "max":
            isAllMax = False
            break

    return isAllMax


def normalization_of_estimations(optimization):
    normalized = condition
    transponate = np.array(condition).transpose()
    sum = []
    desired_values = []
    worst_values = []
    if check_optimization(optimization) == True:
        for i in range(0, len(transponate)):
            sum_of_column = 0.00
            for j in range(0, len(transponate[i])):
                sum_of_column += math.pow(condition[j][i], 2)
            sum.append(sum_of_column)
        for i in range(0, len(normalized)):
            for j in range(0, len(normalized[i])):
                normalized[i][j] = normalized[i][j] / math.sqrt(sum[j])

    print("Нормалізовані оцінки альтернатив")
    for i in range(0, len(normalized)):
        for j in range(0, len(normalized[i])):
            print('%1.4f' % round(normalized[i][j], 4), end=" ")
        print()
    return normalized


def weighted_estimations(optimization):
    estimations = normalization_of_estimations(optimization)
    weight_sum = 0
    for i in range(0, len(weight)):
        weight_sum += weight[i]
    for i in range(0, len(weight)):
        weight[i] /= weight_sum
    for i in range(0, len(estimations)):
        for j in range(0, len(estimations[i])):
            estimations[i][j] *= weight[j]
    print()
    print("Зважені нормалізовані оцінки альтернатив")
    for i in range(0, len(estimations)):
        for j in range(0, len(estimations[i])):
            print('%1.4f' % round(estimations[i][j], 4), end=" ")
        print()

    return estimations


def find_nis(estimations):
    weighted_estimations = np.array(estimations).transpose()
    nis = []
    for i in range(0, len(weighted_estimations)):
        min_value = np.array(weighted_estimations[i]).min()
        nis.append(min_value)
    print('\nАнтиутопічна точка NIS')
    for j in range(0, len(nis)):
        print('%1.4f' % round(nis[j], 4), end=" ")
    return nis


def find_pis(estimations):
    weighted_estimations = np.array(estimations).transpose()
    pis = []
    for i in range(0, len(weighted_estimations)):
        max_value = np.array(weighted_estimations[i]).max()
        pis.append(max_value)
    print('\nУтопічна точка PIS')
    for j in range(0, len(pis)):
        print('%1.4f' % round(pis[j], 4), end=" ")
    return pis


def distance_to_pis(PIS, weighted_estimations):
    d_better = []
    for i in range(0, len(weighted_estimations)):
        difference = 0.00
        for j in range(0, len(weighted_estimations[i])):
            difference += math.pow(weighted_estimations[i][j] - PIS[j], 2)
        d_better.append(math.sqrt(difference))
        

    print('\nD*')
    for j in range(0, len(d_better)):
        print('%1.4f' % round(d_better[j], 4), end=" ")
    return d_better


def distance_to_nis(NIS, weighted_estimations):
    d_worse = []
    for i in range(0, len(weighted_estimations)):
        difference = 0.00
        for j in range(0, len(weighted_estimations[i])):
            difference += math.pow(weighted_estimations[i][j] - NIS[j], 2)
        d_worse.append(math.sqrt(difference))
    print('\n\nD-')
    for j in range(0, len(d_worse)):
        print('%1.4f' % round(d_worse[j], 4), end=" ")
    return d_worse


def proximity(d_pis, d_nis):
    ck = []
    for i in range(0, len(d_pis)):
        ck.append(d_nis[i] / (d_pis[i] + d_nis[i]))
    print('\n\nC*')
    for j in range(0, len(ck)):
        print('%1.4f' % round(ck[j], 4), end=" ")
    return ck


def topsis(optimization):
    estimations = weighted_estimations(optimization)

    PIS = find_pis(estimations)
    NIS = find_nis(estimations)

    print("\n\nВідстані альтернатив до PIS, NIS та ступінь наближеності до утопічної точки")
    d_pis = distance_to_pis(PIS, estimations)
    d_nis = distance_to_nis(NIS, estimations)
    ck = proximity(d_pis, d_nis)
    alternatives = np.argsort(np.array(ck))
    alternatives = [x + 1 for x in alternatives]
    print("\n\nНайкраща альтернатива ", (alternatives[len(alternatives) - 1]))
    print("Ранжування ", alternatives[::-1])


topsis(optimization1)

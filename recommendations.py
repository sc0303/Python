# Write by SunChuan on 2016/06/05
import math
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

# print(critics['Lisa Rose']['Lady in the Water'])

def distance(data, person1, person2):
    item = {}
    distanceSum = 0
    for tmp in data[person1]:
        if tmp in data[person2]:
            item[tmp] = 1

    if len(item) == 0: return None
    else:
        # for key in item:
        #     distanceSum = distanceSum + pow(data[person1][key] - data[person2][key],2)
        distanceTmp = sum(pow(data[person1][itemTmp]-data[person2][itemTmp], 2) for itemTmp in item)
        return 1 / (math.sqrt(distanceTmp) + 1)


def pearson(data, person1, person2):
    item = {}
    pearsonDistance = 0
    for tmp in data[person1]:
        if tmp in data[person2]:
            item[tmp] = 1
    n = len(item)
    if n == 0: return None
    else:
        sum1 = sum([data[person1][key1] for key1 in item])
        sum2 = sum([data[person2][key2] for key2 in item])

        sum1P = sum(pow(data[person1][key1], 2) for key1 in item)
        sum2P = sum(pow(data[person2][key2] ,2) for key2 in item)
        pSum = sum(data[person1][key] * data[person2][key] for key in item)

        num = pSum-(sum1*sum2/n)
        den = math.sqrt((sum1P-pow(sum1,2)/n)*(sum2P-pow(sum2,2)/n))
        return num / den

def topMatch(data, person, topNum, similarity = pearson):
    scores = [(pearson(data, person, value), value) for value in data if value != person]
    scores.sort(reverse = True)
    return scores

def getRecommendation(data, person, similarity = pearson):
    totals = {}
    simSums = {}

    for p in data:
        if p == person: continue
        sim = similarity(data, p, person)
        #忽略评价小于零的数据
        if sim <= 0: continue
        for value in data[p]:
            if value not in data[person] or data[person][value] == 0:
                totals.setdefault(value, 0)
                totals[value] = totals[value] + data[p][value] * sim

                simSums.setdefault(value, 0)
                simSums[value] = simSums[value] + sim

    rankings = [(key, value/simSums[key]) for key, value in totals.items()]
    rankings.sort(reverse = True)
    return rankings


def transform(data):
    result = {}
    for key in data:
        for value in data[key]:
            # print(result)
            result.setdefault(value, {})
            # print(result)
            # result[value] = (value, {})
            result[value][key] = data[key][value]

    return result


def itemSim(data, n = 10):
    res = {}
    dataT = transform(data)
    c = 0
    for key in dataT:
        c = c + 1
        if c % 100 == 0: print("%d, %d" % (c, len(dataT)))
        scores = topMatch(dataT,key,topNum = n, similarity = distance)
        res[key] = scores
    return res

#################to be continued
def getItemRec(data, itemSim, user):
    userData = data[user]
    scores = {}
    totalSum = {}

    for (key, value) in userData.items():
        for()




# dis = distance(critics,'Lisa Rose','Gene Seymour')
# print(dis)
# pearsonDis = pearson(critics,'Lisa Rose','Gene Seymour')
# print(pearsonDis)
# print(topMatch(critics, 'Toby', similarity = pearson, topNum = 5))
# myRank = getRecommendation(critics, 'Toby', similarity=pearson)
# print(myRank)
# print(critics)
# print(transform(critics))
myItemSim = itemSim(critics,n = 10)
print(myItemSim)
# c = 10
# print("x = %s, y = %s" %(c, c))
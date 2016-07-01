# Write by SunChuan on 20160622
import math
import random
import time

people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
# Laguardia
destination = 'LGA'

flight = {}
for line in open('D:/DataMining/machinelearninginaction/PCI_Code Folder/chapter5/schedule.txt'):
    origin, destination_tmp, start_time, arrive_time, price = line.strip().split(',')
    flight.setdefault((origin, destination_tmp), [])
    flight[(origin, destination_tmp)].append((start_time, arrive_time, int(price)))  # 注意append的用法


def get_minutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]


def print_schedule(r):
    for d in range(int(len(r) / 2)):
        name = people[d][0]
        origin = people[d][1]
        out = flight[origin, destination][r[d * 2]]  # 列表使用起来太灵活了！！！！
        back = flight[origin, destination][r[d * 2 + 1]]
        print('%10s%10s %5s - %5s $%3s %5s - %5s $%3s' % (
            name, origin, out[0], out[1], out[2], back[0], back[1], back[2]))  # 注意多个输出如何使用


def schedulecost(sol):
    total_price = 0
    last_arrivarl = 0
    earliest_dep = 24 * 60
    for i in range(int(len(sol) / 2)):
        origin = people[i][1]
        # 得到往返航班
        # print(sol[i * 2])
        try:
            out = flight[(origin, destination)][int(sol[i * 2])]
            back = flight[(origin, destination)][int(sol[i * 2 + 1])]
        except:
            # with open('D:/DataMining/machinelearninginaction/PCI_Code Folder/chapter5/tmp.txt','w') as file:
            #     file.write(str(flight))
            print(flight)
            print(sol)
            print(origin)
            print(destination)
            print(i * 2 + 1)
            print(sol[i * 2 + 1])
            print('hello')

        total_price += out[2] + back[2]
        if last_arrivarl < get_minutes(out[1]): last_arrivarl = get_minutes(out[1])
        if earliest_dep > get_minutes(back[0]): earliest_dep = get_minutes(back[0])
    total_wait = 0

    for i in range(int(len(sol) / 2)):
        origin = people[i][1]
        try:
            out = flight[(origin, destination)][int(sol[i * 2])]
            back = flight[(origin, destination)][int(sol[i * 2 + 1])]
        except:
            print(sol)
            print(i * 2 + 1)
            print(sol[i * 2 + 1])
            print(origin)
            print(destination)
            print('hello')

        total_wait = total_wait + last_arrivarl - get_minutes(out[1]) + get_minutes(back[0]) - earliest_dep

    if last_arrivarl > earliest_dep: total_price = total_price + 50
    return total_wait + total_price


def random_optimize(random_num, costf):
    best_cost = 99999999
    best_r = None
    random_input = [random.randint(random_num[i][0], random_num[i][1]) for i in range(len(random_num))]
    for i in range(1000):
        cost_tmp = costf(random_input)
        if best_cost > cost_tmp:
            best_cost = cost_tmp
            best_r = random_input
    return best_cost, best_r


def hill_climb(random_num, costf):
    random_input = [random.randint(random_num[i][0], random_num[i][1]) for i in range(len(random_num))]
    cycle_time = 0
    while 1:
        neighbour = []
        for j in range(len(random_input)):
            if random_input[j] > random_num[j][0]:
                neighbour.append(random_input[0:j] + [random_input[j] - 1] + random_input[j + 1:])
            if random_input[j] < random_num[j][1]:
                neighbour.append(random_input[0:j] + [random_input[j] + 1] + random_input[j + 1:])
        current_cost = costf(random_input)
        best = current_cost
        for k in range(len(neighbour)):
            cost = costf(neighbour[k])
            if cost < best:
                best = cost
                random_input = neighbour[k]
        cycle_time += 1
        if current_cost == best: break
    print(cycle_time)
    return random_input, best


def annealing_optimize(domain, costf, T=10, cool=0.95, step=1):
    vec_input = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

    while T > 0.1:
        i = random.randint(0, len(domain) - 1)

        dir = random.randint(-step, step)
        vec_tmp = vec_input[:]
        vec_tmp[i] += dir

        # 确保调整后的数据不超出范围
        if vec_tmp[i] < domain[i][0]:
            vec_tmp[i] = domain[i][0]
        elif vec_tmp[i] > domain[i][1]:
            vec_tmp[i] = domain[i][1]

        ea = costf(vec_input)
        eb = costf(vec_tmp)
        if (eb < ea or random.random() < pow(math.e, -(eb - ea) / T)):
            vec_input = vec_tmp
        T = T * cool
    return vec_input


def genetic_optimize(domain, cosf, popsize=50, step=1, mutprob=0.2, elite=0.2, maxtier=100):
    # 变异操作
    def mutate(vec):
        i = random.randint(0, len(domain) - 1)
        if (random.random() < 0.5 and vec[i] > domain[i][0]):
            return vec[0:i] + [vec[i] + step] + vec[i + 1:]
        else:
            return vec[0:i] + [vec[i] - step] + vec[i + 1:]

    # 交差操作
    def corss_over(r1, r2):
        i = random.randint(0, len(domain))
        return r1[0:i] + r2[i:]

    # 构造初始群

    pop = []
    for i in range(maxtier):
        vec = [random.randint(domain[1][0], domain[1][1]) for i in range(len(domain))]
        pop.append(vec)
    print(pop)
    # 每一代中胜出的数量
    top_elite = int(elite * popsize)
    for i in range(maxtier):
        scores = [(cosf(s), s) for s in pop]
        scores.sort()
        ranked = [value for (key, value) in scores]  #####使用起来非常非常灵活，太赞了！！！！！！！！！！！！
        pop = ranked[0: top_elite]

        while len(pop) < popsize:
            if random.random() < mutprob:
                c = random.randint(0, top_elite)
                pop.append(mutate(ranked[c]))
            else:
                c1 = random.randint(0, top_elite)
                c2 = random.randint(0, top_elite)
                pop.append(corss_over(ranked[c1], ranked[c2]))
        print(scores[0][0])
    return scores[0][1]

#
# random_num = [(0, 9)] * len(people) * 2
#
# best_cost, best_r = random_optimize(random_num, schedulecost)
# print(best_cost)
# print_schedule(best_r)
# print('###########################################################################################')
#
# random_input, best_cost = hill_climb(random_num, schedulecost)
# print(random_input)
# print_schedule(random_input)
# print(best_cost)
# print('###########################################################################################')
#
# vec_input = annealing_optimize(random_num, schedulecost)
# print(vec_input)
# print_schedule(vec_input)
# print('###########################################################################################')
#
# vec_input_2 = genetic_optimize(random_num, schedulecost)
# print(vec_input_2)
# print_schedule(vec_input_2)

import xml.dom.minidom


dom = xml.dom.minidom.parseString('<data><rec>hello!</rec></data>')
print(dom)
print(dom.getElementsByTagName('rec')[0].firstChild.data)


# r = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
#
# print_schedule(r)
# total_price = schedulecost(r)
# print(total_price)
# print(schedulecost(r))
# for key in flight:
#     print('%s:%s' %(key,flight[key]))
#     print('\n')

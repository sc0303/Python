# Write by SunChuan on 20160629
import re


def get_words(doc):
    splitter = re.compile('\W+')
    words = [s.lower() for s in splitter.split(doc.strip()) if len(s) > 2 and len(s) < 20]
    print(dict([(w, 1) for w in words]))
    return dict([(w, 1) for w in words])


class Classifier:
    def __init__(self, get_feature, file_name=None):
        # 统计特征/分类组合数量
        self.fc = {}
        # 统计每个分类中的文档数量
        self.cc = {}
        self.get_feature = get_feature

    # 增加对特征统计
    def inc_fc(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    # 增加对某一分类的计数值
    def in_cc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    # 某一特征出现在某一分类的次数
    def f_count(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # 属于某一分类项的内容项数量
    def cat_count(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0

    # 所有内容项的数量
    def total_count(self):
        return sum(self.cc.values())

    # 所有分类的列表
    def categories(self):
        return self.cc.keys()

    # 对数据进行训练
    def training(self, item, cat):
        features = self.get_feature(item)
        for i in features:
            self.inc_fc(i, cat)
        # print(self.fc)

        self.in_cc(cat)
        # print(self.cc)
    def f_prob(self,f,cat):
        if self.cat_count(cat)==0:return 0
        return self.f_count(f,cat)/self.cat_count(cat)


    def sample_train(self,input):
        cl.training('Nobody owns the water.','good')
        cl.training('the quick rabbit jumps fences','good')
        cl.training('buy pharmaceuticals now','bad')
        cl.training('make quick money at the online casino','bad')
        cl.training('the quick brown fox jumps','good')

    def weight_prob(self, f, cat, prf, weight = 1.0, ap = 0.5):
        basic_prob = prf(f, cat)
        totals = sum([self.f_count(f, c) for c in self.categories()])
        bp = ((weight*ap + totals*basic_prob))/(weight+totals)
        return bp





cl = Classifier(get_words)
cl.sample_train(cl)
# print(cl.cc)
# print(cl.fc)
# print(cl.f_prob('the', 'good'))
# print(cl.weight_prob('money', 'good', cl.f_prob))

# cl.training('make quick money at the online casino', 'bad')
# cl.training('the quick brown fox jumps', 'good')
# print(cl.f_count('make', 'good'))
# print(cl.f_count('make', 'bad'))

# dict_test = {}
# dict_test.setdefault('quick', {})
# print(dict_test)
# dict_test['quick'].setdefault('bad', 0)
# dict_test['quick'].setdefault('good', 0)
# print(dict_test)
# dict_test['quick']['bad'].setdefault('bad', 0)
# print(dict_test)
# dict_test['quick']['bad'].setdefault('bad',0)
# print(dict_test)

import pypinyin as pypinyin
import re
import math
def pinyin_2_hanzi(pinyinList):
    from Pinyin2Hanzi import DefaultDagParams
    from Pinyin2Hanzi import dag

    dagParams = DefaultDagParams()
    # 10个候选值
    result = dag(dagParams, pinyinList, path_num=10, log=True)
    for item in result:
        socre = item.score # 得分
        res = item.path # 转换结果
        print(socre, res)

class HMM():
    def __init__(self):
        self.init_pro = {}  # 初始概率
        self.emis_pro = {}  # 发射概率
        self.trans_pro = {}  # 转移概率
        self.data=[]
        self.word={}
        self.double_word={}
        self.py_chinese_dict={}
    def word_to_pinyin(self, s):
        py = pypinyin.lazy_pinyin(s)
        return py

    def input_data(self):
        with open("C:\\Users\\陈\\OneDrive\\桌面\\news_sohusite_xml.smarty.dat", encoding='ANSI') as f:
            for line in f.readlines():
                temp = re.findall('[\u4e00-\u9fa5]+', line)
                if temp != []:
                    self.data.append(temp)

    def train_pro(self):
        all=0
        for words in self.data:
            pre=' '
            for i in words:
                for j in i:
                    all+=1
                    if j not in self.word:
                        self.word[j]=1
                    else:
                        self.word[j]+=1
                    if pre != ' ':
                        if pre+j not in self.double_word:
                            self.double_word[pre+j]=1
                        else:
                            self.double_word[pre+j]+=1
                    pre=j

        for i in self.word.keys():
            self.init_pro[i]=math.log(self.word[i]/all)

        #'深': -7.368497402580141,

        for i in self.double_word.keys():
            self.trans_pro[i]=math.log(self.double_word[i]/self.word[i[0]])
        #词语:概率

    def train_emis(self):
        for words in self.data:
            for i in words:
                for j in i:
                    py_j=self.word_to_pinyin(j)
                    py_j=py_j[0]
                    if py_j not in self.py_chinese_dict:
                        self.py_chinese_dict[py_j]=j
                    else:
                        if j not in self.py_chinese_dict[py_j]:
                            self.py_chinese_dict[py_j]+=j
                    if py_j not in self.emis_pro:
                        self.emis_pro[py_j]={}
                        self.emis_pro[py_j][j]=1
                    else:
                        if j not in self.emis_pro[py_j]:
                            self.emis_pro[py_j][j]=1
                        else:
                            self.emis_pro[py_j][j]+=1
        for i in self.emis_pro:
            s=sum(self.emis_pro[i].values())
            for j in self.emis_pro[i]:
                self.emis_pro[i][j]=math.log(self.emis_pro[i][j]/s)
        '''ce': {'侧': -2.8824035882469876, '策': -1.1394342831883648, '测': -0.9996723408132061, '厕': -1.8838747581358606,
               '册': -2.2633643798407643},'''


    def viterbi(self,pinyin_list, n):
        length = len(pinyin_list)
        delta = [[0 for i in range(n)] for j in range(length)]
        path_record = [[0 for i in range(n)] for j in range(length)]
        first_word = self.py_chinese_dict[pinyin_list[0]]
        max_first=-1000000
        id=0
        for i in range(len(first_word)):
            delta[0][i] = self.init_pro[first_word[i]]
            if self.init_pro[first_word[i]]>max_first:
                max_first=self.init_pro[first_word[i]]
                id=i
        if length==1:
            for i in range(10):
                print(first_word[id+i],self.init_pro[first_word[id+i]])

        for i in range(1, length):
            word = self.py_chinese_dict[pinyin_list[i]]
            for j in range(len(word)):
                max_pro = -100000000
                pre_word = self.py_chinese_dict[pinyin_list[i-1]]
                path = 0
                for k in range(len(pre_word)):
                    double_word = pre_word[k]+word[j]
                    if double_word not in self.trans_pro:
                        pro = -100000
                    else:
                        pro = self.trans_pro[double_word]
                    double_word_value = delta[i-1][k]+pro
                    if double_word_value > max_pro:
                        max_pro = double_word_value
                        path = k

                delta[i][j] = self.emis_pro[pinyin_list[i]][self.py_chinese_dict[pinyin_list[i]][j]] + max_pro
                path_record[i][j] = path
            prob = -10000000
            path_choice = [0 for i in range(length)]
            path_choice[length - 1] = 0
            for i in range(len(self.py_chinese_dict[pinyin_list[length-1]])):
                if prob < delta[length - 1][i]:
                    prob = delta[length - 1][i]
                    path_choice[length - 1] = i
            for t in range(length - 2, -1, -1):
                path_choice[t] = path_record[t + 1][path_choice[t + 1]]
            final_word = ""
            pro_end=0
            for i in range(length):
                final_word += self.py_chinese_dict[pinyin_list[i]][path_choice[i]]
                pro_end+=delta[i][path_choice[i]]
            print(final_word, pro_end)




from pinyincut import *
a=HMM()
a.input_data()
a.train_pro()
a.train_emis()
s=input()
b=pinyincut(s)
b.Tire()
b.consist(b.pycut(s),"",[])
c=b.cut
for i in c:
    a.viterbi(i,100)



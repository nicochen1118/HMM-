from copy import deepcopy
class pinyincut():
    def __init__(self,string):
        self.string=string
        # 创建了一个音节字典树，将所有音节加入这个一维列表中
        self.pydict = []
    def Tire(self):
        with open("C:\\Users\陈\\OneDrive\\桌面\\pinyin.txt", "r") as f:
            for line in f.readlines():
                line = line.split()
                for i in line:
                    self.pydict.append(i)
        self.pydict.append(" ")
        self.cut=[]
    def pycut(self,s):
        len_s = len(s)
        start_s=0
        last_s = 0
        new_str=[]
        while start_s<=(len_s):
            while last_s<=len_s:
                if s[start_s:last_s] in self.pydict:
                     char=s[start_s:last_s]
                     last_s+=1
                     new_str.append(char)
                else:
                     last_s+=1
            start_s+=1
            last_s=deepcopy(start_s)
        return new_str
    #这里递归还需要剪枝
    def consist(self,new_str,piece,lis):
        if piece not in self.string:
            return
        if piece==self.string:
            x=deepcopy(lis)
            self.cut.append(x)
            return
        if len(piece)>len(self.string):
            return

        else:
            for i in new_str:
                lis.append(i)
                self.consist(new_str,piece+i,lis)
                lis.remove(i)





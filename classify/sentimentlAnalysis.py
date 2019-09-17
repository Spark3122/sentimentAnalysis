#encoding=utf-8
# coding: utf-8

# In[21]:

import pickle
import re
import jieba


# In[5]:
CUR = "/data/AI/python/"

model = pickle.load(open(CUR+'model0307','rb'))
# model


# In[22]:

stopwordset = set()
with open(CUR+'jieba_dict/stopwords.txt','r',encoding = 'utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))
        
def seg_sent(art):
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'  
    art = art.strip()
    art = re.sub(r, '', art)
    l = []
    seg_list = list(jieba.cut(art, cut_all = False))
    for word in seg_list:
        if word not in stopwordset and word != ' ' and word != "\n" and word != "\n\n":
            l.append(word)
    corpus = " ".join(l)
    return corpus


# In[39]:

def predictForFile(article,output):
    # file = open(fileIn,"r",encoding = 'utf-8')
    
    # article = file.read()
    
    cp = seg_sent(article)
    
    result = model.predict([cp])
    # output = open(fileOut,'w')
    if result == 0:
        # print ("负面新闻###")
        output.write("###SA###负面新闻 ")
    else:
        # print("正面新闻### ")
        output.write("###SA###正面新闻 ")
    print('neg:\t\t','pos:')
    rate = model.predict_proba([cp])
    print(rate)
    output.write("负面值："+str(rate[0][0])+" 正面值："+str(rate[0][1]))

        
def predictForConttent(content):
    cp = seg_sent(content)
    result = model.predict([cp])
#     output = open('file_sa.txt','w')
    rate = model.predict_proba([cp])
    print(rate)
   
#     output.write("负面值2："+str(rate[0][0])+" 正面值2： "+str(rate[0][1]))
    return rate

def main(title):
    file = open(title,"r",encoding = 'utf-8')
    
    article = file.read()
    
    cp = seg_sent(article)
    
    result = model.predict([cp])
    output = open(CUR+'file_sa.txt','w')
    if result == 0:
        print ("这是一篇负面新闻")
        output.write("这是一篇负面新闻")
    else:
        print("这是一篇正面新闻")
        output.write("这是一篇正面新闻")
    print('负面值:\t\t','正面值:')
    rate = model.predict_proba([cp])
    print(rate)
    output.write("负面值："+str(rate[0][0])+" 正面值： "+str(rate[0][1]))


# In[ ]:

# if __name__ == "__main__":
#     import sys
#     import tkinter as tk
#     from tkinter import filedialog

#     root = tk.Tk()
#     root.withdraw()

#     file_path = filedialog.askopenfilename()
#     print(file_path)
#     main(file_path)


# file = open("/Users/daichanglin/Desktop/igoldenbeta/robotSVN/robot/robot-parent/python/sa/test/p1",
#             "r",encoding = 'utf-8')
# article = file.read()
# predictForConttent(article)

# file = open("/Users/daichanglin/Desktop/igoldenbeta/robotSVN/robot/robot-parent/python/sa/test/p2",
#             "r",encoding = 'utf-8')
# article = file.read()
# predictForConttent(article)

# # file = open("/Users/daichanglin/Desktop/igoldenbeta/robotSVN/robot/robot-parent/python/sa/test/rp3",
# #             "r",encoding = 'utf-8')
# # article = file.read()
# # predictForConttent(article)


# file = open("/Users/daichanglin/Desktop/igoldenbeta/robotSVN/robot/robot-parent/python/sa/test/rp1",
#             "r",encoding = 'utf-8')
# article = file.read()
# predictForConttent(article)

# file = open("/Users/daichanglin/Desktop/igoldenbeta/robotSVN/robot/robot-parent/python/sa/test/rp2",
#             "r",encoding = 'utf-8')
# article = file.read()
# predictForConttent(article)

# file = open("/Users/daichanglin/Desktop/igoldenbeta/robotSVN/robot/robot-parent/python/sa/test/rp3",
#             "r",encoding = 'utf-8')
# article = file.read()
# predictForConttent(article)

# file = open("/Users/daichanglin/Desktop/igoldenbeta/robotSVN/robot/robot-parent/python/sa/test/rp4",
#             "r",encoding = 'utf-8')
# article = file.read()
# predictForConttent(article)

# In[ ]:




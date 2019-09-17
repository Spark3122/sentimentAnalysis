
# coding: utf-8

# In[ ]:


#!/usr/bin/python3

import sys
import pickle
import re
import jieba
import sentimentlAnalysis


try:
    
    print(sys.getdefaultencoding() ) 
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    # sys.setdefaultencoding('utf8')  
except e:
	print(e)
    # pass

import pymysql
import time  

HOST = "10.31.90.118"
UNAME ="root"
PW = "!2D#34S3aA$"
DB ="research"
CHARSET = "utf8"

def reCalWroongRpScore(sql,param):  
    # print(len(neg_text.items()))
    # # 打开数据库连接
#     db = pymysql.connect("10.31.90.118","root","!2D#34S3aA$","research" ,charset='utf8')
    db = pymysql.connect(HOST,UNAME,PW,DB ,charset=CHARSET)

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

  
    update_values=[] 
    new_pos_text={}
    try:
       # 执行SQL语句
       cursor.execute(sql,param)
       # 获取所有记录列表
       results = cursor.fetchall()
       print(len(results))
       for row in results:
          title = row[0]
          url = row[1]
          positive_value = row[2]
          source_content = row[3]
          code = row[4]
          source_type = row[5]
          source_id = row[6]
          investment_advice = row[7]

          rate = sentimentlAnalysis.predictForConttent(source_content)
          new_positive_value = positive_value
          if(len(rate)>0 and len(rate[0])>1):
              new_positive_value = int(rate[0][1]*100)
              update_values.append((int(new_positive_value),int(source_type),int(source_id)))
    #           cursor.execute(updatesql,update_param)
#           print(positive_value,code,source_type,source_id,title,investment_advice,source_id,url,new_positive_value)

          new_pos_text[title]=source_content
            # 打印结果
    #       print ("title=%s,url=%s" %(title, url))
          #  # 打印结果
          # print ("title=%s,url=%s,positive_value%s" % \
          #        (title, url, positive_value))
    except e:
       print ("Error: unable to fetch data"+e)




    # 批量插入
    now=time.strftime("%M:%S")
    print(update_values[0])
    updatesql = "update t_stock_researchreport set positive_value = %s  WHERE  source_type = %s and source_id = %s " 
    try:
        cursor.executemany(updatesql , update_values)
        db.commit()
    except Exception as err:
        print(err.message)
    # finally:
    #     cursor.close()
    #     db.close()
    end=time.strftime("%M:%S")
    print(now+","+end)

    # 关闭数据库连接
    cursor.close()
    db.close()
    print(len(new_pos_text))

    

#重新纠正计算错误的分值（循环遍历）
# SQL 查询语句
a = '%买入%'
b = '%增持%'
print(a)
print(b)
sql = "SELECT title, url,positive_value_original,r.source_content,r.`code`,r.source_type,r.source_id ,r.investment_advice FROM t_stock_researchreport r WHERE (investment_advice LIKE %s OR investment_advice LIKE %s) AND positive_value_original < 50 "
param=(a.encode('utf8'),b.encode('utf8'))
reCalWroongRpScore(sql,param)

# # AND positive_value < 40
# # sql = "SELECT title, url,positive_value FROM research.t_stock_researchreport limit "
# # sql = "SELECT title, url,positive_value_original,r.source_content,r.`code`,r.source_type,r.source_id ,r.investment_advice FROM research.t_stock_researchreport r WHERE (investment_advice LIKE %s OR investment_advice LIKE %s) and  investment_advice not LIKE %s AND positive_value_original < 50 "
# #     sql = "SELECT title, url,positive_value_original,r.source_content,r.`code`,r.source_type,r.source_id ,r.investment_advice FROM research.t_stock_researchreport r WHERE (investment_advice LIKE %s OR investment_advice LIKE %s) AND positive_value_original < 50 "
# #     # param=(a.decode("gbk").encode("utf-8"),b.decode("gbk").encode("utf-8")) ,c.encode('utf8')




# #增量重新计算研报舆情分值
# sql = "SELECT title, url,positive_value_original,r.source_content,\
# r.`code`,r.source_type,r.source_id ,r.investment_advice\
# ,r.create_time,r.time,r.update_time,positive_value\
#  FROM t_stock_researchreport r \
# where r.time>'2017-12-30' ORDER BY r.time  desc"
# reCalWroongRpScore(sql,None)




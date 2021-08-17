import pymysql

conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='123456',db='scrapydb',charset='utf8')
cursor = conn.cursor()
try:
  sql = f'insert into qiubai (author,content) values (123,'')'
  cursor.execute('insert into qiubai (author,content) values ("133","wc")')
  conn.commit()
except Exception as e:
  print(e)
  conn.rollback()
  
cursor.close()
conn.close()
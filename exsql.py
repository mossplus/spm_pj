import pymysql
 
 
def execute_fromfile(filename, cursor): 
    fd = open(filename, 'r', encoding='utf-8')
    sqlfile = fd.read()
    fd.close()
    sqlcommamds = sqlfile.split(';')
 
    for command in sqlcommamds:
        if command.strip() != '':
            try:
                cursor.execute(command)
                print("运行成功")
            except Exception as msg:
                print("错误信息： ", msg)
                print(command)
 
    print('sql执行完成')
 
 
def connect_mysql():
    conn = pymysql.connect(host='db', port=3306, user='root', password='moss123', db='seat')
    print("连接数据库成功")
    cursor = conn.cursor()
    execute_fromfile('data_init.sql', cursor)
    conn.close()
 
 
if __name__ == '__main__':
    connect_mysql()

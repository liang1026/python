#!/usr/bin/env python
# coding:utf-8

"""1. 做一个简单的基于文本文件的学员管理系统，可以实现增删改查，文本文件格式：
编号   姓名    性别  年龄   所在地    qq号
增： 运行程序等待用户输入，用户输入“add”，让用户输入姓名，性别，年龄，所在地，qq号这些信息。
查： 运行程序等待用户输入，用户输入”read”, 让用户输入学员编号，查到之后输出给用户。
删：运行程序等待用户输入，用户输入”delete”, 让用户输入学员编号，查到之后输入给用户，然后输出是否删除的确认命令，确认后删除。
改： 运行程序等待用户输入，用户输入”update”, 让用户输入学员编号，进而输出学员信息，之后让用户填入新的内容（所有字段）
提示：可以把文件转换成Python中的结构"""


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import readline
import MySQLdb
from pylsy import pylsytable

content = MySQLdb.connect(
    host = '192.168.8.219',
    port = 3306,
    user = 'jl',
    passwd = '1',
    db = 'stu_info',
    charset = 'utf8')

cur = content.cursor()
c_db = "create database stu_info"
c_table = "CREATE TABLE user_info (id int(8) NOT NULL AUTO_INCREMENT,name char(80) NOT NULL,sexy char(20) NOT NULL,age int(30) NOT NULL,address char(90) NOT NULL,qq int(60) NOT NULL, PRIMARY KEY (id))ENGINE=MyISAM AUTO_INCREMENT=58 DEFAULT CHARSET=utf8"

try:
    cur.execute(c_db)
    cur.execute(c_table)
except Exception as e:
    print e

data_title = ['id','name','sexy','age','address','qq'] 
table = pylsytable(data_title)
id_list = []
name_list = []
sexy_list = []
age_list = []
addr_list = []
qq_list = []

        
def add_table():
    table.add_data('id', id_list)
    table.add_data('name', name_list)
    table.add_data('sexy', sexy_list)
    table.add_data('age', age_list)
    table.add_data('address', addr_list)
    table.add_data('qq', qq_list)
    print table


def clear_list():
    del id_list[:]
    del name_list[:]
    del sexy_list[:]
    del age_list[:]
    del addr_list[:]
    del qq_list[:]


def add_data():
    try:
        name = str(raw_input('姓名: '))
        sexy = str(raw_input('性别: '))
        age =  int(raw_input('年龄: '))
        addr = str(raw_input('地址: '))
        qq = str(raw_input('QQ: '))
    except TypeError as  e:
        print 'TypeError'
    sql = "insert into user_info  (name,sexy,age,address,qq) values (%s,%s,%s,%s,%s) " 
    data = name,sexy,age,addr,qq
    cur.execute(sql, data)
    cur.execute("select * from user_info where name =  '%s' "  % name )
    data_info =cur.fetchall()
    for data in data_info:
        id_list.append(data[0])
        name_list.append(name)
        sexy_list.append(sexy)
        age_list.append(age)
        addr_list.append(addr)
        qq_list.append(qq)
    add_table()
    

def read_data():
    stu_id = raw_input('请输入学员编号(数字)：')
    if stu_id == 'all':
        read_all()
    cur.execute("select * from user_info where id =  '%s' "  %  stu_id)
    data_info =cur.fetchall()
    for data in data_info:
        id_list.append(data[0])
        name_list.append(data[1])
        sexy_list.append(data[2])
        age_list.append(data[3])
        addr_list.append(data[4])
        qq_list .append(data[5])
    add_table() 


def del_data():
    stu_id = raw_input('请输入学员编号(数字)：')
    if stu_id == 'all':
        cur.execute("delete from user_info") 
    cur.execute("select * from user_info where id = '%s' "  %  stu_id)
    yesno = raw_input('确认是否删除？确认请输入：y，不删除请输入：n  :')
    if yesno == 'y':
        cur.execute("delete from user_info where id =  '%s' "  %  stu_id)
        print '编号为%s的学生已经删除成功~' % stu_id
    clear_list()
    cur.execute("select * from user_info ")
    data_info =cur.fetchall()
    for data in data_info:
        id_list.append(data[0])
        name_list.append(data[1])
        sexy_list.append(data[2])
        age_list.append(data[3])
        addr_list.append(data[4])
        qq_list .append(data[5])
    add_table() 


def update_data():
    stu_id = raw_input('请输入学员编号(数字)：')
    cur.execute("select * from user_info where id =  '%s' "  %  stu_id)
    data_info =cur.fetchall()
    for data in data_info:
        id_list.append(data[0])
        name_list.append(data[1])
        sexy_list.append(data[2])
        age_list.append(data[3])
        addr_list.append(data[4])
        qq_list .append(data[5])
    add_table() 
    clear_list()
    name = str(raw_input('姓名: '))
    sexy = str(raw_input('性别: '))
    age =  int(raw_input('年龄: '))
    addr = str(raw_input('地址: '))
    qq = str(raw_input('QQ: '))
    cur.execute(" update stu_info.user_info set name='%s',sexy='%s',age='%s',address='%s',qq='%s' where id = %s "  % (name,sexy,age,addr,qq,stu_id))
    content.commit()
    clear_list()
    cur.execute ("select * from user_info where id = '%s'"   %  stu_id )
    u_info =cur.fetchall()
    for u in u_info:
        id_list.append(u[0])
        name_list.append(u[1])
        sexy_list.append(u[2])
        age_list.append(u[3])
        addr_list.append(u[4])
        qq_list .append(u[5])
    add_table()


def  read_all():
    cur.execute("select * from user_info  order by id")
    data_info =cur.fetchall()
    for data in data_info:
        id_list.append(data[0])
        name_list.append(data[1])
        sexy_list.append(data[2])
        age_list.append(data[3])
        addr_list.append(data[4])
        qq_list .append(data[5])
    add_table() 
   

while True:
    u_input = raw_input('请输入您的选择--|add|read|delete|update|all|:')
    if u_input == 'add':
        clear_list()
        add_data()
    elif u_input == 'read':
        clear_list()
        read_data()
    elif u_input == 'delete':
        clear_list()
        del_data()
    elif u_input == 'update':
        clear_list()
        update_data()
    elif u_input == 'all':
        clear_list()
        read_all()
    elif u_input == 'exit' or u_input == 'quite':
        print '再见！'
        exit()
    else:
        print '请重新输入！'
        
        

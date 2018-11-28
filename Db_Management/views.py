from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import FileResponse
from django.core.urlresolvers import reverse
import pymysql
from db_test_manage.settings import DATABASES,DATABASES_SLAVE
from django import views
from utils.pageation import page_help
#from Db_Management.setting.config_setting import switch_status
import json
# Create your views here.
import os
from pathlib import Path

# 查询从库
# def query_mysql(sql):
#     src_host=DATABASES_SLAVE['default']['HOST']
#     src_user=DATABASES_SLAVE['default']['USER']
#     src_pwd=DATABASES_SLAVE['default']['PASSWORD']
#     src_dbname=DATABASES_SLAVE['default']['NAME']
#     sql_info={'host':src_host,'user':src_user,'password':src_pwd,'db':src_dbname,'port':3306,'charset':'utf8'}
#     conn=pymysql.connect(**sql_info)
#     cur=conn.cursor(cursor=pymysql.cursors.DictCursor)
#     cur.execute(sql)
#     res=cur.fetchall()
#     cur.close()
#     conn.close()
#     return res

def query_mysql(sql):
    src_host=DATABASES['default']['HOST']
    src_user=DATABASES['default']['USER']
    src_pwd=DATABASES['default']['PASSWORD']
    src_dbname=DATABASES['default']['NAME']
    sql_info={'host':src_host,'user':src_user,'password':src_pwd,'db':src_dbname,'port':3306,'charset':'utf8'}
    conn=pymysql.connect(**sql_info)
    cur=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res=cur.fetchall()
    cur.close()
    conn.close()
    return res

def update_mysql(sql):
    src_host=DATABASES['default']['HOST']
    src_user=DATABASES['default']['USER']
    src_pwd=DATABASES['default']['PASSWORD']
    src_dbname=DATABASES['default']['NAME']
    sql_info={'host':src_host,'user':src_user,'password':src_pwd,'db':src_dbname,'port':3306,'charset':'utf8'}
    conn=pymysql.connect(**sql_info)
    cur=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def turn_to_index(request):
    if request.method=='GET':
        return redirect(index)


def index(request):
    if request.method=='GET':
        # 获取到当前页码
        current_page = int(request.GET.get('pagenum', 1))
        amount_sql="SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '%s';"%DATABASES['default']['NAME']
        total = query_mysql(amount_sql)
        total=total[0]['COUNT(*)']
        #print(total)
        obj = page_help('/index', current_page, total, 15)
        page = obj.page_str()
        sql="SELECT (@i:=@i+1)AS id, table_name, TABLE_COMMENT FROM information_schema.tables,(select @i:=0)as it  WHERE table_schema = '%s' ORDER BY table_name;"%DATABASES['default']['NAME']
        table_comment=query_mysql(sql)
        # print(type(the_id))
        #print(table_comment)
        query_set = table_comment[obj.db_start():obj.db_end()]

        return render(request,'index.html',locals())
    elif request.method=='POST':
        table_name=request.POST.get('table_name',default='')
        comments=request.POST.get('comments',default='')
        sql = "SELECT (@i:=@i+1)AS id, table_name, TABLE_COMMENT FROM information_schema.tables,(select @i:=0)as it  WHERE TABLE_SCHEMA='%s' AND TABLE_NAME LIKE '%%%s%%' AND TABLE_COMMENT LIKE '%%%s%%' ORDER BY table_name;" % (DATABASES['default']['NAME'],table_name, comments)
        print(sql)
        query_set = query_mysql(sql)

        return render(request,'index.html',locals())
# def table_search(request):
#     if request.method=='POST':
#         table_name=request.POST.get('table_name',default='')
#         comments=request.POST.get('comments',default='')
#
#         sql="SELECT (@i:=@i+1)AS id, table_name, TABLE_COMMENT FROM information_schema.tables,(select @i:=0)as it  WHERE TABLE_SCHEMA='clear_vphotos' AND TABLE_NAME LIKE '%%%s%%' AND TABLE_COMMENT LIKE '%%%s%%'"%(table_name,comments)
#         print(sql)
#         resp=query_mysql(sql)
#         print(resp)
#         return HttpResponse(json.dumps(resp),content_type="application/json")


def table_comment_edit(request):
    if request.method=='POST':
        try:
            change_data=request.POST.get('col_info')
            table_name=request.POST.get('table_name')
            table_comment=request.POST.get('table_info')

            print('data:',change_data)
            change_data=eval(change_data)

            sql = """SELECT     
            concat(    
                'ALTER TABLE %s'   ,  
                ' modify column ', COLUMN_NAME, ' ', COLUMN_TYPE, ' ',
                if(is_nullable = 'YES', ' ', 'not null '),     
                if(column_default IS NULL, '',     
                    if(    
                        data_type IN ('char', 'varchar')     
                        OR     
                        data_type IN ('date', 'datetime', 'timestamp') AND column_default != 'CURRENT_TIMESTAMP',     
                        concat(' default ''', column_default,''''),     
                        concat(' default ', column_default)    
                    )    
                ),     
                if(extra is null or extra='','',concat(' ',extra)),  
                ' comment ''%%s'';'    
            ) info
            FROM information_schema.columns    
            WHERE table_schema = '%s' AND table_name = '%s';""" % (table_name,DATABASES['default']['NAME'],table_name)


            sql1='''alter table %s comment '%s'; '''%(table_name,table_comment)

            update_mysql(sql1)

            col_ddl_info = query_mysql(sql)
            for index,i in enumerate(col_ddl_info):

                single_ddl=i['info']
                col_comment=change_data[str(index)][0]
                col_comment_sql=single_ddl%(col_comment)

                print(index, single_ddl)
                print(col_comment_sql)
                if col_comment !='':
                    update_mysql(col_comment_sql)
        except Exception as e:
            return HttpResponse('error')
        return HttpResponse('success')




    if request.method=='GET':
        table_name=request.GET.get('table_name')
        print(table_name)
        table_comment_sql="SELECT TABLE_COMMENT FROM information_schema.TABLES WHERE table_schema='%s' AND TABLE_NAME='%s';"%(DATABASES['default']['NAME'],table_name)
        title_table_comment=query_mysql(table_comment_sql)[0]['TABLE_COMMENT']
        print(title_table_comment)

        sql = "SELECT (@i:=@i+1)AS id,COLUMN_NAME,DATA_TYPE,COLUMN_DEFAULT,is_nullable,COLUMN_COMMENT from information_schema.COLUMNS,(select @i:=0)as it where table_schema = '%s' AND TABLE_NAME='%s'"%(DATABASES['default']['NAME'],table_name)
        table_comment = query_mysql(sql)
        query_set=table_comment
        #print(query_set)
        # switch=switch_status
        # if switch_status=='False':
        #     switch_flag=False
        # else:
        #     switch_flag=True
        # print(switch)
        return render(request,'table_commtent_edit.html',locals())

#
# def switch(requset):
#     if requset.method=='POST':
#         if switch_status=='False':
#             with open('Db_Management/setting/config_setting.py','w')as f:
#                 f.write('switch_status=\'True\'')
#             return HttpResponse('%s'%switch_status)
#         elif switch_status == 'True':
#             with open('Db_Management/setting/config_setting.py', 'w')as f:
#                 f.write('switch_status=\'False\'')
#             return HttpResponse('%s'%switch_status)


def download_excel(request):
    if request.method=='GET':
        table_name=request.GET.get('table_name')
        path = 'C:\download_excel\%s.xls' % table_name
        if os.access(path, os.F_OK):
            os.remove(path)
        os.system(r'''mysql -h 10.3.141.11 -uvphotos -ppaineRu1 -P 3306 -D vphotos -e "SELECT b.TABLE_NAME AS '表名', a.COLUMN_NAME AS '字段名', a.COLUMN_TYPE AS '类型', a.COLUMN_DEFAULT AS '默认值', a.IS_NULLABLE AS '是否允许非空', a.CHARACTER_SET_NAME AS '表字符集', a.COLLATION_NAME AS '校验字符集', a.COLUMN_COMMENT AS '列备注' , b.TABLE_COMMENT AS '表备注', b.`ENGINE` AS '引擎' FROM information_schema.`COLUMNS` AS a,information_schema.`TABLES`AS b WHERE a.TABLE_NAME=b.TABLE_NAME AND a.TABLE_SCHEMA='vphotos' AND b.TABLE_SCHEMA='vphotos' AND b.TABLE_NAME ='%s';"  > C:\download_excel\%s.xls'''%(table_name,table_name))

        file=open(path,'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s.xls"'%table_name
        return response


def test(request):
    if request.method=='GET':
        file = open(r'C:\BaiduNetdiskDownload\114124 MySQL5.7从入门到精通.pdf', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="114124_MySQL5.7从入门到精通.pdf"'
        return response
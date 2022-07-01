import pymysql
from MyTools import settings
from os import listdir
import re
from lxml import etree


# 递归地搜索所有文件
def search_file(file_list, path, file=''):
    path = path + '/' + file
    try:
        dir_list = listdir(path)
    except OSError:
        file_storage = path
        try:
            # 加入列表
            file_list.append(file_storage[len(settings.MEDIA_ROOT+"upload_files/"):])
        except:
            pass
        return

    for file in dir_list:
        # 递归
        search_file(file_list, path, file)


def get_extra_file():
    database_info = ['127.0.0.1', 'root', 'GuoHT990520#2', 'ToolsBoxPi']  # ip、用户名、密码、数据库名
    try:
        # 链接数据库， 创建游标
        conn = pymysql.connect(database_info[0], database_info[1], database_info[2], database_info[3])
        cur = conn.cursor()
        print("数据库链接成功！")
    except Exception as e:
        print("数据库连接失败: ", e)
        return -1

    sql_file = "select tool_file, tool_icon, tool_describe from tool_info;"
    try:
        cur.execute(sql_file)
        info_list = cur.fetchall()
        file_db = [tool[0] for tool in info_list]
        icon_db = [tool[1] for tool in info_list]
        describe_db = [tool[2] for tool in info_list]
    except Exception as e:
        print("查询失败：", e)
        return -1
    file_dir = listdir(settings.MEDIA_ROOT + "Files")
    icon_dir = listdir(settings.MEDIA_ROOT + "Icons")
    img_admin_list = []
    search_file(img_admin_list, settings.MEDIA_ROOT+ 'upload_files')
    # print(img_admin_list)
    img_dir = listdir(settings.MEDIA_ROOT + "ckeditor") + img_admin_list

    unused_file = []
    unused_icon = []
    unused_img = []    

    # print("================多余的 文件包====================")
    for file in file_dir:
        if "Files/" + file in file_db:
            pass
        else:
            # print(file)
            unused_file.append(settings.MEDIA_ROOT + "/Files/"+file)
    # print("===============多余的 文件图标===================")
    for icon in icon_dir:
        if "Icons/" + icon in icon_db:
            pass
        else:
            # print(icon)
            unused_icon.append(settings.MEDIA_ROOT + "/Icons/" + icon)
    # print("===============多余的 介绍图片===================")
    img_db_list = []
    for describe in describe_db:
        o_des = etree.HTML(describe)
        o_img = o_des.xpath("//img/@src")
        for img_path in o_img:
            if img_path.find(settings.MEDIA_URL+"ckeditor")!=-1:
                file_name = img_path[23:]
            else:
                file_name = img_path[26:]
            img_db_list.append(file_name)
    # print(img_db_list)
    for img in img_dir:
        if img in img_db_list:
            pass
        else:
            # print(img)
            unused_img.append(settings.MEDIA_ROOT + "/upload_files/" + img)
    return unused_file, unused_icon, unused_img


def show_extra_files(unused_file, unused_icon, unused_img):
    print("================多余的 文件包====================")
    i=0
    for each in sorted(unused_file):
        print(i+1, each)
        i+=1
    print()
    print("===============多余的 文件图标===================")
    i=0
    for each in sorted(unused_icon):
        print(i+1, each)
        i+=1
    print()
    print("===============多余的 介绍图片===================")
    i=0
    for each in sorted(unused_img):
        print(i+1, each)
        i+=1
    print()


def del_file_list(file_list):
    import os
    for each in sorted(file_list):
        try:
            os.remove(each)
        except Exception as e:
            print("删除失败：", e)


def del_extra_file(unused_file, unused_icon, unused_img):
    del_file_list(unused_file)
    del_file_list(unused_icon)    
    del_file_list(unused_img)    


if __name__ == "__main__":
    extra_files = get_extra_file()
    show_extra_files(extra_files[0],extra_files[1],extra_files[2])
    while True:
        finish=0
        judge = input("是否删除以上文件？0：保留   1：删除 :")
        if judge=="1":
            flag=1  # 是否删除
            while True:
                check = input("确定删除？？？操作不可逆！！！Y/n :")
                if check=="" or check=='y' or check=='Y':
                    del_extra_file(extra_files[0],extra_files[1],extra_files[2])
                    finish=1
                    break
                elif check=='n' or check=="N":
                    flag=0
                    break
                else:
                    continue
            if flag==0 or finish==1:
                break
        elif judge=="0":
            break
        else:
            continue
    print("完成！")

# MyTools

## 介绍
工具人的工具箱——一个优质软件共享平台

## 软件架构
- nginx + uwsgi + django + mysql + redis + celery


## 安装教程
1.  安装python3.7
2.  安装django 2.1.15 => pip3 install django==2.1.15
3.  安装jieba分词 => pip3 install jieba
4.  安装django-cors-headers => pip install django-cors-headers
5.  安装ckeditor => pip install django-ckeditor pillow
6.  安装redis => apt install redis-server
7.  安装redis的python操作包 => pip install django-redis==5.0.0 django-redis-sessions==0.6.2
8.  安装Sqlserver 2017
9.  安装sqlserver的django操作包 => pip install django-sqlserver==1.11
10.  安装celery => pip install celery
11.  安装IIS 10（Linux环境下，建议使用nginx + uwsgi进行部署）


## 使用说明
1.  配置部署环境。
2.  运行web服务器（nginx+uwsgi）: nohup uwsgi --ini uwsgi_.ini > log.txt &
3.  若使用celery，在celery所在服务器，进入项目根目录，执行以下命令: nohup celery -A celery_tasks.tasks worker -l info > celery_log.txt &
4.  进入浏览器 http://localhost:port/ 或 http://localhost:port/tools/index 进入主页
5.  http://guohtgo.asuscomm.com:8001/



#### Redis说明

1.  0号库->session信息
2.  1号库->配合celery的消息队列
3.  2号库->禁止访问的ip
4.  3号库->屏蔽关键字


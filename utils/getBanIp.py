import redis


# 建立redis链接
redis_con = redis.StrictRedis(host="localhost",password="guoht990520_2_redis" ,port=6379, db=2)


def get_ban_ip():
    # 获取redis中2号数据库的所有key
    ban_ip = redis_con.keys("*")
    # print(f"共封禁{len(ban_ip)-1}个ip地址\n")

    ip_time = {}

    # 遍历key，取value
    for each in ban_ip:
        each_ip = each.decode()
        ban_time_str = redis_con.get(each_ip).decode()
        ip_time[each_ip] = ban_time_str

    # 按value排序
    ip_time = sorted(ip_time.items(), key=lambda x:x[1])

    ban_all = []
    # 输出
    for each in ip_time:
        this_ban = {"ip": each[0], "time": each[1].split("\t")[0], "loc": each[1].split("\t")[1]}
        ban_all.append(this_ban)
    return ban_all


if __name__ == "__main__":
    ban_ips = get_ban_ip()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"共封禁{len(ban_ips)-1}个ip地址\n")
    for each in ban_ips:
        print("%4s\t%16s\t%s" % (ban_ips.index(each), each[0], each[1]), end="\n")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

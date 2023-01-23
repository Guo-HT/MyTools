import redis
import sys
import datetime
from utils.ip2loc import IpLocQuery

def main(ip_list):
    redis_con = redis.StrictRedis(host="localhost", port=6379, db=2)
    ip_count = len(ip_list)
    print(f"要禁掉{ip_count}个IP")
    for each in ip_list:
        print("要禁掉的ip为：", each, end="\t")
        ip_loc = IpLocQuery(each)
        loc = ip_loc.run()['data']['location']
        if redis_con.set(each, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\t"+loc):
            print(loc, "\tdone.")


if __name__ == "__main__":
    ip_list = sys.argv[1:]
    main(ip_list)

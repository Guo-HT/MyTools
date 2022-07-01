import sys
import redis


def add_ban_word(word):
    con = redis.StrictRedis(host="localhost", port=6379, db=3)
    result = con.set(word, "1")
    return result


if __name__=="__main__":
    argv = sys.argv
    print(f"获取到{len(argv)-1}个关键字参数：")
    for each in argv[1:]:
        result = add_ban_word(each)
        print(f"{each} {result}.")


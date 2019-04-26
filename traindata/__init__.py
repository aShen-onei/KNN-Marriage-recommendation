import requests
import urllib.parse
import urllib.request
import json
import re
import pymysql
import time
import random
import datareptile
# import queue
# import thread




if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "LZ6=0*9RuWKd", "graduateprojecttest")
    page1 = 1
    url = 'http://search.jiayuan.com/v2/search_v2.php?'
    stc = [
        "2:18.24,23:1",
        "2:25.30,23:1",
        "2:31.36,23:1",
        "2:37.42,23:1",
        "2:43.48,23:1",
        "2:49.54,23:1",
        "2:55.60,23:1",
        "2:61,66,23:1",
        "2:67,70,23:1",
    ]
    us = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"]
    for stcdata in stc:
        for page in range(1, 401):
            print("第%d次爬取" % page1)
            headers = {
                # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'user-agent': random.choice(us),
                'Cookie': 'guider_quick_search=on; accessID=20190419093843742969; user_access=1; SESSION_HASH=d2ee85261720e57b4f8941c0d7021e9fa7eac831; myuid=204197176; save_jy_login_name=13516502945; PHPSESSID=56fb82b3bab2fc99c622bd137d4b806a; main_search:205197176=%7C%7C%7C00; is_searchv2=1'
                # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                # 'Cookie':'guider_quick_search=on; accessID=20190419194257823238; _gscu_1380850711=5567487645gqve19; stadate1=204197176; myloc=44%7C4406; myage=21; mysex=m; myuid=204197176; myincome=30; pop_sj=0; SESSION_HASH=dbe74b3f18d23fa62c95b133ad51f7e848fe6737; FROM_BD_WD=%25E4%25B8%2596%25E7%25BA%25AA%25E4%25BD%25B3%25E7%25BC%2598; FROM_ST_ID=1764229; FROM_ST=.jiayuan.com; user_access=1; save_jy_login_name=13516502945; upt=BDHePs4fqzdpo2aPGEZXVOP-Ej7NKvMbTWgpHxeHy8SfhhFMbc-sRUfwlfwExLyoFRj-0X-VFH0LHByFIj45zEA.; user_attr=000000; is_searchv2=1; jy_refer=sp0.baidu.com; COMMON_HASH=1b86e07a17d23836a9aff7c4e2d76b8d; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-04-20; last_login_time=1555748563; PHPSESSID=6eeeca5ac59667f3292bc55eec31ace4; main_search:205197176=%7C%7C%7C00; pop_avatar=1; PROFILE=205197176%3AaShenone%3Am%3Aimages2.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A50%3A10%3A3; RAW_HASH=OypgsBvvpJNuH1-nUETBs-8QMq8dtlnF4tMZVTBfpoorcdIsc1genZgjVuO2KLLkCYLF8xoBxsqP9MzpjDriDBrti0VuStkBfmVYhmF1-Ys1o08.; pop_time=1555748605556'
            }
            formdata = {
                "sex": "f",
                "key": "",
                "stc": stcdata,
                "sn": "default",
                "sv": "1",
                "p": page1,
                "f": "select",
                "listStyle": "bigPhoto",
                "pri_uid": "0",
                "jsversion": "v5"
            }
            # datareptile.main(url, headers, formdata, db)
            page1 = page1 + 1
            if page % 10 == 0:
                time.sleep(3)
    db.close()
    # print(html)
    # parserhtml(html)
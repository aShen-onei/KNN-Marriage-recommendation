# http://search.jiayuan.com/v2/search_v2.php?key=&sex=f&stc=23:1&sn=default&sv=1&f=select
import requests
import json
def fetchUrl(url):
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Cookie':'guider_quick_search=on; accessID=20190419194257823238; _gscu_1380850711=5567487645gqve19; stadate1=204197176; myloc=44%7C4406; myage=21; mysex=m; myuid=204197176; myincome=30; pop_sj=0; SESSION_HASH=dbe74b3f18d23fa62c95b133ad51f7e848fe6737; FROM_BD_WD=%25E4%25B8%2596%25E7%25BA%25AA%25E4%25BD%25B3%25E7%25BC%2598; FROM_ST_ID=1764229; FROM_ST=.jiayuan.com; user_access=1; save_jy_login_name=13516502945; upt=BDHePs4fqzdpo2aPGEZXVOP-Ej7NKvMbTWgpHxeHy8SfhhFMbc-sRUfwlfwExLyoFRj-0X-VFH0LHByFIj45zEA.; user_attr=000000; is_searchv2=1; jy_refer=sp0.baidu.com; COMMON_HASH=1b86e07a17d23836a9aff7c4e2d76b8d; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-04-20; last_login_time=1555748563; PHPSESSID=6eeeca5ac59667f3292bc55eec31ace4; main_search:205197176=%7C%7C%7C00; pop_avatar=1; PROFILE=205197176%3AaShenone%3Am%3Aimages2.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A50%3A10%3A3; RAW_HASH=OypgsBvvpJNuH1-nUETBs-8QMq8dtlnF4tMZVTBfpoorcdIsc1genZgjVuO2KLLkCYLF8xoBxsqP9MzpjDriDBrti0VuStkBfmVYhmF1-Ys1o08.; pop_time=1555748605556'
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'unicode_escape'
        print(r.url)
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")

def parserhtml(html):
    res = json.loads(html)
    femal = []
    for key in res['userInfo']:
        reslist = []
        uid = key['uid']
        nickname = key['nickname']
        sex = key['sex']
        age = key['age ']
        work_location = key['work_location']
        height = key['height']
        education = key['education']
        marriage = key['marriage']
        income = key['income']
        shortnote = key['shortnote']
        image = key['image']
        matchCondition = key['matchCondition']

        reslist.append(uid)
        reslist.append(nickname)
        reslist.append(sex)
        reslist.append(work_location)
        reslist.append(height)
        reslist.append(education)
        reslist.append(marriage)
        reslist.append(income)
        reslist.append(shortnote)
        reslist.append(image)
        reslist.append(matchCondition)

        print(reslist)
        femal.append(reslist)
    print(femal)

if __name__ == '__main__':
    url = 'http://search.jiayuan.com/v2/search_v2.php?key=&sex=f&stc=23:1&sn=default&sv=1&f=select'
    html = fetchUrl(url)
    print(html)
    # parserhtml(html)
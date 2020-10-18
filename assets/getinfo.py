from urllib import error
from urllib import parse
from http import cookiejar
from bs4 import BeautifulSoup
from main import username, password
from random import choice
import urllib.request
import base64
import re
import sys


user_agent = [
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
]
headers = {
    'Host': ' qzjw.xxxedu.edu.cn',
    'Upgrade-Insecure-Requests': ' 1',
    'Origin': 'https://qzjw.xxxedu.edu.cn',
    'Content-Type': ' application/x-www-form-urlencoded',
    'User-Agent': choice(user_agent),
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://qzjw.xxxedu.edu.cn/jsxsd/',
    'Accept-Language': ' zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}


try:
    # 获取信息

    list_info = []  # info列表

    # 登录
    def login():
        LOGIN_URL = "https://qzjw.xxxedu.edu.cn/jsxsd/xk/LoginToXk"

        values = {}

        values['userAccoun'] = username
        values['userPassword'] = ''
        st = base64.b64encode(bytes(username, 'utf8')).decode(
        )+'%%%'+base64.b64encode(bytes(password, 'utf8')).decode()
        values['encoded'] = st

        postdata = parse.urlencode(values).encode('utf-8')
        cookie = cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)

        request = urllib.request.Request(LOGIN_URL, postdata, headers)
        opener.open(request)

        return opener

    def get_soup(url, headers):
        get_request = urllib.request.Request(url, headers=headers)
        get_response = opener.open(get_request)
        soup = BeautifulSoup(get_response.read(), 'html.parser')

        return soup

    def post_soup(url, data, headers):
        get_request = urllib.request.Request(url, data, headers=headers)
        get_response = opener.open(get_request)
        soup = BeautifulSoup(get_response.read(), 'html.parser')

        return soup

    # 获取标签名为a，b属性的内容，存入数组

    def find_tag(soup, a, b):
        list_test = []
        result = soup.find_all(a, b)
        rule = re.compile(r'<[^>]+>', re.S)
        for i in range(len(result)):
            res_k = re.sub(r'\s', '', rule.sub('', str(result[i])))
            if res_k != '':
                list_test.append(res_k)

        return list_test

    # 去除成绩列表中的不需要的数据

    def cjcx_rule(soup, flag=False, kk=False):
        list_test = []
        list_cont = []
        list_out = []
        # 从序号到总成绩的数据
        result = soup.find_all('tr')
        for i in range(len(result)):
            a = result[i].find_all('td')
            rule = re.compile(r'<[^>]+>', re.S)
            for j in range(0, len(a)):
                res_k = re.sub(r'\s', '', rule.sub('', str(a[j].next)))
                if res_k == '':
                    res_k = "null"
                list_test.append(res_k)

        if flag == True:
            if kk ==True:
                list_test[26] = soup.find('input', id='xm')["value"] #26 名字
                list_test[18] = soup.find('input', id='xb')["value"] #18 性别
            list_out = list_test
        else:
            # 成绩查询的数据处理
            for k in range(len(soup.contents)):
                if re.match(r'^<td>', str(soup.contents[k])):
                    res_k = re.sub(r'\s', '', rule.sub(
                        '', str(soup.contents[k])))
                    if res_k == '':
                        res_k = "null"
                    list_cont.append(res_k)
            for i in range(int(len(list_test)/6)):
                for j in range(i*6, i*6+6):
                    list_out.append(list_test[j])
                for k in range(i*12, i*12+12):
                    list_out.append(list_cont[k])
        return list_out

    # 获取GPA

    def getGPA(list_test):
        gpa_dict = {
            'A': 4.00,
            'A-': 3.70,
            'B+': 3.30,
            'B': 3.00,
            'B-': 2.70,
            'C+': 2.30,
            'C': 2.00,
            'C-': 1.70,
            'D+': 1.30,
            'D': 1.00,
            'F': 0,
        }
        xfjd = float()  # 学分*绩点的总和
        qudexfkc = float()  # 取得学分
        allxfkc = float()  # 所有课程学分

        for i in range(6, len(list_test), 18):
            xfjd += gpa_dict[list_test[i]] * float(list_test[i+3])
            allxfkc += float(list_test[i+3])

            if list_test[i+1] == '合格':
                qudexfkc += float(list_test[i+3])

        qudexfGPA = round(xfjd / qudexfkc, 2)
        allxfGPA = round(xfjd / allxfkc, 2)

        return qudexfGPA, allxfGPA

    # 获取当前学期（教室借用记录）

    def get_xueqi():
        soup = get_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/kbxx/jsjy_query', headers)
        xnxqh = soup.find('input', id="xnxqh")["value"]  # 当前学期
        print("当前学期是：", xnxqh, "\n")
        soup = get_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/kbxx/jsjyjl_query', headers)

        list_test = []
        str_test = find_tag(soup, "select", {"id": "xnxqh"})[0]

        for i in range(7, len(str_test)-11, 11):
            list_test.append(str_test[i:i+11])

        last_xnxqh = list_test[list_test.index(xnxqh)+1]  # 上个学期
        return xnxqh, last_xnxqh

    # 基本信息
    def get_base():

        global list_info
        soup = get_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/bygl/bysxx', headers)
        list_test = []
        list_test = cjcx_rule(soup, flag=True, kk=True) 

        for i in (24, 26, 18, 14, 8, 10,):  # 学号、名字、性别、层次、学院、专业
            if i == 24:  # 获取年级
                a = list_test[i][:4]
                list_info.append(a)
                list_info.append(list_test[i])
            elif i == 14:
                list_info.append(list_test[i][2:])
            elif i == 10:
                list_info.append(list_test[i][3:])
            else:
                list_info.append(list_test[i])

        return 0

    # 获取当前学期上课课程及学分(选课结果查询)

    def get_nowcourse(xnxqh):
        global list_info
        values = {}
        now_course = []
        now_course_xf = float()
        values['xnxqid'] = xnxqh
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/xkgl/loadXsxkjgList', postdata, headers)

        list_test = cjcx_rule(soup, flag=True)
        for i in range(0, len(list_test), 11):
            now_course_xf += float(list_test[i+8])
            for j in (i+10, i+2, i+1, i+8):  # 课程性质、编号、名称、学分
                now_course.append(list_test[j])

        list_info.append('{:g}'.format(now_course_xf))
        return now_course

    # 获取上个学期课程及成绩(课程成绩查询)

    def get_lastcourse(last_xnxqh):
        last_course = []
        values = {}
        values['kksj'] = last_xnxqh  # 开课时间
        values['kcxz'] = ''  # 课程性质
        values['kcmc'] = ''  # 课程名称
        values['xsfs'] = 'max'  # 显示方式
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)

        list_test = cjcx_rule(soup)
        for i in range(0, len(list_test), 18):
            for j in (i+16, i+2, i+3, i+6, i+9):  # 课程性质、编号、名称、等级、学分
                last_course.append(list_test[j])

        return last_course

    def get_en_course_num():
        # 获取双语课程en_course_num数目
        values = {}
        values['kksj'] = ''  # 开课时间
        values['kcxz'] = ''  # 课程性质
        values['kcmc'] = '双语'  # 课程名称
        values['xsfs'] = 'max'  # 显示方式
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)

        list_test = cjcx_rule(soup)
        en_course_num = int(len(list_test) / 18)
        return en_course_num

    def get_xfGPA():
        # GPA、专业必修GPA
        values = {}
        list_test = []
        values['kksj'] = ''  # 开课时间
        values['kcxz'] = ''  # 课程性质
        values['kcmc'] = ''  # 课程名称
        values['xsfs'] = 'max'  # 显示方式
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
        list_test = cjcx_rule(soup)
        qudexfGPA, allxfGPA = getGPA(list_test)  # 取得学分GPA,所有课程学分GPA

        values['kcxz'] = '16'     # 专业必修
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
        list_test = cjcx_rule(soup)
        zballGPA = getGPA(list_test)[1]  # 获取专业必修课程zballGPA
        return qudexfGPA, allxfGPA, zballGPA

    # 获取学分情况

    def get_xf():
        global list_info
        values = {}
        values['kksj'] = ''  # 开课时间
        values['kcxz'] = ''  # 课程性质
        values['kcmc'] = '奖励学分'  # 课程名称
        values['xsfs'] = 'max'  # 显示方式
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
        list_tests = cjcx_rule(soup)
        list_test = [list_tests[i:i+18]for i in range(0, len(list_tests), 18)]
        gx_jlxf = cd_jlxf = 0
        for i in range(len(list_test)):
            if '公选' in list_test[i][16]:
                gx_jlxf += float(list_test[i][9])
            elif '创业就业' in list_test[i][16]:
                cd_jlxf += float(list_test[i][9])

        # 学分情况  学习完成情况查看(性质)
        soup = get_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqk_idxOnlb.do', headers)
        ndzydm = soup.find('input', type="hidden")["value"]

        values.clear()
        values['ndzydm'] = ndzydm
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'https://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqkOnkclb.do', postdata, headers)

        list_tests = cjcx_rule(soup, flag=True)[1:33]

        list_test = [list_tests[i:i+4]for i in range(0, len(list_tests), 4)]

        # 公必、公选、专必、专选、实践、创导、课外科技
        qude_allxf = float()
        for i in (1, 2, 5, 6, 4, 0, 3):
            b_test = float(list_test[i][1])  # 该类课程应修学分
            c_test = float(list_test[i][2])  # 该类课程已取得学分

            list_info.append("{:g}".format(b_test))
            if i == 2:
                c_test = float(list_test[i][2]) + gx_jlxf  # 公选课程+奖励学分
            elif i == 0:
                c_test = float(list_test[i][2]) + cd_jlxf  # 创导课程+奖励学分

            qude_allxf += c_test
            list_info.append("{:g}".format(c_test))

            if b_test <= c_test:
                list_info.append('0')
            else:
                list_info.append("{:g}".format(b_test - c_test))  # 该类课程欠修学分

        list_info.append("{:g}".format(qude_allxf))  # 取得总学分
        list_info.append("{:g}".format(float(list_test[7][1])))  # 毕业总学分

        return 0

    # 登录
    values = {}
    opener = login()
    soup = get_soup('https://qzjw.xxxedu.edu.cn/jsxsd/bygl/bysxx', headers)
    if soup.find('title').decode()[10:12] == "信息" and soup.status_code != 404:
        print("\n ", username, "登录成功\n")
    else:
        print("\n学号或密码错误，请稍后重试！\n")
        sys.exit(0)

    xnxqh, last_xnxqh = get_xueqi()
    get_base()
    now_course = get_nowcourse(xnxqh)
    last_course = get_lastcourse(last_xnxqh)
    en_course_num = get_en_course_num()
    qudexfGPA, allxfGPA, zballGPA = get_xfGPA()
    get_xf()

    list_mo_info = [
        list_info[30], list_info[29], '', str(allxfGPA), 'null', str(en_course_num), 'null', str(
            zballGPA), last_xnxqh[:9], last_xnxqh[-1:], '', xnxqh[:9], xnxqh[-1:], '',
        list_info[29], str(qudexfGPA), str(allxfGPA), list_info[7], 'null',
    ]

except Exception as e:
    print("[-] %s" % e)
    sys.exit(0)

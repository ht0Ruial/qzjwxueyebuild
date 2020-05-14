from urllib import error
from urllib import parse
from http import cookiejar
from bs4 import BeautifulSoup
from main import username,password
from random import choice
import urllib.request
import base64
import re
import sys

# 登录
user_agent = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12"
]
headers = {
    'Host': ' qzjw.xxxedu.edu.cn',
    'Upgrade-Insecure-Requests': ' 1',
    'Origin': 'http://qzjw.xxxedu.edu.cn',
    'Content-Type': ' application/x-www-form-urlencoded',
    'User-Agent': choice(user_agent),
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://qzjw.xxxedu.edu.cn/jsxsd/',
    'Accept-Language': ' zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}

LOGIN_URL = 'http://qzjw.xxxedu.edu.cn/jsxsd/xk/LoginToXk'

values = {}
values['userAccoun'] = username
values['userPassword'] = ''
st = base64.b64encode(bytes(username, 'utf8')).decode()+'%%%'+base64.b64encode(bytes(password, 'utf8')).decode()
values['encoded'] = st

postdata = parse.urlencode(values).encode('utf-8')
cookie = cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(LOGIN_URL, postdata, headers)
response = opener.open(request)


try:
    # 获取信息

    list_info = []  # info列表
    list_test = []  # 临时列表


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


    # 去除成绩列表中的成绩标识、补重学期

    def cjcx_rule(list_test):
        for i in range(10, len(list_test), 13):  # 这一行的len(list_test)在for循环运行时会固定初始值，不会动态变化
            if i > len(list_test):  # 防止溢出
                break
            if list_test[i-6] == '2':
                list_test.pop(i-6)
            if list_test[i] != '正常考试' and list_test[i-3] == '补考':
                list_test.pop(i-3)
                list_test.pop(i-1)
            elif list_test[i] != '正常考试' and list_test[i-3] != '补考':
                list_test.pop(i-1)

        return list_test


    # 获取GPA
    def getGPA(list_test):
        gpa_dict = {
            'A': 4.00,
            'A-': 3.70,
            'B+': 3.40,
            'B': 3.00,
            'B-': 2.70,
            'C+': 2.40,
            'C': 2.0,
            'C-': 1.70,
            'D+': 1.40,
            'D': 1.0,
            'F': 0,
        }
        xfjd = float()  # 学分*绩点的总和
        qudexfkc = float()  # 取得学分
        allxfkc = float()  # 所有课程学分

        for i in range(5, len(list_test), 13):
            xfjd += gpa_dict[list_test[i]] * float(list_test[i+2])
            allxfkc += float(list_test[i+2])

            if list_test[i+1] == '合格':
                qudexfkc += float(list_test[i+2])

        qudexfGPA = round(xfjd / qudexfkc, 2)
        allxfGPA = round(xfjd / allxfkc, 2)

        return qudexfGPA, allxfGPA


    # 基本信息
    soup = get_soup('http://qzjw.xxxedu.edu.cn/jsxsd/bygl/bysxx', headers)
    list_test.clear()
    list_test.append(soup.find('input', id='xm')["value"])  # 获取名字
    list_test.extend(find_tag(soup, "td", {"align": "center"}))

    for i in (17, 0, 12, 8, 2, 4,):  # 学号、名字、性别、层次、学院、专业
        if i == 17:  # 获取年级
            a = list_test[i][:4]
            list_info.append(a)
            list_info.append(list_test[i])
        elif i == 8:
            list_info.append(list_test[i][2:])
        elif i == 4:
            list_info.append(list_test[i][3:])
        else:
            list_info.append(list_test[i])

    # 获取当前学期
    soup = get_soup('http://qzjw.xxxedu.edu.cn/jsxsd/kbxx/jsjy_query', headers)
    xnxqh = soup.find('input', id="xnxqh")["value"]  # 当前学期
    soup = get_soup('http://qzjw.xxxedu.edu.cn/jsxsd/kbxx/jsjyjl_query', headers)

    list_test.clear()
    str_test = find_tag(soup, "select", {"id": "xnxqh"})[0]

    for i in range(7, len(str_test)-11, 11):
        list_test.append(str_test[i:i+11])

    last_xnxqh = list_test[list_test.index(xnxqh)+1]  # 上个学期，格式2019-2020-1


    # 学分情况
    soup = get_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqk_idxOnlb.do', headers)
    ndzydm = soup.find('input', type="hidden")["value"]

    values.clear()
    values['ndzydm'] = ndzydm
    postdata = parse.urlencode(values).encode('utf-8')
    soup = post_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqkOnkclb.do', postdata, headers)

    list_test.clear()
    list_test = find_tag(soup, "td", {"align": "center"})
    # 正修读学分
    list_info.append('{:g}'.format(float(list_test[35])))

    # 获取当前学期上课课程
    now_course = []
    list_test = find_tag(soup, "td", '')
    for i in range(len(list_test)):  # 获取修读中的列表下标
        if list_test[i] == '修读中':
            now_course.extend(list_test[i-5:i-1])

    for i in range(3, len(now_course), 4):  # 调整合适位置
        now_course.insert(i-3, now_course[i])
        now_course.pop(i+1)

    # 获取双语课程en_course_num数目
    en_course_num = 0
    for i in range(len(list_test)):  # 获取双语课程的列表下标
        if '双语' in list_test[i] and list_test[i+4] != '修读中':
            en_course_num += 1


    # 获取上个学期课程及成绩
    last_course = []
    values.clear()
    values['kksj'] = last_xnxqh  #开课时间
    values['kcxz'] = ''  # 课程性质
    values['kcmc'] = ''  # 课程名称
    values['xsfs'] = 'max'  # 显示方式
    postdata = parse.urlencode(values).encode('utf-8')
    soup = post_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
    
    list_test.clear()
    list_test = cjcx_rule(find_tag(soup, "td", ''))
    for i in range(10, len(list_test), 13):
        for j in (i+2, i-8, i-7, i-5, i-3):
            last_course.append(list_test[j])

    # 公必01、公选15、专必16、专选05、实践07、创导09、课外科技10
    kcxz = ['01', '15', '16', '05', '07', '09', '10']
    xf_num = float()  # 总学分
    for i in kcxz:
        values['kksj'] = ''
        values['kcxz'] = i
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
        list_test.clear()
        list_test = cjcx_rule(find_tag(soup, "td", ''))
        if i == '16':
            zballGPA = getGPA(list_test)[1]  # 获取专业必修课程zballGPA

        k = float()
        for j in range(7, len(list_test), 13):
            if list_test[j-1] == '合格':
                k += float(list_test[j])

        xf_num += k
        list_info.append("{:g}".format(k))
        
    list_info.append("{:g}".format(xf_num))

    # GPA、专业必修GPA
    values['kcxz'] = ''
    postdata = parse.urlencode(values).encode('utf-8')
    soup = post_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
    list_test.clear()
    list_test = cjcx_rule(find_tag(soup, "td", ''))
    qudexfGPA, allxfGPA = getGPA(list_test)  # 取得学分,所有课程学分

    list_mo_info = [
        list_info[15], '', str(allxfGPA), str(en_course_num), '', str(
            zballGPA), last_xnxqh[:9], last_xnxqh[-1:], '', xnxqh[:9], xnxqh[-1:], '',
        list_info[15], str(qudexfGPA), str(allxfGPA), list_info[7], '',
    ]
except :
    print("\nPlease check your studentid or password.\n")
    sys.exit()
    

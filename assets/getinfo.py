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
    'Origin': 'http://qzjw.xxxedu.edu.cn',
    'Content-Type': ' application/x-www-form-urlencoded',
    'User-Agent': choice(user_agent),
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://qzjw.xxxedu.edu.cn/jsxsd/',
    'Accept-Language': ' zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}


try:
# 获取信息

    list_info = []  # info列表
    list_test = []  # 临时列表
    flag = False


    def login():
        LOGIN_URL = "http://qzjw.xxxedu.edu.cn/jsxsd/xk/LoginToXk"

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


    #去除成绩列表中的不需要的数据
    def cjcx_rule(soup):
        list_test = []
        list_cont = []
        list_out = []
        ##从序号到总成绩的数据
        result = soup.find_all('tr')
        for i in range(len(result)):
            a = result[i].find_all('td')
            rule = re.compile(r'<[^>]+>', re.S)
            for j in range(0,len(a)):
                res_k = re.sub(r'\s', '', rule.sub('',str(a[j].next)))
                if res_k == '':
                    res_k = "null"
                list_test.append(res_k)

        if flag == True :
            list_out = list_test
        else :
            ##从成绩等级-课程类别的数据
            for k in range(len(soup.contents)):
                if re.match(r'^<td>',str(soup.contents[k])):
                    res_k = re.sub(r'\s', '', rule.sub('',str(soup.contents[k])))
                    if res_k == '':
                        res_k = "null"
                    list_cont.append(res_k)
            for i in range(int(len(list_test)/6)):
                for j in range(i*6,i*6+6):
                    list_out.append(list_test[j])
                for k in range(i*12,i*12+12):
                    list_out.append(list_cont[k])
        
        return list_out


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

        for i in range(6, len(list_test), 18):
            xfjd += gpa_dict[list_test[i]] * float(list_test[i+3])
            allxfkc += float(list_test[i+3])

            if list_test[i+1] == '合格':
                qudexfkc += float(list_test[i+3])

        qudexfGPA = round(xfjd / qudexfkc, 2)
        allxfGPA = round(xfjd / allxfkc, 2)

        return qudexfGPA, allxfGPA


    # 登录
    opener = login()
    soup = get_soup('http://qzjw.xxxedu.edu.cn/jsxsd/bygl/bysxx',headers)
    if soup.find('title').decode()[10:12] == "信息" and soup.status_code != 404:
        print("\n ",username, "登录成功\n")
    else:
        print("\n学号或密码错误，请稍后重试！")
        print("Please check your studentid or password.\n")
        sys.exit(0)


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
    print("当前学期是：",xnxqh,"\n")
    soup = get_soup('http://qzjw.xxxedu.edu.cn/jsxsd/kbxx/jsjyjl_query', headers)

    list_test.clear()
    str_test = find_tag(soup, "select", {"id": "xnxqh"})[0]

    for i in range(7, len(str_test)-11, 11):
        list_test.append(str_test[i:i+11])

    last_xnxqh = list_test[list_test.index(xnxqh)+1]  # 上个学期


    # 学分情况
    soup = get_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqk_idxOnlb.do', headers)
    ndzydm = soup.find('input', type="hidden")["value"]

    values = {}
    values['ndzydm'] = ndzydm
    postdata = parse.urlencode(values).encode('utf-8')
    soup = post_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqkOnkclb.do', postdata, headers)

    list_test.clear()
    list_test = find_tag(soup, "td", {"align": "center"})
    # 正修读学分
    list_info.append('{:g}'.format(float(list_test[35])))

    # 获取双语课程en_course_num数目
    en_course_num = 0
    for i in range(len(list_test)):  # 获取双语课程的列表下标
        if '双语' in list_test[i] and list_test[i+4] != '修读中':
            en_course_num += 1


    # 获取当前学期上课课程
    flag = True
    values.clear()
    list_test.clear()
    now_course = []
    values['xnxqid'] = xnxqh
    postdata = parse.urlencode(values).encode('utf-8')
    soup = post_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/xkgl/loadXsxkjgList', postdata, headers)

    list_test = cjcx_rule(soup)
    for i in range(0, len(list_test), 11):
        for j in (i+10, i+2, i+1, i+8): #课程性质、编号、名称、学分
            now_course.append(list_test[j])
    flag = False  #flag状态还原



    # 获取上个学期课程及成绩
    last_course = []
    values.clear()
    list_test.clear()

    values['kksj'] = last_xnxqh  #开课时间
    values['kcxz'] = ''  # 课程性质
    values['kcmc'] = ''  # 课程名称
    values['xsfs'] = 'max'  # 显示方式
    postdata = parse.urlencode(values).encode('utf-8')
    soup = post_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)

    list_test = cjcx_rule(soup)
    for i in range(0, len(list_test), 18):
        for j in (i+16, i+2, i+3, i+6, i+9): #课程性质、编号、名称、等级、学分
            last_course.append(list_test[j])

    # 公必01、公选15、专必16、专选05、实践07、创导09、课外科技10
    values.clear()
    kcxz = ['01', '15', '16', '05', '07', '09', '10']
    xf_num = float()  # 总学分
    for i in kcxz:
        values['kksj'] = ''
        values['kcxz'] = i
        postdata = parse.urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
        list_test.clear()
        list_test = cjcx_rule(soup)
        if i == '16':
            zballGPA = getGPA(list_test)[1]  # 获取专业必修课程zballGPA

        k = float()
        for j in range(7, len(list_test), 18):
            if list_test[j] == '合格':
                k += float(list_test[j+2])

        xf_num += k
        list_info.append("{:g}".format(k))
        
    list_info.append("{:g}".format(xf_num))

    # GPA、专业必修GPA
    values['kcxz'] = ''
    postdata = parse.urlencode(values).encode('utf-8')
    soup = post_soup(
        'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
    list_test.clear()
    list_test = cjcx_rule(soup)
    qudexfGPA, allxfGPA = getGPA(list_test)  # 取得学分,所有课程学分

    list_mo_info = [
        list_info[15], '', str(allxfGPA), str(en_course_num), '', str(
            zballGPA), last_xnxqh[:9], last_xnxqh[-1:], '', xnxqh[:9], xnxqh[-1:], '',
        list_info[15], str(qudexfGPA), str(allxfGPA), list_info[7], '',
    ]
    
except Exception as e:
    print("[-] %s" % e)
    sys.exit(0)
    

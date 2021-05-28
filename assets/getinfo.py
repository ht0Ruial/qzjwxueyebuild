import re
import sys
import base64
import requests
from random import choice
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from main import username, password


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
    'Host': 'qzjw.xxxedu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://qzjw.xxxedu.edu.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': choice(user_agent),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://qzjw.xxxedu.edu.cn/jsxsd/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}


try:
    # 获取信息

    list_info = []  # info列表

    s = requests.session()

    # 登录


    def login():
        LOGIN_URL = "http://qzjw.xxxedu.edu.cn/jsxsd/xk/LoginToXk"

        values = {}

        values['userAccoun'] = username
        values['userPassword'] = ''
        st = base64.b64encode(bytes(username, 'utf8')).decode(
        )+'%%%'+base64.b64encode(bytes(password, 'utf8')).decode()
        values['encoded'] = st
        postdata = urlencode(values).encode('utf-8')
        s.post(LOGIN_URL, data=postdata, headers=headers)

        return 0


    def get_soup(url, headers):
        get_response = s.get(url, headers=headers)
        soup = BeautifulSoup(get_response.text, 'html.parser')

        return soup


    def post_soup(url, data, headers):
        get_response = s.post(url, data=data, headers=headers)
        soup = BeautifulSoup(get_response.text, 'html.parser')

        return soup


    # 去除成绩列表中的不需要的数据

    def cjcx_rule(soup, flag=False, kk=False):
        list_test = []
        list_out = []
        # 从序号到总成绩的数据
        result = soup.find_all('td')
        rule = re.compile(r'<[^>]+>', re.S)
        for j in range(0, len(result)):
            res_k = re.sub(r'\s', '', rule.sub('', str(result[j].next)))
            if res_k == '':
                res_k = "null"
            list_test.append(res_k)

        if flag == True:
            if kk == True:
                list_test[26] = soup.find('input', id='xm')["value"]  # 26 名字
                list_test[18] = soup.find('input', id='xb')["value"]  # 18 性别

        return list_test

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

        for i in list_test:
            xfjd += gpa_dict[i[6]] * float(i[2])
            allxfkc += float(i[2])

            if i[7] == '及格':
                qudexfkc += float(i[2])

        qudexfGPA = round(xfjd / qudexfkc, 2)
        allxfGPA = round(xfjd / allxfkc, 2)

        return qudexfGPA, allxfGPA

    # 获取当前学期（选课结果查询）


    def get_xueqi():
        soup = get_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/xkgl/xsxkjgcx', headers)
        demo_res = soup.find_all('option')
        xnxqh = demo_res[2].attrs['value']  # 当前学期
        print("当前学期是：", xnxqh, "\n")

        last_xnxqh = demo_res[3].attrs['value']  # 上个学期
        return xnxqh, last_xnxqh

    # 基本信息


    def get_base():

        global list_info
        soup = get_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/grxx/xsxx', headers)
        list_test = soup.find_all("tr")

        for i in range(6):
            list_info.append(i)

        # 学号、名字、性别、层次、学院、专业
        for i in (2, 3, 8):
            cc = list_test[i].text.split('\n')[1:-1]
            if i == 2:
                list_info[0] = cc[4][3:]  # 学号
                list_info[4] = cc[0][3:]  # 学院
                list_info[5] = cc[1][3:]  # 学院
            elif i == 3:
                list_info[1] = cc[1][1:]
                list_info[2] = cc[3][1:]
            elif i == 8:
                list_info[3] = cc[3][1:]

        return 0

    # 获取当前学期上课课程及学分(选课结果查询)


    def get_nowcourse(xnxqh):
        global list_info
        values = {}
        now_course = []
        now_course_xf = float()
        values['xnxqid'] = xnxqh
        postdata = urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/xkgl/loadXsxkjgList', postdata, headers)

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
        postdata = urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)

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
        postdata = urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)

        list_test = cjcx_rule(soup)
        en_course_num = int(len(list_test) / 18)
        return en_course_num


    def get_xfGPA(remove_course):
        values = {}
        # 学分情况--学习完成情况(性质)
        soup = get_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqk_idxOnlb.do', headers)
        ndzydm = soup.find('input', type="hidden")["value"]

        values['ndzydm'] = ndzydm
        postdata = urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqkOnkclb.do', postdata, headers)
        aa = soup.find_all('table')[2]
        bb = aa.find_all('tr')
        lins = []  # 保存从"学习完成情况(性质)"里获得的课程数据
        for i in range(len(bb)):
            lins_test = []
            cc = bb[i].find_all('td')
            try:
                if cc[0].text.isdigit() and cc[5].text != '待修读' and cc[5].text != '修读中':
                    for j in range(len(cc)-1):  # 减1是因为不要备注的数据
                        lins_test.append(cc[j].text)
                    lins.append(lins_test)
            except:
                pass

        # 移除当前学期正常考试的课程，不算入GPA
        if len(remove_course) != 0:
            for i in remove_course:
                for j in lins:
                    if i[0] == j[1]:  # 课程名称
                        lins.remove(j)
                        break

        qudexfGPA, allxfGPA = getGPA(lins)  # 取得学分GPA,所有课程学分GPA

        # 专业必修
        lins_zb = []
        for i in lins:
            if i[3] == '专业必修课':
                lins_zb.append(i)
        zballGPA = getGPA(lins_zb)[1]  # 获取专业必修课程zballGPA
        return qudexfGPA, allxfGPA, zballGPA

    # 获取学分情况


    def get_xf(remove_course):
        global list_info
        values = {}
        course_value = {
            "创业就业导向课": 0,
            "公共必修课": 1,
            "公共选修课": 2,
            "课外科技学分": 3,
            "实践课": 4,
            "专业必修课": 5,
            "专业选修课": 6,
        }

        # 学分情况--学习完成情况(性质)
        soup = get_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqk_idxOnlb.do', headers)
        ndzydm = soup.find('input', type="hidden")["value"]

        values['ndzydm'] = ndzydm
        postdata = urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/xxwcqk/xxwcqkOnkclb.do', postdata, headers)

        list_tests = cjcx_rule(soup, flag=True)[1:33]

        list_test = [list_tests[i:i+4]for i in range(0, len(list_tests), 4)]

        # 公必、公选、专必、专选、实践、创导、课外科技
        qude_allxf = float()
        for i in (1, 2, 5, 6, 4, 0, 3):
            b_test = float(list_test[i][1])  # 该类课程应修学分
            c_test = float(list_test[i][2])  # 该类课程已取得学分

            list_info.append("{:g}".format(b_test))
            for j in remove_course:
                if i == course_value[j[2]]:  # 课程性质
                    c_test -= j[1]  # 学分

            qude_allxf += c_test
            list_info.append("{:g}".format(c_test))

            if b_test <= c_test:
                list_info.append('0')
            else:
                list_info.append("{:g}".format(b_test - c_test))  # 该类课程欠修学分

        list_info.append("{:g}".format(qude_allxf))  # 取得总学分
        list_info.append("{:g}".format(float(list_test[7][1])))  # 毕业总学分

        return 0

    # 记录当前学期正常考试的课程及学分


    def remove():
        values = {}
        remove_course = []
        values['kksj'] = xnxqh  # 开课时间
        values['kcxz'] = ''  # 课程性质
        values['kcmc'] = ''  # 课程名称
        values['xsfs'] = 'max'  # 显示方式
        postdata = urlencode(values).encode('utf-8')
        soup = post_soup(
            'http://qzjw.xxxedu.edu.cn/jsxsd/kscj/cjcx_list', postdata, headers)
        list_tests = cjcx_rule(soup)
        if list_tests[0] == '未查询到数据':
            return ''
        list_test = [list_tests[i:i+18]for i in range(0, len(list_tests), 18)]
        for i in list_test:
            remove_a = []
            if i[14] == "正常考试":
                remove_a.append(i[3])   # 课程名称
                remove_a.append(float(i[9]))  # 学分
                remove_a.append(i[16])  # 课程性质
                remove_course.append(remove_a)

        return remove_course


    # 登录
    values = {}
    login()
    soup = s.get(
        'http://qzjw.xxxedu.edu.cn/jsxsd/framework/xsMain.jsp', headers=headers)
    if soup.status_code == 200:
        print("\n ", username, "登录成功\n")
    else:
        print("\n学号或密码错误，请稍后重试！\n")
        sys.exit(0)

    xnxqh, last_xnxqh = get_xueqi()
    get_base()
    now_course = get_nowcourse(xnxqh)
    last_course = get_lastcourse(last_xnxqh)
    en_course_num = get_en_course_num()
    remove_course = remove()
    qudexfGPA, allxfGPA, zballGPA = get_xfGPA(remove_course)
    get_xf(remove_course)
    # 插入年级
    list_info.insert(0, list_info[0][:4])

    list_mo_info = [
        list_info[30], list_info[29], '', str(allxfGPA), 'null', str(en_course_num), 'null', str(
            zballGPA), last_xnxqh[:9], last_xnxqh[-1:], '', xnxqh[:9], xnxqh[-1:], '',
        list_info[29], str(qudexfGPA), str(allxfGPA), list_info[7], 'null',
    ]

except Exception as e:
    print("[-] %s" % e)
    sys.exit(0)

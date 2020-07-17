import sys
from assets import builddocx

usage = """

Usage: python %s Studentid Password

Studentid ：学号
Password  ：强智教务系统密码

"""   % sys.argv[0]
try:
    username = sys.argv[1]

    password = sys.argv[2]

except Exception as e:
    print(usage)
    sys.exit(0)
    



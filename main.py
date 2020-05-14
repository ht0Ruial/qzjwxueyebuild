import sys
from assets import builddocx

usage = """

Usage: python %s studentid password

Please enter your studentid or password.

"""    % sys.argv[0]
try:
    username = sys.argv[1]

    password = sys.argv[2]

except Exception as e:
    print(usage)
    sys.exit()
    



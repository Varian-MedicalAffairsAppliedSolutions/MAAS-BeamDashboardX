# run like this:
# python make_license.py
from datetime import date, timedelta
import os
if __name__ == '__main__':
    expiry = date.today() + timedelta(days=365)
    with open(os.path.join(os.getcwd(),'expiration.py'),'w') as f:
        f.write('from datetime import datetime\n'),
        f.write(f"EXP_DATE = datetime({expiry.year}, {expiry.month}, {expiry.day})\n")

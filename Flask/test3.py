from datetime import datetime
date = '2022-10-15'
a = '上午'
r = (date + ' AM' if a == '上午' else date + ' PM')
print(r, type(r))
a = datetime.now().strftime('%Y-%m-%d %p')
print(a, type(a))
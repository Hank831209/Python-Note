from datetime import datetime
import re
date = '2022-10-15'
a = '上午'
r = (date + ' AM' if a == '上午' else date + ' PM')
print(r, type(r))
a = datetime.now().strftime('%Y-%m-%d %p')
print(a, type(a))
cell = '0983-760-795'
# cell = '0983760795'
cell = '02-2312-2863'
cell = '02-312-2863'
# /^09\d{2}-?\d{3}-?\d{3}$/
# (\d{2,3}-?|\(\d{2,3}\))\d{3,4}-?\d{4}
# ans = re.search(pattern=r'^09[0-9]{8}$', string=cell)
ans = re.search(pattern=r'^09\d{2}-?\d{3}-?\d{3}$', string=cell)
ans = re.search(pattern=r'^\d{2}-?\d{4}-?\d{4}$', string=cell)  # 2 -4 -4
ans = re.search(pattern=r'^\d{3}-?\d{3}-?\d{4}$', string=cell)  # 3 -3 -4
# print(ans)
if ans:
    print('我好帥')
else:
    print('失敗')
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine, distinct
from DB_EXAMPLE import EMP, DEPT, SAL_LEVEL
from sqlalchemy.sql import func, and_, or_


password = 'hank831209'
engine_url = 'mysql+pymysql://root:{}@127.0.0.1:3306/example'.format(password)
engine = create_engine(engine_url)
Session = sessionmaker(bind=engine)
session = Session()

# 01.請列出薪資比所有SALESMAN還低的員工
subquery = session.query(func.min(EMP.sal)).filter(EMP.job == 'SALESMAN').scalar_subquery()
ans1_query = session.query(EMP.empno).filter(EMP.sal < subquery)
# print(ans1_query)  # 印出SQL語法
# for i in ans1_query.all():  # 印出查詢結果
#     print('EMPNO:\t', i[0])

# 02.請列出到職年(到職日之年)最早的兩年，那兩年到職的員工，並依到職日排序
e = aliased(EMP)
# 透過子查詢和切片方式寫(不支援limit語法, 但可以用切片去做更自由)
# .label()直接在SQL語法內修改別名
subquery = session.query(func.year(e.hiredate).label('y1'))\
    .group_by(func.year(e.hiredate)).order_by(func.year(e.hiredate))[:2]
ans2_query = session.query(e.empno, func.year(e.hiredate))\
    .filter(func.year(e.hiredate).in_(subquery))\
    .order_by(e.hiredate)

# print(subquery)
# for i in ans2_query.all():
#     print(i)

# 03.請列出主管的主管是KING的員工
e = aliased(EMP)
subquery1 = session.query(e.empno).filter(e.ename == 'KING')
subquery2 = session.query(e.empno).filter(e.mgr.in_(subquery1))
subquery3 = session.query(e.empno).filter(e.mgr.in_(subquery2)).order_by(e.mgr)
ans3_query = session.query(e.empno, e.ename).filter(e.empno.in_(subquery3)).order_by(e.mgr)
# print(ans3_query)
# for i in ans3_query.all():
#     print(i)

# 04.請列出部門內員工薪資有3種薪資等級之部門名稱、部門所在地
e = aliased(EMP)
s = aliased(SAL_LEVEL)
d = aliased(DEPT)
# 因為有group_by所以要用having
subquery1 = session.query(e.deptno) \
    .select_from(e).join(s, and_(e.sal >= s.sal_min, e.sal <= s.sal_max)) \
    .group_by(e.deptno).having(func.count(distinct(s.level)) == 3)
ans4_query = session.query(d.dname, d.loc).filter(d.deptno.in_(subquery1))
# print(ans4_query)
for i in ans4_query.all():
    print(i)

# 05.請列出跟員工姓名最後一字元是S的員工同部門，該部門薪資最低的員工之部門名稱、姓名、
# 薪資
e = aliased(EMP)
s = aliased(SAL_LEVEL)
d = aliased(DEPT)
subquery1 = session.query(distinct(e.deptno)).filter(e.ename.like('%s'))  # 20, 30
subquery2 = session.query(e.deptno)\
    .filter(e.deptno.in_(subquery1)).group_by(e.deptno)\
    .order_by(e.deptno)  # (20, 800), (950, 30)  func.min(e.sal)
subquery3 = session.query(func.min(e.sal))\
    .filter(e.deptno.in_(subquery1)).group_by(e.deptno)\
    .order_by(e.deptno)
subquery4 = session.query(e.empno)\
    .filter(e.deptno.in_(subquery2)).filter(e.sal.in_(subquery3))
# subquery4 = session.query(e.empno)\
#     .filter(and_(e.deptno.in_(subquery2), e.sal.in_(subquery3)))  # 效果同上
ans5_query = session.query(d.dname, e.ename, e.sal)\
    .select_from(e).join(d, e.deptno == d.deptno)\
    .filter(e.empno.in_(subquery4))
# print(ans5_query)
# for i in subquery4:
#     print(i)











from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine
from DB_EXAMPLE import EMP, DEPT, SAL_LEVEL
from sqlalchemy.sql import func, and_, or_


password = 'hank831209'
engine_url = 'mysql+pymysql://root:{}@127.0.0.1:3306/example'.format(password)
engine = create_engine(engine_url)
Session = sessionmaker(bind=engine)
session = Session()


# 01.請列出所有員工的員工編號、姓名、職稱、部門編號及部門名稱
ans1_query = session.query(EMP.empno, EMP.ename, EMP.job,
                           EMP.deptno).join(DEPT, DEPT.deptno == EMP.deptno).order_by(
                            EMP.deptno.desc())
# print(ans1_query)  # 印出SQL語法
# for i in ans1_query.all():  # 印出查詢結果
#     print(i)

# 02.請列出所有部門編號為30且職稱為"SALESMAN"之部門名稱、員工姓名、獎金
ans2_query = session.query(DEPT.dname, EMP.ename, EMP.comm).\
    filter(EMP.deptno == 30, EMP.job == 'SALESMAN').join(DEPT, DEPT.deptno == EMP.deptno)
# print(ans2_query)
# for i in ans2_query.all():  # 印出查詢結果
#     print(i)

# 03.請列出薪水等級為"B"的員工之員工編號、員工姓名、薪資
e = aliased(EMP)  # 取別名, 但生成的SQL語句不會寫入這個別名
s = aliased(SAL_LEVEL)
# 解法1, join玩再查
# ans3_query = session.query(e.empno, e.ename, e.sal) \
#     .select_from(e).join(s, and_(e.sal >= s.sal_min, e.sal <= s.sal_max)) \
#     .filter(s.level == 'B')

# 解法2, 先找level 'B' 的金額範圍再去查詢
subquery_min = session.query(s.sal_min).filter(s.level == 'B').scalar_subquery()
subquery_max = session.query(s.sal_max).filter(s.level == 'B').scalar_subquery()
ans3_query = session.query(e.empno, e.ename, e.sal) \
    .filter(e.sal >= subquery_min).filter(e.sal <= subquery_max)

# print(ans3_query)
# for i in ans3_query.all():  # 印出查詢結果
#     print(i)

# 04.請列出部門編號、部門名稱及部門人數
e = aliased(EMP)
d = aliased(DEPT)
# select_from() 決定誰在左邊, 所以是d left outerjoin e
ans4_query = session.query(d.deptno, d.dname, func.count(e.empno))\
    .select_from(d).outerjoin(e, e.deptno == d.deptno).group_by(d.deptno)
# print(ans4_query)
# for i in ans4_query.all():  # 印出查詢結果
#     print(i)

# 05.請列出每個主管之姓名、直屬下屬人數、直屬下屬平均薪資，並依直屬減下屬人數遞、主
# 管姓名遞增排序
e1 = aliased(EMP)
e2 = aliased(EMP)
ans5_query = session.query(e2.ename, func.count(e1.empno), func.avg(e1.sal)) \
    .select_from(e1).join(e2, e1.mgr == e2.empno) \
    .group_by(e1.mgr).order_by(func.count(e1.empno).desc(), e2.ename)
# print(ans5_query)
# for i in ans5_query.all():  # 印出查詢結果
#     print(i)





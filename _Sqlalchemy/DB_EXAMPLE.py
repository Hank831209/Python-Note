from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Numeric, DATETIME, ForeignKey
# from sqlalchemy.orm import relationship


Base = declarative_base()


class SAL_LEVEL(Base):
    __tablename__ = 'SAL_LEVEL'
    # enum('A', 'B', 'C', 'D')
    level = Column('level', Enum('A', 'B', 'C', 'D'), primary_key=True, nullable=False)
    sal_min = Column('sal_min', Numeric, nullable=False)  # decimal(6, 2)
    sal_max = Column('sal_max', Numeric, nullable=False)  # decimal(6, 2)

    def __init__(self, level, sal_min, sal_max):
        self.level = level
        self.sal_min = sal_min
        self.sal_max = sal_max


# empno, ename, job, mgr, hiredate, sal, comm, deptno
class EMP(Base):
    __tablename__ = 'EMP'
    empno = Column('empno', Integer, primary_key=True, nullable=False)
    ename = Column('ename', String)
    job = Column('job', String)
    mgr = Column('mgr', Integer)
    hiredate = Column('hiredate', DATETIME)
    sal = Column('sal', Numeric)  # decimal(6, 2)
    comm = Column('comm', Numeric)  # decimal(6, 2)
    deptno = Column('deptno', Integer, nullable=False)

    def __init__(self, empno, ename, job, mgr, hiredate, sal, comm, deptno):
        self.empno = empno
        self.ename = ename
        self.job = job
        self.mgr = mgr
        self.hiredate = hiredate
        self.sal = sal
        self.comm = comm
        self.deptno = deptno


# dept ---> DEPTNO(INT, PK), DNAME(VARCHAR), LOC(VARCHAR)
class DEPT(Base):
    __tablename__ = 'DEPT'
    deptno = Column('deptno', Integer, ForeignKey('EMP.deptno'), primary_key=True, nullable=False)
    dname = Column('dname', String)
    loc = Column('LOC', String)

    def __init__(self, deptno, dname, loc):
        self.deptno = deptno
        self.dname = dname
        self.loc = loc


from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class Person(Base):
    __tablename__ = 'Person'  # 表格名
    # 欄位設置
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(45))
    sex = Column(String(45))

    def __init__(self, id, name, sex):
        self.id = id
        self.name = name
        self.sex = sex

# 初始化数据库连接:
password = '0983760795'
engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/test', echo=False)
Base.metadata.create_all(engine)  # 創建所有資料表

# 建立連線
DBSession = sessionmaker(bind=engine)

# 新增資料(insert)
session = DBSession()
item1 = Person(id=1, name='xgx', sex='male')
session.add(item1)

item2 = Person(id=2, name='xgx1', sex='female')
session.add(item2)

item3 = Person(id=3, name='xgx1', sex='male')
session.add(item3)

item4 = Person(id=4, name='xgx2', sex='female')
session.add(item4)

session.commit()
session.close()

# # 查詢資料(select)
session1 = DBSession()
persons = session1.query(Person).filter(Person.id < '4').all()

for i in range(len(persons)):
    print('ID: ', persons[i].id, '姓名: ', persons[i].name, '性別: ', persons[i].sex)

session1.close()

# 修改(update)
# session2 = DBSession()
# session2.query(Person).filter(Person.id == '2').update({Person.name: 'yyy'})
# session2.commit()
# session2.close()

# ## 查看修改结果
# session3 = DBSession()
# print('\n')
# print(session3.query(Person).filter(Person.id == '2').one().name)
# session3.close()

# # 刪除(delete)
# session4 = DBSession()
# session4.query(Person).filter(Person.id == '3').delete()
# session4.commit()
# session4.close()
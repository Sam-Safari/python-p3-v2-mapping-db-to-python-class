import os

# Ensure clean DB before importing connection (so sqlite creates a fresh file)
try:
    os.remove('company.db')
except FileNotFoundError:
    pass

from lib.__init__ import CONN, CURSOR
from lib.department import Department

# Run checks mirroring the pytest tests
# Drop tables
CURSOR.execute("DROP TABLE IF EXISTS employees")
CURSOR.execute("DROP TABLE IF EXISTS departments")
Department.all = {}

# create table
Department.create_table()
# save test
department = Department('Payroll','Building A, 5th Floor')
department.save()
row = CURSOR.execute('SELECT * FROM departments').fetchone()
assert (row[0],row[1],row[2])==(department.id,department.name,department.location)

# create via classmethod
Department.drop_table()
Department.create_table()
d = Department.create('Payroll','Building A, 5th Floor')
row = CURSOR.execute('SELECT * FROM departments').fetchone()
assert (row[0],row[1],row[2])==(d.id,d.name,d.location)

# update
Department.drop_table(); Department.create_table()
department1 = Department.create('Human Resources','Building C, East Wing')
department2 = Department.create('Marketing','Building B, 3rd Floor')
id1 = department1.id
id2 = department2.id
# change department2
department2.name = 'Sales and Marketing'
department2.location = 'Building B, 4th Floor'
department2.update()
# check id1 unaffected
dept = Department.find_by_id(id1)
assert (dept.id,dept.name,dept.location)==(id1,'Human Resources','Building C, East Wing')
# check id2 updated
dept = Department.find_by_id(id2)
assert (dept.id,dept.name,dept.location)==(id2,'Sales and Marketing','Building B, 4th Floor')

# delete
Department.drop_table(); Department.create_table()
department1 = Department.create('Human Resources','Building C, East Wing')
department2 = Department.create('Sales and Marketing','Building B, 4th Floor')
id1 = department1.id; id2 = department2.id
department2.delete()
# id1 exists
dept = Department.find_by_id(id1)
assert (dept.id,dept.name,dept.location)==(id1,'Human Resources','Building C, East Wing')
# id2 deleted
assert Department.find_by_id(id2) is None
assert (department2.id,department2.name,department2.location)==(None,'Sales and Marketing','Building B, 4th Floor')
assert Department.all.get(id2) is None

# instance_from_db
Department.drop_table(); Department.create_table()
Department.create('Payroll','Building A, 5th Floor')
row = CURSOR.execute('SELECT * FROM departments').fetchone()
dep = Department.instance_from_db(row)
assert (row[0],row[1],row[2])==(dep.id,dep.name,dep.location)

# get_all
Department.drop_table(); Department.create_table()
d1 = Department.create('Human Resources','Building C, East Wing')
d2 = Department.create('Marketing','Building B, 3rd Floor')
all_depts = Department.get_all()
assert len(all_depts)==2
assert (all_depts[0].id,all_depts[0].name,all_depts[0].location)==(d1.id,'Human Resources','Building C, East Wing')
assert (all_depts[1].id,all_depts[1].name,all_depts[1].location)==(d2.id,'Marketing','Building B, 3rd Floor')

# find_by_name
Department.drop_table(); Department.create_table()
d1 = Department.create('Human Resources','Building C, East Wing')
d2 = Department.create('Marketing','Building B, 3rd Floor')
assert (Department.find_by_name('Human Resources').id,Department.find_by_name('Human Resources').name)==(d1.id,'Human Resources')
assert (Department.find_by_name('Marketing').id,Department.find_by_name('Marketing').name)==(d2.id,'Marketing')
assert Department.find_by_name('Unknown') is None

print('All local checks passed')

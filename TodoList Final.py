from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    '''Table is the name of the model class. 
    It is used to access data from the table it describes. 
    The name of the class can be anything.

__tablename__ specifies the table name in the database.

id is an integer column of the table; primary_key=True says that this column is the primary key.

string_field is a string column; default='default_value' says that the default value of this column is 'default_value'.

date_field is a column that stores the date. SQLAlchmey automatically converts SQL date into a Python datetime object.

__repr__ method returns a string representation of the class object. In the ORM concept, each row in the table is an object of a class.'''
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class TodoList:

    def MainMenu(self):
        while True:
            print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
            ui = self.UI()
            if ui == '1':
                self.today_task()
            elif ui == '2':
                self.week_task()
            elif ui == '3':
                self.all_task()
            elif ui == '4':
                self.missed_task()
            elif ui == '5':
                self.add_task()
            elif ui == '6':
                self.delete_task()
            elif ui == '0':
                print("\nBye!")
                break

    def UI(self):
        user_input = input()
        return user_input

    def today_task(self):
        today = datetime.today()
        day_tasks = session.query(Table).filter(Table.deadline == today).all()
        print(f'Today {today.day} {today.strftime("%b")}:')
        if not day_tasks:
            print("Nothing to do!")
        else:
            for i in range(len(day_tasks)):
                print(day_tasks[i].task)

    def week_task(self):
        today = datetime.today()
        weekday_dict = {0: 'Monday',
                        1: 'Tuesday',
                        2: 'Wednesday',
                        3: 'Thursday',
                        4: 'Friday',
                        5: 'Saturday',
                        6: 'Sunday'}

        for i in range(7):
            week_date = today + timedelta(days=i)
            week_task = session.query(Table).filter(Table.deadline == week_date.date()).all()
            week_day = week_date.weekday()

            print(f"\n{weekday_dict[week_day]} {week_date.day} {week_date.strftime('%b')}:")
            if not week_task:
                print("Nothing to do!")
            else:
                for i in range(len(week_task)):
                    print(f"{i + 1}. {week_task[i].task}")
                print("")

    def all_task(self):
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        for i in range(len(all_tasks)):
            deadline_date = all_tasks[i].deadline
            print(f"{i+1}. {all_tasks[i].task}. {deadline_date.day} {deadline_date.strftime('%b')}")

    def missed_task(self):
        missed_tasks = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
        print("Missed tasks:")
        if not missed_tasks:
            print("Nothing is missed!")
        for i in range(len(missed_tasks)):
            missed_deadline = missed_tasks[i].deadline
            print(f"{i+1}. {missed_tasks[i].task}. {missed_deadline.day} {missed_deadline.strftime('%b')}")
        print('')

    def add_task(self):
        print("Enter task")
        user_input = self.UI()
        print("Enter deadline")
        deadline_input = self.UI()
        new_row = Table(task=user_input, deadline=datetime.strptime(deadline_input, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    def delete_task(self):
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        print("Chose the number of the task you want to delete:")
        for i in range(len(all_tasks)):
            deadline_date = all_tasks[i].deadline
            print(f"{i+1}. {all_tasks[i].task}. {deadline_date.day} {deadline_date.strftime('%b')}")
        to_delete = int(self.UI()) - 1
        row_delete = all_tasks[to_delete]
        session.delete(row_delete)
        session.commit()
        print("The task has been deleted!")


# MainMenu()
tdl = TodoList()
tdl.MainMenu()



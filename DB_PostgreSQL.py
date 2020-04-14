import psycopg2

conn = psycopg2.connect(dbname='netology_test', user='netology_user', password='test')
cur = conn.cursor()


class db_work:
    def create_db():  # ??????? ???????
        cur.execute("""
        create table if not exists Student(
        id integer not null,
        name character varying(100) not null,
        gpa numeric(10,2),
        birth timestamp with time zone);
        """)

        cur.execute("""
            create table if not exists Course(
            id integer not null,
            name character varying(100) not null);
            """)

        conn.commit()

    def get_students(course_id):  # ?????????? ????????? ????????????? ?????
        cur.execute("SELECT name FROM Course where id = (%s)", (course_id,))
        print(f'на курсе {course_id} учаться следующие студенты:')
        for students_list in cur.fetchall():
            for student_name in students_list:
                print(student_name)

    def add_students(course_id, students):  # ??????? ????????? ?
        for student in students:
            cur.execute("INSERT INTO Student (id, name, gpa, birth) VALUES (%s, %s, %s, %s)",
                        (student[0], student[1], student[2], student[3]))
            cur.execute("INSERT INTO Course (id, name) VALUES (%s, %s)",
                        (course_id, student[1]))
        conn.commit()

    def add_student(Student):  # ?????? ??????? ????????
        cur.execute("INSERT INTO Student (id, name, gpa, birth) VALUES (%s, %s, %s, %s)",
                    (Student[0], Student[1], Student[2], Student[3]))
        conn.commit()

    def get_student(student):
        cur.execute("SELECT id, name, gpa, birth FROM Student WHERE id = (%s)", (student[0],))
        print(cur.fetchall())


Student1 = ["1", "Ivan", "4.2", "01.01.2020"]
Student2 = ["2", "Anton", "4.3", "01.01.2019"]
Student3 = ["3", "Boris", "4.5", "01.01.2018"]
Students_list = [Student2, Student3]

db_work.create_db()
db_work.add_student(Student1)
db_work.get_student(Student1)
db_work.add_students(3, Students_list)
db_work.get_students(3)
conn.close()

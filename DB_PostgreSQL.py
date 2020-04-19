import psycopg2

conn = psycopg2.connect(dbname='netology_test', user='netology_user', password='test')
cur = conn.cursor()


class db_work:
    def create_db():
        cur.execute("""
        create table if not exists Student(
        id integer not null PRIMARY KEY,
        name character varying(100) not null,
        gpa numeric(10,2),
        birth timestamp with time zone);
        """)

        cur.execute("""
            create table if not exists Course(
            id integer not null PRIMARY KEY,
            name character varying(100) not null);
            """)

        cur.execute("""
            create table if not exists Course_and_Student(
            id_course integer not null,
            id_student integer not null,
            CONSTRAINT ID_course_student PRIMARY KEY (id_course,id_student));
            """)

        conn.commit()

    def get_students(course_id):
        cur.execute("""
            SELECT Student.name, course.name
            FROM Course_and_Student
            INNER JOIN Student ON Course_and_Student.id_student = Student.id
            INNER JOIN Course ON Course_and_Student.id_course = Course.id
            WHERE Course_and_Student.id_course = (%s)""", (course_id,))
        students_list = cur.fetchall()
        print(f'на курсе {students_list[0][1]} учаться следующие студенты:')
        for student_name in students_list:
            print(student_name[0])

    def add_students(course_id, students):
        for student in students:
            cur.execute("INSERT INTO Student (id, name, gpa, birth) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (student[0], student[1], student[2], student[3]))
            cur.execute("INSERT INTO Course (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (course_id, f'ADPY-{course_id}'))
            cur.execute("INSERT INTO Course_and_Student (id_course, id_student) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (course_id, student[0]))
        conn.commit()

    def add_student(Student):
        cur.execute("INSERT INTO Student (id, name, gpa, birth) VALUES (%s, %s, %s, %s)  ON CONFLICT DO NOTHING",
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

import sqlite3
import time
import hashlib

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def define_tables():
    global connection, cursor

    course_query=   '''
                        CREATE TABLE course (
                                    course_id INTEGER,
                                    title TEXT,
                                    seats_available INTEGER,
                                    PRIMARY KEY (course_id)
                                    );
                    '''

    student_query=  '''
                        CREATE TABLE student (
                                    student_id INTEGER,
                                    name TEXT,
                                    PRIMARY KEY (student_id)
                                    );
                    '''

    enroll_query= '''
                    CREATE TABLE enroll (
                                student_id INTEGER,
                                course_id INTEGER,
                                enroll_date DATE,
                                grade TEXT,
                                PRIMARY KEY (student_id, course_id),
                                FOREIGN KEY(student_id) REFERENCES student(student_id),
                                FOREIGN KEY(course_id) REFERENCES course(course_id)
                                );
                '''
    

    cursor.execute(course_query)
    cursor.execute(student_query)
    cursor.execute(enroll_query)
    connection.commit()

    return

def insert_data():
    global connection, cursor

    insert_courses = '''
                        INSERT INTO course(course_id, title, seats_available) VALUES
                            (1, 'CMPUT 291', 200),
                            (2, 'CMPUT 391', 100),
                            (3, 'CMPUT 101', 300);
                     '''

    insert_students =  '''
                        INSERT INTO student(student_id, name) VALUES
                                (1509106, 'Saeed'),
                                (1409106, 'Alex'),
                                (1609106, 'Mike');
                       '''

    cursor.execute(insert_courses)
    cursor.execute(insert_students)
    connection.commit()
    return

def drop_tables():
    global connection, cursor

    drop_course = "DROP TABLE IF EXISTS course; "
    drop_student = "DROP TABLE IF EXISTS student; "
    drop_enroll = "DROP TABLE IF EXISTS enroll; "

    cursor.execute(drop_enroll)
    cursor.execute(drop_student)
    cursor.execute(drop_course)

def enroll_assign_grades():
    global connection, cursor

    cursor.execute('SELECT * FROM course;')
    all_courses = cursor.fetchall()

    cursor.execute('SELECT * FROM student;')
    all_students = cursor.fetchall()

    Grades = ['A', 'A', 'C', 'B', 'C', 'B', 'F', 'C', 'A']
    i=0

    for every_course in all_courses:
        for every_student in all_students:
            enroll(every_student[0], every_course[0])

            data = (Grades[i], every_student[0], every_course[0])
            cursor.execute('UPDATE enroll SET grade=? where student_id=? and course_id=?;', data)
            i += 1

    return

def enroll(student_id, course_id):
    global connection, cursor

    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    crs_id = (course_id,)
    cursor.execute('SELECT seats_available FROM course WHERE course_id=?;', crs_id)
    seats_available = cursor.fetchone()[0]

    if seats_available > 0:
        data = (student_id, course_id, current_date)
        cursor.execute('INSERT INTO enroll (student_id, course_id, enroll_date) VALUES (?,?,?);', data) 
        cursor.execute('UPDATE course SET seats_available = seats_available - 1 where course_id=?;', crs_id)
    
    connection.commit()
    return

def drop(student_id, course_id):
    global connection, cursor

    data = { 'course_id': course_id, 'student_id': student_id }
    cursor.execute("""
        DELETE FROM enroll WHERE student_id = ? AND course_id = ?;
    """, data)
    cursor.execute("""
        UPDATE course SET seats_available = seats_available + 1
        WHERE course_id = :course_id AND NOT EXISTS (
            SELECT * FROM enroll
            WHERE student_id = :student_id AND course_id = :course_id
        );
    """, data)
    connection.commit()

    return


def GPA(grade):
    global connection, cursor

    if grade == 'A':
        return 4
    if grade == 'B':
        return 3
    if grade == 'C':
        return 2
    return 0


def main():
    global connection, cursor
    path = "./register.db"
    connect(path)
    connection.create_function('GPA', 1, GPA)
    define_tables()
    insert_data()
    enroll_assign_grades()

    cursor.execute('''
        SELECT s.name, AVG(GPA(e.grade)) AS avg_gpa
        FROM student AS s, enroll AS e
        WHERE s.student_id = e.student_id
        GROUP BY s.name
        ORDER BY avg_gpa;
    ''')
    all_entry = cursor.fetchall()
    for one_entry in all_entry:
        print(one_entry)

    drop_tables()
    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
    main()
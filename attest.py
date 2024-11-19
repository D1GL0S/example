# задание 1
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

point1 = Point(2, 3)


#2
class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def is_strong_password(self):
        if len(self.password) >= 8 and self.password != self.login:
            return True
        else:
            return False

short_pswd = User('user', 'qwerty')
simple_pswd = User('super_user', 'super_user')
strong_pswd = User('admin', 'Qwerty12345')

print(short_pswd.is_strong_password())
print(simple_pswd.is_strong_password())
print(strong_pswd.is_strong_password())

#3
class NobelWinner:
    def __init__(self, winner, year, category):
        self.winner = winner
        self.year = year
        self.category = category

    def __str__(self):
        return f'{self.winner} выиграл нобелевскую премию по {self.category} в {self.year}'


winner = NobelWinner('Роджер Пенроуз', 2020, 'физика')
print(winner)



#4
def sort_case_insensitive(lst):
    return sorted(lst, key=str.lower)
a = ['context', 'Visible', 'center', 'acquisition', 'Football', 'testify', 'Responsible', 'cause']
print(sort_case_insensitive(a))


#5
class Person:
    def __init__(self, firstname, lastname, surname):
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname


def __str__(self):
    return f'{self.lastname} {self.firstname} {self.surname}'

class Student(Person):
    def go_to_class(self, subject):
        print(f'Школьник {self.firstname} {self.lastname} идет на {subject}')

class Teacher(Person):
    def teach_class(self, subject):
        print(f'Учитель {self.firstname} {self.lastname} преподает {subject}')
        
student = Student('Иван', 'Иванов', 'Иванович')
teacher = Teacher('Петр', 'Петров', 'Эдуардович')
student.go_to_class('математику')
teacher.teach_class('информатику')
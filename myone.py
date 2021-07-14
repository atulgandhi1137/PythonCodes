
class Person:
    def draw(self,n):
        print('Draw a shape of size', n)


class Student(Person):
    def draw(self):
        print('Drawing a student')


s = Student()

s.draw()
s.draw(8)

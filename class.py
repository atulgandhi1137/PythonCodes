
class Vehicle:
    def __init__(self):
        print('You have created the Vehicle class')

class Truck(Vehicle):
    def __init__(self):
        print('You have created the Truck class')

    def wheels(self):
        print('Your vehicle has 8 wheels')

class Car(Vehicle):
    def __init__(self):
        print('You have created the Car class')

    def wheels(self):
        print('\nYour vehicle has 4 wheels')
    
    def own(self):
        print("\nIt's just a car !!")

class BMW(Car):
    def __init__(self):
        print('You have created the BMW class')

    def own(self):
        print('You own a BMW Car !!')
        
class Audi(Car):
    def __init__(self):
        print('You have created the Audi class')

    def own(self):
        print('You own a Audi Car !!')


v1 = Vehicle()
c1 = Car()
t1 = Truck()
b1 = BMW()
a1 = Audi()

c1.wheels()
t1.wheels()
c1.own()
b1.own()
a1.own()



print(globals())


        

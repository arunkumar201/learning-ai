class Person:
    def __init__(self) -> None:
        # Public attribute (can be accessed from anywhere)
        self.name = "John"

        # Protected attribute (single underscore)
        # Convention: Should not be accessed outside class/subclasses
        self._age = 25

        # Private attribute (double underscore)
        # Name mangling: Can't be easily accessed outside class
        self.__salary = 50000

        print("This is a constructor")

    # Public method
    def talk(self, n):
        print(f"Hello, I am {self.name}. {n}")
        self.__private_method()  # Can access private method inside class

    # Protected method
    def _calculate_bonus(self):
        return self.__salary * 0.1

    # Private method
    def __private_method(self):
        print("This is a private method")
    
    def _get_person_salary(self):
        print(self.__salary)

    def get_details(self):
        print(f"Name (public): {self.name}")
        print(f"Age (protected): {self._age}")
        print(f"Salary (private): {self.__salary}")
        print(f"Bonus (protected method): {self._calculate_bonus()}")


my_person = Person()

# Public access - Works fine
print(my_person.name)  # OK
my_person.talk(1)  # OK

# Protected access - Works but shouldn't be used (convention)
print(my_person._age)  # "Works" but not recommended

# Private access - Will raise AttributeError
try:
    print(my_person.__salary)  # Error!
except AttributeError as e:
    print("Can't access private attribute:", e)

# Accessing all details through public method
my_person.get_details()

# print(my_person.__private_method)

# calling private method
try:
    my_person._get_person_salary()
except AttributeError as e:
    print("Can't access private attribute:", e)
except Exception as e:
    print("An error occurred:", e)


# parent and child class
class Parent:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def talk(self):
        print(f"Hello, my name is {self.name}")

    def _protected_method(self):
        print("This is a protected method")

    def __private_method(self):
        print("This is a private method")


class Child(Parent):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade

    def talk(self):
        print(f"Hello, my name is {self.name} and I am {self.grade} grade")


child = Child("John", 25, 10)
child.talk()

try:
    child._protected_method()
except Exception as e:
    print("An error occurred:", e)

try:
    child.__private_method()  # this will raise an error as it is private
except Exception as e:
    print("An error occurred:", e)

# polymorphism - child class can access parent class methods
child.talk()
child._protected_method()


# abstract class
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def make_sound(self):
        print(f"{self.name} makes a sound- {self.sound}")

    def speak(self):
        print(f"{self.name} speaks")

    def eat(self):
        print(f"{self.name} eats")

    def sleep(self):
        print(f"{self.name} sleeps")

    def __str__(self):
        return f"{self.name} is an animal"


class Dog(Animal):
    def __init__(self, name, sound):
        super().__init__(name, sound)
        self.sound = "bark"


class Cat(Animal):
    def __init__(self, name, sound):
        super().__init__(name, sound)
        self.sound = sound


dog = Dog("Fido", "bark")
cat = Cat("Whiskers", "meow")

# Dog
print("-------DOG-------")
dog.make_sound()
dog.speak()
dog.eat()
print("-------CAT-------")
# Cat
cat.make_sound()
cat.speak()
cat.eat()

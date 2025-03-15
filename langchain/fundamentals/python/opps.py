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

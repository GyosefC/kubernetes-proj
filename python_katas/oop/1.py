class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hello, my name is {self.name}, and I am {self.age} years old.")

    def speak(self):
        print("I am speaking!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!.")


# Create objects (instances of the class)
person1 = Person("John", 25)
person2 = Person("Mary", 30)

# Call object methods
person1.introduce()
person2.introduce()
person1.speak()


############################################################## Class Person ##############################################################


class Student(Person):
    def __init__(self, name, age, course):
        # Call the constructor of the parent class
        super().__init__(name, age)
        self.course = course

    def study(self):
        print(f"{self.name} is studying in the {self.course} course.")

    def speak(self):
        print(f"{self.name} is speaking.")


# Create objects (instances of the Student class)
student1 = Student("Anna", 20, "second")

# Call object methods
student1.introduce()
student1.study()
student1.speak()

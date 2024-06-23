class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def make_sound(self):
        pass

    def introduce(self):
        print(f"I am a {self.species} named {self.name}.")


animal = Animal("Rover", "Dog")
animal.introduce()
print("==" * 50)


class Dog(Animal):
    def __init__(self, name, species, breed, age):
        super().__init__(name, species)
        self.breed = breed
        self.age = age

    def make_sound(self):
        print("Woof!")

    def introduce(self):
        print(f"I am a {self.species} named {self.name}. I am a {self.breed} and I am {self.age} years old.")


class Cat(Animal):
    def make_sound(self):
        print("Meow!")


class Bird(Animal):
    def make_sound(self):
        print("Tweet!")


dog = Dog("Buddy", "Dog", "Golden Retriever", 3)
cat = Cat("Whiskers", "Cat")
bird = Bird("Tweetie", "Bird")

dog.introduce()
dog.make_sound()

cat.introduce()
cat.make_sound()

bird.introduce()
bird.make_sound()

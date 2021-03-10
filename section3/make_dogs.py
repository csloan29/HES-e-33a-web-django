from dogs.models import User, Dog, City

cities = [
    ("Cambridge", "02138"),
    ("Gilford", "03249"),
    ("New York", "10001"),
    ("Lebanon", "37087")
]

users = [
    ("z", "b", "Sophie", 18),
    ("y", "c", "Connor", 20),
    ("x", "d", "Sydney", 19),
    ("w", "e", "Caroline", 20),
    ("v", "f", "Nora", 26)
]

dogs = [
    ("Quinn", 11, "03249"),
    ("Willow", 9, "10001"),
    ("Maisy", 1, "02138"),
    ("Fern", 4, "37087"),
    ("Winston", 12, "03249")
]

dogs_people = [
    ("Quinn", ["Connor", "Sophie"]),
    ("Winston", ["Connor", "Sophie"]),
    ("Willow", ["Sydney"]),
    ("Maisy", ["Caroline"]),
    ("Fern", ["Nora"])
]

# Make cities:
for name, zipcode in cities:
    city_model = City(name=name, zip_code=zipcode)
    city_model.save()

# Make Users:
for username, password, name, age in users:
    user_model = User(username=username, name=name, age=age)
    user_model.save()

# Make Dogs:
for name, age, zipcode in dogs:
    city_model = City.objects.get(zip_code=zipcode)
    dog_model = Dog(name=name, age=age, home=city_model)
    dog_model.save()

# Associate dogs with people
for dog, people in dogs_people:
    dog_obj = Dog.objects.get(name=dog)
    for person in people:
        person_obj = User.objects.get(name=person)
        dog_obj.people.add(person_obj)

# exec(open('db_populate.py').read())
# admin
# sumo2993

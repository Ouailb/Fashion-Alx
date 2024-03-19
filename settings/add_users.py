#!/usr/bin/python3
from models.user import User
from faker import Faker


fake = Faker()
# create 150 user
for i in range(10):
    name = fake.name().split(" ")
    pwd_lenght = fake.random_int(min=8, max=15)
    data = {
        "first_name": name[0],
        "last_name": name[1],
        "password": fake.password(length=pwd_lenght),
        "address": fake.address(),
        "email": fake.email(),
        "phone": fake.phone_number()
    }
    new_user = User(**data)
    new_user.save()

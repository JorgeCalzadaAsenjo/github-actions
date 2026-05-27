from objects import Db, Item, User

users: list[User] = [
    User(id = 0, name = "Admin", password = "01234"),
    User(id = 1, name = "Jorge", password = "12345"),
    User(id = 2, name = "Andrea", password = "123456"),
    User(id = 3, name = "Juan", password = "1234"),
    User(id = 4, name = "Pepe", password = "1234"),
    User(id = 5, name = "Maria", password = "1234"),
    User(id = 6, name = "Lucia", password = "1234"),
]

items: list[Item] = [
    Item(id = 0, name = "Foo", price = 50.2,is_offer = True),
    Item(id = 1, name = "Bar", price = 62.0,is_offer = False),
    Item(id = 2, name = "Baz", price = 50.2,is_offer = True),
    Item(id = 3, name = "Foz", price = 25.2,is_offer = True),
    Item(id = 4, name = "Baw", price = 90.0,is_offer = False),
    Item(id = 5, name = "Bam", price = 63.0,is_offer = True),
]

db = Db(users = users, items = items)

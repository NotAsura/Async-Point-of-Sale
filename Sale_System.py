import asyncio
from main import *
from inventory import *

i = Inventory()

total_price = 0
burger_id = []
side_id = []
drink_id = []
order_id = []
burger = []
side = []
drink = []

# Checks inventory of the object to make sure the item ordered is in stock
async def check_stock(arr):
    print("Placing order...")
    for j in arr:
        if await i.get_stock(j) == False:
            print(
                f"Unfortunately item number {j} is out of stock and has been removed from your order. Sorry!")
        else:
            if j < 7:
                burger_id.append(j)
            elif j < 12:
                side_id.append(j)
            elif j < 21:
                drink_id.append(j)

#Prints the menu that is used to order from
def print_catalogue():
    print("Welcome to the ProgrammingExpert Burger Bar!")
    print("Loading Catalogue...")
    display_catalogue(i.catalogue)

#Takes the order and adds the ids of the items into an array
def place_order():
    print("Please enter the number of items that you would like to add to your order. Enter q to complete your order.")
    num = ""
    while not num == "q":
        num = input("Enter an item Number: ")
        try:
            if num == "q":
                break
            elif int(num) <= 0:
                print("Please enter a valid number.")
                continue
            elif int(num) >= 21:
                print("Please enter a number below 21.")
                continue
            else:
                order_id.append(int(num))
        except:
            print("Please enter a valid number.")
            continue

    return order_id

#Gets the names of either the drinks of the sides
def get_name(item):
    if item["id"] <= 9:
        return "Fries"
    elif item["id"] <= 11:
        return "Caesar Salad"
    elif item["id"] <= 14:
        return "Coke"
    elif item["id"] <= 17:
        return "Ginger Ale"
    elif item["id"] <= 20:
        return "Chocolate Milk Shake"

#Takes an old array of ids and puts a dictionary of the item ordered into an new array. Only works for burgers
def add_burger_dic(type, arr, new_arr):
    for p in arr:
        for j in i.catalogue[type]:
            if j["id"] == p:
                new_arr.append(j)

#Takes an old array of ids and puts a dictionary of the item ordered into an new array. Only works for drinks
def add_drink_dic(arr, new_arr):
    keys = ["Coke", "Ginger Ale", "Chocolate Milk Shake"]
    for p in arr:
        for w in keys:
            for j in i.catalogue["Drinks"][w]:
                if j["id"] == p:
                    new_arr.append(j)

#Takes an old array of ids and puts a dictionary of the item ordered into an new array. Only works for sides
def add_side_dic(arr, new_arr):
    keys = ["Fries", "Caesar Salad"]
    for p in arr:
        for w in keys:
            for j in i.catalogue["Sides"][w]:
                if j["id"] == p:
                    new_arr.append(j)

#Takes in an array of the items ordered in dictionary form and orders it by price from least to greatest
def sort_by_price(arr):
    arr.sort(key=lambda x: x["price"])

#Takes in three arrays consisting of burgers, sides, and drinks, and makes combos using the expensive ones 
def make_combos(burgers, sides, drinks):
    global total_price
    print("\nHere is a summary of your order:")
    print("\n")
    while len(burgers) > 0 and len(sides) > 0 and len(drinks) > 0:
        burg = burgers.pop()
        sid = sides.pop()
        drin = drinks.pop()
        cost = burg["price"] + sid["price"] + drin["price"]
        dis_cost = round(cost * .85, 2)
        burg_name = burg["name"]
        sid_size = sid["size"]
        drin_size = drin["size"]
        sid_name = get_name(sid)
        drin_name = get_name(drin)
        print(f"${dis_cost} Burger Combo")
        print(f"  {burg_name}")
        print(f"  {sid_size} {sid_name}")
        print(f"  {drin_size} {drin_name}")
        total_price = total_price + dis_cost

#Prints the rest of the items that weren't placed into a combo
def print_order(burgers, sides, drinks):
    global total_price
    for i in burgers:
        price = i["price"]
        name = i["name"]
        print(f"${price} {name}")
        total_price += price
    for i in sides:
        name = get_name(i)
        size = i["size"]
        price = i["price"]
        print(f"${price} {size} {name}")
        total_price += price
    for i in drinks:
        name = get_name(i)
        size = i["size"]
        price = i["price"]
        print(f"{price} {size} {name}")
        total_price += price
    print("\n")

#Prints the subtotal, tax, and total of the whole order
def print_price(price):
    p = round(price, 2)
    print(f"Subtotal: ${p}")
    tax = round(price * 0.05, 2)
    print(f"Tax: ${tax}")
    total = round(price + tax, 2)
    print(f"Total: ${total}\n")
    answer = ""
    while not (answer == "yes" or answer == "no"):
        answer = input(f"Would you like to purchase this order for ${total} (yes/no)?")
    if answer == "yes":
        print("Thank you for your order!")
    elif answer == "no":
        print("Goodbye")
        return "stop"

#Resets all the variables so that the customer can order again without past items messing with the order
def reset():
    global total_price
    global burger_id
    global side_id
    global drink_id
    global order_id
    global burger
    global side
    global drink
    total_price = 0
    burger_id = []
    side_id = []
    drink_id = []
    order_id = []
    burger = []
    side = []
    drink = []



print_catalogue()
another = "yes"
while another == "yes":
    order = place_order()
    asyncio.run(check_stock(order_id))
    add_burger_dic("Burgers", burger_id, burger)
    add_side_dic(side_id, side)
    add_drink_dic(drink_id, drink)
    sort_by_price(burger)
    sort_by_price(drink)
    sort_by_price(side)
    make_combos(burger, side, drink)
    print_order(burger, side, drink)
    again = print_price(total_price)
    if again == "stop":
        break
    another = input("Would you like to make another order (yes/no)?")
    if another == "yes":
        print("\n")
        reset()
    else:
        print("Goodbye!")
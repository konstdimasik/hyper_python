import random


def main():
    entry_quantity = input("Enter the number of friends joining (including you):\n")
    friends = {}
    try:
        quantity = int(entry_quantity)
    except ValueError:
        print("No one is joining for the party")
        exit()
    if quantity < 1:
        print("No one is joining for the party")
        exit()
    else:
        print("\nEnter the name of every friend (including you), each on a new line:")
        for _ in range(quantity):
            name = input()
            friends[name] = 0

    entry_bill = input("\nEnter the total bill value:\n")
    try:
        bill = float(entry_bill)
    except ValueError:
        print("Total bill please")
        exit()
    equal_share = round(bill / quantity, 2)
    for name in friends:
        friends[name] = equal_share

    entry_lucky = input('\nDo you want to use the "Who is lucky?" feature? Write Yes/No:\n')
    if entry_lucky != "Yes":
        print("\nNo one is going to be lucky")
        print(friends)
        exit()
    else:
        lucky_one = random.choice(list(friends.keys()))
        print(f"\n{lucky_one} is the lucky one")
        new_equal_share = round(bill / (quantity - 1), 2)
        for name in friends:
            friends[name] = new_equal_share
        friends[lucky_one] = 0

        print(friends)


if __name__ == '__main__':
    main()

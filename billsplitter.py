def main():
    quantity = int(input("Enter the number of friends joining (including you):\n"))
    friends = {}
    if quantity < 1:
        print("No one is joining for the party")
        return
    else:
        print("\nEnter the name of every friend (including you), each on a new line:")
        for _ in range(quantity):
            name = input()
            friends[name] = 0
    print()
    print(friends)


if __name__ == '__main__':
    main()

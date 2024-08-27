def display_menu():
    print("What Game are you using\n Please select an option:")
    print("1. Dual universe")
    print("2. Option 2")
    print("3. Option 3")
    print("4. Exit")


def get_user_choice():
    choice = input("Enter your choice (1-4): ")
    return choice


def dual_universe():
    from dual_universe.src.querysets import CharacterQuerySet, MissionQuerySet

    # write to db
    missions = MissionQuerySet.select_all_missions()
    for mission in missions:
        print(mission)
    pilot_name = input("Enter Mission: ").lower().strip()

    characters = CharacterQuerySet.select_all_characters()
    for character in characters:
        print(character)
    pilot_name = input("Enter Character's to use: ").lower().strip()

    pilot_name = input("Enter Pilot name: ").lower().strip()


def main():
    while True:
        display_menu()
        choice = get_user_choice()
        if choice == "1":
            print("You selected Option 1")
            dual_universe()
        elif choice == "2":
            print("You selected Option 2")
        elif choice == "3":
            print("You selected Option 3")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

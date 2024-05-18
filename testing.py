def take_notes():
    topic = input("Enter the topic: ")
    notes = ""
    print("Start taking notes. When you're done, type 'end_notes' to finish.")
    while True:
        note = input("Note: ")
        if note.lower() == "end_notes":
            break
        notes += note + "\n"
    save_notes_to_file(topic, notes)

def make_list():
    topic = input("Enter the topic: ")
    items = []
    print("Start making the list. When you're done, type 'end_list' to finish.")
    while True:
        item = input("List item: ")
        if item.lower() == "end_list":
            break
        items.append(item)
    save_list_to_file(topic, items)

def save_notes_to_file(topic, notes):
    file_name = topic.replace(" ", "_") + "_notes.txt"
    with open(file_name, "w") as file:
        file.write(notes)
    print("Notes saved to file:", file_name)

def save_list_to_file(topic, items):
    file_name = topic.replace(" ", "_") + "_list.txt"
    with open(file_name, "w") as file:
        for item in items:
            file.write(item + "\n")
    print("List saved to file:", file_name)

def main():
    while True:
        choice = input("What do you want to do? (1: Take notes, 2: Make a list, 3: Exit): ")
        if choice == "1":
            take_notes()
        elif choice == "2":
            make_list()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()

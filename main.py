import user_input

def main():
    command = user_input.init()
    if command.classify:
        user_input.classify_data()

    if command.migrate:
        user_input.import_data()

    if command.plot:
        user_input.plot_data()

if __name__ == "__main__":
    main()

from src.generator import generate_tweet

if __name__ == "__main__":
    names_generated = 0
    try:
        while True:
            print(generate_tweet()[0])
            names_generated += 1
            input(
                "\033[90mPress enter to generate a new city (CTRL + C to quit)\033[0m"
            )
    except KeyboardInterrupt:
        print(
            f"\n\nYou generated {names_generated} "
            f"{'city' if names_generated <= 1 else 'cities'} "
            f"- See you soon!\n"
        )

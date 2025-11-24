from src.generator import generate_tweet

if __name__ == "__main__":
    while True:
        print(generate_tweet()[0])
        input("\033[90mPress enter to generate a new city (CTRL + C to quit)\033[0m")

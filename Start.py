from Display import Display

def main():
    try:
        display = Display()
        display.start()
    except Exception as ex:
        print("Error starting the game:", ex)

if __name__ == "__main__":
    main()

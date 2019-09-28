# main file.
# This file is run after boot.py.


def main(counter=0):
    """main"""
    import shelfie
    print("preparing to listen.")
    try:
        shelfie.listen()
    except OSError:
        if counter <= 10:
            print("Error... reconnecting...")
            main(counter+1)
        else:
            print("Rebooting system due to too many connection failures.")
            import machine
            machine.reset()
    except KeyboardInterrupt:
        raise
    else:
        print("Exitting")

if __name__ == "__main__":
    main()

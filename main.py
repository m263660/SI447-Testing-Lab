# main.py
from server_model import ServerModel

def main():
    
    # Instance of ServerModel
    server = ServerModel("http://lnx1073302govt:8000")  

    # User interaction
    print("~~ MidsQuest ~~")
    print("1. Sign up   2. Log in")
    choice = input("> ")
    
    # Sign up 
    if choice == "1":
        u = input("Username: ")
        p = input("Password: ")
        if server.sign_up(u, p):
            print("Signed up – now log in")
        else:
            print("Sign-up failed")
            return

    # Login
    u = input("Username: ")
    p = input("Password: ")
    try:
        server.login(u, p)
        print("Logged in")
    except Exception as e:
        print(e)
        return

    # List of available commands
    print("\nCommands: n/s/e/w, look, doing <action>, use <item>, quit")

    # Game loop that process commands and interacting with API using the Server Model
    while True:

        # User input
        cmd = input("> ").strip().lower()

        # Quit
        if cmd == "quit":
            break

        # Directions
        elif cmd in ("n", "s", "e", "w"):
            dmap = {"n":"north","s":"south","e":"east","w":"west"}
            try:
                print(server.move(dmap[cmd]))
            except Exception as e: print(e)

        # Look Around
        elif cmd == "look":
            try:
                d = server.look()
                print(d["description"])
                if d.get("players"):
                    print("Players here:")
                    for p in d["players"]:
                        print(f" - {p['name']} is {p['action']}")
            except Exception as e: print(e)
        
        # Sets Action
        elif cmd.startswith("doing "):
            try:
                print(server.doing(cmd[6:]))
            except Exception as e: print(e)
        
        # Uses Item
        elif cmd.startswith("use "):
            try:
                print(server.use(cmd[4:]))
            except Exception as e: print(e)

        # If command is invalid
        else:
            print("unknown command")

# Checks is script is run directly
if __name__ == "__main__":
    main()
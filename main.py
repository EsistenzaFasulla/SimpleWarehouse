import sqlite3,string,random,getpass

username_logged = False; password_logged = False


class colors:
    HEADER = '\033[95m'
    LIGHTGRAY = '\033[97m'
    BLUE = '\033[94m'
    LIGHTPURPLE = '\033[94m'
    PURPLE = '\033[95m'
    BLACK = '\033[98m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def menu():
    global username_logged;global password_logged
    if password_logged:
        db = sqlite3.connect("data.db"); c = db.cursor()
        ask_action = input("What action do you wish to take? (CHECK; ADD; REMOVE; EDIT USERNAME PASSWORD; LOG OUT; EXIT) >> ").lower()
        if ask_action == "check": # check items in warehouse
            while True:
                spongebob = ""
                warehouse_list = c.execute(f"select id,name,quantity from warehouse").fetchall()
                if warehouse_list:
                    for x in warehouse_list:
                        spongebob += f"{x[0]} - {x[1]} (x{x[2]})\n"
                else:
                    spongebob = f"{colors.FAIL}No items into warehouse found.{colors.ENDC}"
                check_action = input(f"OK, what would you like to check into warehouse? (or just press the enter key to return to the menu) \n\n\n{spongebob}\n\n>> ").upper()
                if check_action == "":
                    print(f"{colors.GREEN}All right, I’m gonna go ahead and get you back on the menu.{colors.ENDC}")
                    return menu()
                found = c.execute(f"select id,name,quantity from warehouse where id='{check_action.upper()}'").fetchone()
                if found:
                    print(f"Existing product, here is to you sir the info:\n\nID: {found[0]}\nNAME: {found[1]}\nQUANTITY: {found[2]}\n\n")
                else:
                    print(f"{colors.FAIL}No product, please try again.{colors.ENDC}")
        elif ask_action == "add": # add item or quantity of the item
            while True:
                add_action = input("OK, what do you want to add into warehouse? (or just press the enter key to return to the menu) >> ").upper()
                if add_action == "":
                    print(f"{colors.GREEN}All right, I’m gonna go ahead and get you back on the menu.{colors.ENDC}")
                    return menu()
                exists = c.execute(f"select id,name,quantity from warehouse where id='{add_action}'").fetchone()
                if exists:
                    try:
                        quantity_ask = int(input(f"How many of the articles you want to add {exists[0]} [{exists[1]}]? (x{exists[2]}) >> "))
                    except ValueError:
                        print(f"{colors.FAIL}Error found, you can't send a string instead of int value.{colors.ENDC}")
                    finally:
                        print(f"{colors.FAIL}Retry!{colors.ENDC}")
                    c.execute(f"update warehouse set quantity=quantity+{quantity_ask} where id='{exists[0]}'")
                    db.commit()
                    print(f"{colors.GREEN}Correctly added +{quantity_ask} of {add_action} ({exists[1]}).{colors.ENDC}")
                else:
                    random_id = ''.join(random.choice(f"{string.ascii_letters}0123456789") for x in range(6)).upper()
                    try:
                        quantity_ask = int(input(f"Quantity? >> "))
                    except ValueError:
                        print(f"{colors.WARNING}Error found, you can't send a string instead of int value.{colors.ENDC}")
                    finally:
                        print(f"{colors.FAIL}Retry!{colors.ENDC}")
                    c.execute(f"insert into warehouse values('{random_id}', '{add_action}', {quantity_ask})")
                    db.commit()
                    print(f"{colors.GREEN}Correctly created {random_id} [{add_action}] w/ x{quantity_ask}!{colors.ENDC}")
        elif ask_action.lower() == "remove": # remove quantity of the item or the item
            while True:
                remove_action = input("Enter the item id to be removed. (or just press the enter key to return to the menu) >> ").upper()
                if remove_action == "":
                    print(f"{colors.GREEN}All right, I’m gonna go ahead and get you back on the menu.{colors.ENDC}")
                    return menu()
                exists = c.execute(f"select id,name from warehouse where id='{remove_action}'").fetchone()
                if exists:
                    try:
                        selection = int(input("Write '0' if you wanna delete this item, '1' if u just wanna remove some quantity. >> "))
                    except ValueError:
                        print(f"{colors.WARNING}Error found, you can't send a string instead of int value.{colors.ENDC}")
                    finally:
                        print(f"{colors.FAIL}Retry!{colors.ENDC}")
                    if selection == 0:
                        c.execute(f"delete from warehouse where id='{remove_action}'")
                        db.commit()
                        print(f"{colors.GREEN}Item deleted!{colors.ENDC}")
                    else:
                        howmuch = str(input(f"Agree, how much quantity do you want to remove from the article {exists[0]} [{exists[1]}]?"))
                        c.execute(f"update warehouse set quantity=quantity-{howmuch} where id='{exists[0]}'")
                        db.commit()
                        print(f"{colors.GREEN}Correctly removed {howmuch} from {exists[0]} [{exists[1]}]{colors.ENDC}")
        elif ask_action.lower() == "edit username password": # change your username/password
            ask_new_username = input("New username (or just press the enter key to return to the menu) >> ")
            if ask_new_username == "":
                print(f"{colors.GREEN}All right, I’m gonna go ahead and get you back on the menu.{colors.ENDC}")
                return menu()
            ask_new_password = getpass.getpass("New password (or just press the enter key to return to the menu) >> ")
            if ask_new_password == "":
                c.execute(f"update login set username='{ask_new_username}'")
                db.commit()
                print(f"{colors.GREEN}Correctly changed username.{colors.ENDC}")
                print(f"{colors.GREEN}All right, I’m gonna go ahead and get you back on the menu.{colors.ENDC}")
                return menu()
            c.execute(f"update login set username='{ask_new_username}', password='{ask_new_password}'")
            db.commit()
            print(f"{colors.GREEN}Correctly changed username and password, ill log out you rn!{colors.ENDC}")
            username_logged = False; password_logged = False
            db.close()
            return start_function()
        elif ask_action.lower() == "log out" or ask_action.lower() == "logout": # log out
            username_logged = False; password_logged = False
            db.close()
            return start_function()
        elif ask_action.lower() == "exit" or ask_action.lower() == "leave": # exit program
            print(f"\n\n{colors.ORANGE}Goodbye!{colors.ENDC}")
            return;
        db.close()

def start_function():
    global username_logged; global password_logged
    print(f"\n\n{colors.BLUE}Welcome in my simple warehouse software!\n\n{colors.GREEN}Credits: {colors.CYAN} Antonello D. ~ (made with love and piadina){colors.ENDC}\n\n")
    db = sqlite3.connect("data.db"); c = db.cursor()
    credenziali = c.execute(f"select username,password from login").fetchone()
    while True:
        if not username_logged:
            username_login = input("Enter your username >> ")
        if username_login == credenziali[0] or username_logged:
            # correct
            username_logged = True
            if not password_logged:
                password_login = getpass.getpass('Enter your password >> ')
            if password_login == credenziali[1] or password_logged:
                # correct
                password_logged = True
                print(f"{colors.GREEN}Correctly joined into warehouse!{colors.ENDC}")
                break;
            else:
                # wrong
                print(f"{colors.FAIL}Password invalid, try again!{colors.ENDC}")
        else:
            # wrong
            print(f"{colors.FAIL}Username invalid, try again!{colors.ENDC}")
    db.close()
    return menu()




start_function()
import mysql.connector


def mostrar_menu_login(bd):
    print("======== Thorbe Systems ========")
    print("[                              ]")
    print("[     1· Sign in               ]")
    print("[     2· Log in                ]")
    print("[     3· Exit                  ]")
    print("[                              ]")
    print("================================")
    i = input("Selet an option (number of list): ")
    if i == "1":
        username = input("Username: ")
        passwd = input("Password: ")
        permited = logIn(username, passwd, bd)
        if permited:
            mostrar_menu_inicio()
        else:
            mostrar_menu_login(bd)

    elif i == "2":
        newUser(bd)
        mostrar_menu_login(bd)

    elif i == "3":
        print("Nos vemos!")

    else:
        mostrar_menu_login(bd)


def mostrar_menu_inicio():
    print("======== Thorbe  Systems ========")
    print("[                               ]")
    print("[     1· Sell lemonade          ]")
    print("[     2· Order ingredients      ]")
    print("[     3· Make lemonade          ]")
    print("[     4· Accounting             ]")
    print("[     5· Exit                   ]")
    print("[                               ]")
    print("================================")
    i = int(input("Selet an option (number of list): "))
    return i


def create_connection(ip, nombre):
    mydb = mysql.connector.connect(
        host=ip,
        user="root",
        passwd="",
        database=nombre
    )
    return mydb


def user_exists(micursor, username):
    micursor.execute("SELECT userName FROM `users`")
    repetido = False
    listUsers = micursor.fetchall()
    for res in listUsers:
        res = str(res).replace("('", "")
        res = res.replace("',)", "")

        if str(res) == str(username):
            print("Sorry, user already registered.")
            repetido = True

    return repetido


def newUser(bd):
    micursor = bd.cursor()
    repetido = True
    while repetido:
        username = input("Insert a username: ")
        repetido = user_exists(micursor, username)

    pwd = input("Insert a password: ")
    micursor.execute("INSERT INTO `users`(`userName`, `passwd`) VALUES ('{}','{}')".format(username, pwd))
    bd.commit()
    print("Welcome to the system {}!".format(username))


def logIn(username, pwd, bd):
    micursor = bd.cursor()
    micursor.execute("SELECT passwd FROM `users` WHERE userName=\"{}\"".format(username))
    stored_pwd = micursor.fetchall()[0]
    if "('{}',)".format(pwd) == str(stored_pwd):
        print("Successfully logged")
        return True
    else:
        print("The password is not correct. Please try again.")
        return False


def make_lemondae(liters, bd):
    li = int(liters)
    micursor = bd.cursor()
    micursor.execute("UPDATE `products` SET `total_amount`=`total_amount`+{} WHERE 1".format(li))
    bd.commit()


def sell_lemondae(liters, bd):
    r = remaining_lemonade(bd)
    li = int(liters)
    if li > r or r == 0:
        print("Sorry, there's only {}L left".format(r))
    else:
        micursor = bd.cursor()
        micursor.execute("UPDATE `products` SET `total_amount`=`total_amount`-{} WHERE 1".format(li))
        bd.commit()
        print("Transaction complete.")


def remaining_lemonade(bd):
    micursor = bd.cursor()
    micursor.execute("SELECT total_amount FROM `products` WHERE 1")
    remains = str(micursor.fetchall()[0]).replace("(", "")
    remains = remains.replace(",)", "")
    return int(remains)


def remaining_products(bd):
    micursor = bd.cursor()
    micursor.execute("SELECT * FROM `products`")
    remains = micursor.fetchall()
    return remains


mydb = create_connection("localhost", "lemondb")
mostrar_menu_login(mydb)

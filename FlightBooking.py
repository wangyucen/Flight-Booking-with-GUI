from tkinter import *
from tkinter import messagebox
from turtle import bgcolor
from tkcalendar import Calendar
from random import randint
from tkinter import ttk
import datetime
import re
ticketCnt = 0
root = Tk()
root.geometry("500x500")
originCity = ['London', 'Peking', 'Budapest', 'Paris', 'Tokyo']
destinationCity = ['London', 'Peking', 'Budapest', 'Tokyo']


class Customer:
    def __init__(self, name="Guest", email=None, password=None, gender=None):
        self.gender = gender
        self.name = name
        self.email = email
        self.password = password
        self.tickets = {}


class Ticket:

    def __init__(self, name, email, type, dep_date, quantity, originCity, destinationCity, ticketNumber):
        self.ticketNumber = ticketNumber
        self.name = name
        self.email = email
        self.type = type
        self.dep_date = dep_date
        self.quantity = quantity
        self.originCity = originCity
        self.destinationCity = destinationCity


def createNewBookingClicked():
    bookingWindow = Toplevel(root)
    bookingWindow.title("Booking Tickets")
    bookingWindow.geometry("440x500")
    bookingWindow.grab_set()
    Label(bookingWindow,
          text="Booking Online", font="Times 20 italic bold").grid(row=0, column=1)
    # classes
    classType = StringVar()
    classType.set(-1)

    Radiobutton(bookingWindow, text='First', variable=classType, value="First", font=("Times 13 italic bold")).grid(
        row=1, column=0)
    Radiobutton(bookingWindow, text='Business', variable=classType, value="Business",
                font=("Times 13 italic bold")).grid(row=1, column=1)
    Radiobutton(bookingWindow, text='Economic', variable=classType, value="Economic",
                font=("Times 13 italic bold")).grid(row=1, column=2)
    # cities
    Label(bookingWindow, text='Origin City: ', font=("Times 13 italic bold")).grid(row=2, column=0, sticky=W, pady=10)
    Label(bookingWindow, text='Destination City: ', font=("Times 13 italic bold")).grid(row=3, column=0, sticky=W)
    selected_origin = StringVar()
    ori = ttk.Combobox(bookingWindow, textvariable=selected_origin, values=originCity, state='readonly').grid(row=2,
                                                                                                              column=1,
                                                                                                              sticky=W)
    selected_dest = StringVar()
    dest = ttk.Combobox(bookingWindow, textvariable=selected_dest, values=destinationCity, state='readonly')
    dest.grid(row=3, column=1, sticky=W)
    # quantity
    quan = Spinbox(bookingWindow, from_=1, to=20)
    Label(bookingWindow, text='Quantity: ', textvariable=quan, font=("Times 13 italic bold")).grid(row=4, column=0,
                                                                                                   sticky=W, pady=10)
    quan.grid(row=4, column=1, sticky=W)
    # date
    current_date = datetime.date.today()
    cal = Calendar(bookingWindow, selectmode='day', bgcolor="#F6F6F6")
    cal.grid(row=5, column=1, padx=20, pady=10)
    dep_date = cal.get_date()

    def my_upd():  # triggered on Button Click
        nonlocal dep_date
        temp = cal.get_date()
        chosen_date = datetime.datetime.strptime(temp, '%m/%d/%y').date()
        if chosen_date < current_date:
            messagebox.showerror(title=None, message="Invalid date")
        else:
            dep_date = cal.get_date()
            messagebox.showinfo("Date", dep_date + ' selected')

    b1 = Button(bookingWindow, text='confirm date', command=lambda: my_upd(), font=("Times 13 italic bold"))
    b1.grid(row=6, column=1)

    # submit
    def submit():
        global currentUser
        if selected_origin.get() == selected_dest.get() and selected_dest.get() != '' and selected_origin.get() != '':
            messagebox.showwarning(title=None,
                                   message="The destination city and the origin city should not be the same!")
        elif selected_dest.get() == '' or selected_origin.get() == '':
            messagebox.showwarning(title=None, message="Empty field detected!")
        else:
            global ticketCnt
            ticketCnt += 1
            newTicket = Ticket(currentUser.name, currentUser.email, classType.get(), dep_date, quan.get(),
                               selected_origin.get(),
                               selected_dest.get(), ticketCnt)

            subMessage = 'Dear customer! you have purchased ' + str(
                quan.get()) + ' ' + classType.get() + ' Tickets, from ' + selected_origin.get() + ' to ' + selected_dest.get() + '\n'
            dateMessage = 'Depature date is :' + dep_date + '\n'
            if classType.get() == 'First':
                price = randint(8000, 10000)
            elif classType.get() == "Business":
                price = randint(5000, 8000)
            elif classType.get() == "Economic":
                price = randint(2000, 5000)
            try:
                priceMessage = 'Total Cost is :' + str(price * int(quan.get())) + ' $ (' + str(
                    price) + ' * ' + quan.get() + ' )'
            except UnboundLocalError:
                messagebox.showwarning(title=None,
                                       message="Please select a proper class")
            res = messagebox.askquestion('submission details', subMessage + dateMessage + priceMessage,
                                         parent=bookingWindow)
            if res == 'yes':
                currentUser.tickets[newTicket] = price * int(quan.get())
                bookingWindow.destroy()
            else:
                messagebox.showinfo('Return', 'Returning to main application')

    Button(bookingWindow, text="purchase",
           command=submit, font=("Times 13 italic bold"), bg='grey').grid(column=1, row=8, sticky=S, pady=50)


def deleteBookingClicked():
    global currentUser
    deleteBookingWindow = Toplevel(root)
    deleteBookingWindow.title("Delete Booking")
    deleteBookingWindow.geometry("250x150")
    deleteBookingWindow.grab_set()
    Label(deleteBookingWindow, text="Ticket number to delete: ", padx=40, pady=15).grid(row=0, column=0)
    deletion = IntVar()
    Entry(deleteBookingWindow, textvariable=deletion).grid(row=1, column=0)

    def delete():
        li = list()
        for de in currentUser.tickets.keys():
            li.append(de.ticketNumber)
        if int(deletion.get()) not in li:
            messagebox.showwarning(title=None, message="The Ticket Number you entered not found!")
        else:
            for ticket in currentUser.tickets.keys():
                if ticket.ticketNumber == deletion.get():
                    del currentUser.tickets[ticket]
                    messagebox.showwarning(title=None, message="Deletion successful!!")

    Button(deleteBookingWindow, text="Delete",
           command=delete, font=("Times 13 italic bold")).grid(row=2, column=0)


def viewHistoryBookingClicked():
    global currentUser
    historyBookingWindow = Toplevel(root)
    historyBookingWindow.title("Bookings")
    historyBookingWindow.geometry("800x300")
    historyBookingWindow.grab_set()
    hist = Scrollbar(historyBookingWindow)
    hist.pack(side=RIGHT, fill=Y)
    mylist = Listbox(historyBookingWindow, yscrollcommand=hist.set, width=200, height=200)
    mylist.insert(END, '-------------Purchase History-------------')
    for line in currentUser.tickets.keys():
        mylist.insert(END, 'Ticket Number : ' + str(line.ticketNumber) + ' Ticket Type: ' + str(
            line.type) + ' || Dep Date: ' + line.dep_date + ' || Quantity: ' + line.quantity + ' || From ' + line.originCity + ' To ' + line.destinationCity + " || Total Cost: " + str(
            currentUser.tickets[line]))
    mylist.pack(side=LEFT, fill=BOTH)
    hist.config(command=mylist.yview)


def signinClicked(root, signinButton,registerButton):
    global currentUser
    signinWindow = Toplevel(root)
    signinWindow.title("Sign In")
    signinWindow.geometry("400x200")
    signinWindow.grab_set()
    email = StringVar()
    password = StringVar()
    signinWindow.grid_columnconfigure(1, minsize=15)
    Label(signinWindow, text="Email: ", padx=20, pady=15).grid(row=0, column=0)
    Label(signinWindow, text="Password: ", padx=20, pady=15).grid(row=1, column=0)
    Entry(signinWindow, textvariable=email).grid(row=0, column=2)
    Entry(signinWindow, show="*", textvariable=password).grid(row=1, column=2)
    Button(signinWindow, text="Enter",
           command=lambda: checkDetails(root, signinWindow, signinButton,registerButton, email.get(), password.get())).grid(row=2,
                                                                                                             column=2)

def registerClicked():
    global currentUser
    registerWindow = Toplevel(root)
    registerWindow.title("Register")
    registerWindow.geometry("300x160")
    registerWindow.grab_set()
    email = StringVar()
    password = StringVar()
    name = StringVar()
    # Label(registerWindow, text="Please enter your information below: ", padx=20, pady=15).grid(row=0)
    Label(registerWindow, text="Name: ").grid(row=0, column=0,sticky=W)
    Label(registerWindow, text="Email: ").grid(row=1, column=0,sticky=W)
    Label(registerWindow, text="Password: ").grid(row=2, column=0,sticky=W)
    Entry(registerWindow, textvariable=name).grid(row=0, column=1, sticky=W)
    Entry(registerWindow, textvariable=email).grid(row=1, column=1,sticky=W)
    Entry(registerWindow, show="*", textvariable=password).grid(row=2, column=1,sticky=W)
    genderType = StringVar()
    genderType.set(-1)
    Radiobutton(registerWindow, text='male', variable=genderType, value="male").grid(
        row=3, column=0)
    Radiobutton(registerWindow, text='female', variable=genderType, value="female"
               ).grid(row=3, column=1)

    def register():
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+(\.[a-z]{1,3})+$"
        if name.get() == '' or email.get() == '' or password.get() == '' or genderType.get() == -1:
            messagebox.showwarning(title=None, message="blank field detected! ")
        elif not name.get().isalpha():
            messagebox.showwarning(title=None, message="user name can only contain letters! ")
        elif email.get() in customers.keys():
            messagebox.showwarning(title=None, message="The email address you used is already taken! ")
        elif not re.match(pat,email.get()):
            messagebox.showwarning(title=None, message="The email address you entered is not a valid one! ")
        else:
            customer = Customer(name.get(),email.get(),password.get(),genderType.get())
            customers[email.get()] = customer
            print(customers.keys())
            messagebox.showinfo(None, 'Customer registration successful')
            registerWindow.destroy()

    Button(registerWindow, text="Register",
           command=register, font=("Times 8 italic bold")).grid(row=4, column=1)

def checkDetails(root, signinWindow, signinButton,registerButton,email, password):
    global currentUser
    if len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title=None, message="Invalid input")
    elif email in customers:
        if customers[email].password == password:
            currentUser = customers[email]
            signinWindow.destroy()
            signinButton.destroy()
            registerButton.destroy()
            if currentUser.gender == 'male':
                Label(root, text=f"Welcome Mr {currentUser.name}!", pady=80).pack()
            elif currentUser.gender == 'female':
                Label(root, text=f"Welcome Ms {currentUser.name}!", pady=80).pack()

        else:
            messagebox.showwarning(title=None, message="Incorrect email/password")

    else:
        messagebox.showwarning(title=None, message="Incorrect email/password")


def displayAccount():
    global currentUser
    accountWindow = Toplevel(root)
    accountWindow.title("Account Details")
    accountWindow.geometry("400x150")
    accountWindow.grab_set()
    if currentUser.name == "Guest":
        Label(accountWindow, text="     ", padx=20, pady=15).grid(row=0, column=0)
        Label(accountWindow, text="Guest account\n Please log in to see full information", padx=20, pady=15).grid(row=0,
                                                                                                                  column=1)
    else:
        Label(accountWindow, text=f"Name: ", padx=20, pady=15).grid(row=0, column=0)
        Label(accountWindow, text=f"Email: ", padx=20, pady=15).grid(row=1, column=0)
        Label(accountWindow, text=f"Gender: ", padx=20, pady=15).grid(row=2, column=0)
        Label(accountWindow, text=currentUser.name, padx=20, pady=15).grid(row=0, column=1)
        Label(accountWindow, text=currentUser.email, padx=20, pady=15).grid(row=1, column=1)
        Label(accountWindow, text=currentUser.gender, padx=20, pady=15).grid(row=1, column=1)
        Button(accountWindow, text="Change Password", command=changePassword, font="Times 13 italic bold").grid(row=2,
                                                                                                                column=1)


def changePassword():
    global currentUser
    passwordWindow = Toplevel(root)
    passwordWindow.title("Change Password")
    passwordWindow.geometry("400x150")
    passwordWindow.grab_set()
    oldPass = StringVar()
    newPass = StringVar()
    Label(passwordWindow, text="Old Password: ", padx=5, pady=15).grid(row=0, column=0)
    Label(passwordWindow, text="New Password: ", padx=5, pady=15).grid(row=1, column=0)
    Entry(passwordWindow, show="*", textvariable=oldPass).grid(row=0, column=2)
    Entry(passwordWindow, show="*", textvariable=newPass).grid(row=1, column=2)
    Button(passwordWindow, text="Enter", command=lambda: checkPassword(oldPass, newPass, passwordWindow),
           font="Times 13 italic bold").grid(row=2, column=1)


def checkPassword(oldPass, newPass, passwordWindow):
    global currentUser
    if currentUser.password == oldPass.get() and oldPass.get() != newPass.get() and len(newPass.get()) != 0:
        currentUser.password = newPass.get()
        messagebox.showwarning(title=None, message="Password Changed Successfully")
        passwordWindow.destroy()
    elif oldPass.get() == newPass.get():
        messagebox.showwarning(title=None, message="New Password May Not Be Identical To Old Password")
    else:
        messagebox.showwarning(title=None, message="Incorrect Password")


def displayMain(currentUser):
    frame = Frame(root)
    frame.pack()

    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='Bookings', menu=filemenu)
    # create new Booking
    filemenu.add_command(label='Create New Booking', command=lambda: createNewBookingClicked())
    # delete existing booking
    filemenu.add_command(label='Delete Booking', command=deleteBookingClicked)
    filemenu.add_separator()
    filemenu.add_command(label="View Bookings", command=lambda: viewHistoryBookingClicked())
    usermenu = Menu(menu)
    menu.add_cascade(label='Account', menu=usermenu)
    usermenu.add_command(label='View Account Details', command=lambda: displayAccount())
    windowmenu = Menu(menu)
    menu.add_cascade(label='Window', menu=windowmenu)
    windowmenu.add_command(label='Close', command=root.quit)

    root.title("Flight Booking")
    message = "Welcome to JP Morgan airlines!"
    welcomeMessage = Label(frame, text=message)
    welcomeMessage.pack()

    canvas = Canvas(frame, bg="#ECECEC", width=250, height=136)
    canvas.pack(pady=100)
    welcomeImage = PhotoImage(file="plane.png")
    canvas.create_image(0, 0, image=welcomeImage, anchor=NW)

    exitButton = Button(frame, text='Exit', command=root.quit, font="Times 13 italic bold",pady=10)
    exitButton.pack(side=BOTTOM)
    registerButton = Button(frame, text='Register', font="Times 13 italic bold",pady=10,command= registerClicked)
    registerButton.pack(side=BOTTOM)
    signinButton = Button(frame, text='Sign in', command=lambda: signinClicked(root, signinButton,registerButton),
                          font="Times 13 italic bold",pady=10)
    signinButton.pack(side=BOTTOM)

    root.mainloop()


test = Customer("Andrei Cojocariu", "andrei85@", "pass")
customers = {"andrei85@": test}

currentUser = Customer()
displayMain(currentUser)

from tkinter import *
import customtkinter as ctk
from PIL import Image
import mysql.connector as mysql
import re

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
# login page
root = ctk.CTk()
root.geometry("700x450")
root.title("BankManagementSystem")
email_reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'  # email authenticity checker

title_label = ctk.CTkLabel(root, text="Bank Management System", font=('Eras Demi ITC', 34, 'bold'))
title_label.pack(padx=100, pady=(10, 30))
con = mysql.connect(user='root', password='anurag10', host='localhost')
if con.is_connected():
    print("connected")
    cursor = con.cursor()
    cursor.execute('create database if not exists project1;')
    cursor.execute('use project1;')
    query1 = ("create table if not exists new_details(ACCOUNT_ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,NAME varchar("
              "50) NOT NULL, AGE int NOT NULL, GENDER Varchar(2) NOT NULL,PHONE_NUMBER BIGINT, EMAIL varchar(50), "
              "PASSWORD varchar(50) NOT NULL , BALANCE int Default 5000);")
    history1 = ("create table if not exists trans_history(Account_sender int NOT NULL ,NAME_rec varchar(50) NOT NULL,"
                "Account_rec int NOT NULL,TRANSFERED_AMT int NOT NULL,Balance_before int NOT NULL,BALANCE_after int "
                "NOT NULL,TRANS_TYPE varchar(20) Default 'AMOUNT DEBITED');")
    history2 = ("create table if not exists rec_history(acc_of_receiver int NOT NULL ,name_of_sender varchar(50) NOT "
                "NULL,Account_sender int NOT NULL,TRANSFERED_AMT int NOT NULL,Balance_before int NOT NULL,"
                "BALANCE_after int NOT NULL,TRAN_TYPE varchar(20) Default 'AMOUNT CREDITED')")
    cursor.execute(query1)
    cursor.execute(history1)
    cursor.execute(history2)


    def login():
        global login_page
        global tempo_serial
        global tempo_password
        global msg

        login_page = Toplevel(root)  # creating a window on top of all other windows
        login_page.title("login")
        login_page.geometry("800x500")
        login_page.configure(background='#1a1a1a')

        tempo_serial = StringVar()
        tempo_password = StringVar()

        title_label = ctk.CTkLabel(login_page, text="Login", font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))

        label1 = ctk.CTkLabel(login_page, text="Enter Account Number ", font=('Eras Demi ITC', 23, 'bold'))
        label1.place(x=180, y=100)
        e1 = ctk.CTkEntry(login_page, width=250, textvariable=tempo_serial)
        e1.place(x=180, y=130)
        label2 = ctk.CTkLabel(login_page, text="Enter Password ", font=('Eras Demi ITC', 23, 'bold'))
        label2.place(x=180, y=175)
        e2 = ctk.CTkEntry(login_page, width=250, textvariable=tempo_password, show='*')
        e2.place(x=180, y=205)
        b1 = ctk.CTkButton(login_page, text="Submit", font=('Eras Demi ITC', 20, 'bold'), command=login2)
        b1.place(x=140, y=245)
        b2 = ctk.CTkButton(login_page, text="Forgot Password", font=('Eras Demi ITC', 20, 'bold'),
                           command=forgot_password)
        b2.place(x=330, y=245)
        msg = ctk.CTkLabel(login_page, text="", font=('Eras Demi ITC', 20, 'bold'))
        msg.place(x=180, y=320)


    def login2():

        global passwrd
        global acc_no
        global serial_no
        global passw
        global check
        global name

        name = StringVar()
        serial_no = int(tempo_serial.get())
        passw = tempo_password.get()
        query2 = "select * from new_details;"
        cursor.execute(query2)
        data = cursor.fetchall()
        check = 0

        for i in data:
            acc_no = i[0]
            passwrd = i[6]
            name = i[1]

            if acc_no == serial_no and passwrd == passw:
                check += 1
                break
        if check == 1:
            global dash
            print("Account found")
            msg.configure(fg_color='#12e632', text='Login Successful')
            login_page.destroy()
            dash = Toplevel(root)
            dash.geometry("1000x600")
            dash.title("Main Menu")
            dash.configure(background='#1a1a1a')
            title_label = ctk.CTkLabel(dash, text="Bank Management System", font=('Eras Demi ITC', 34, 'bold'))
            title_label.pack(padx=100, pady=(10, 30))
            buttonframe = ctk.CTkFrame(dash)
            buttonframe.columnconfigure(0, weight=1)
            buttonframe.columnconfigure(1, weight=1)

            btn1 = ctk.CTkButton(buttonframe, text="Transfer Money", font=('Eras Demi ITC', 20), width=200,
                                 command=transfer)
            btn1.grid(row=0, column=0, padx=10, pady=10)

            btn2 = ctk.CTkButton(buttonframe, text="Account Details",
                                 font=('Eras Demi ITC', 20), width=200, command=acc_details)
            btn2.grid(row=0, column=1, padx=10, pady=10)

            btn3 = ctk.CTkButton(buttonframe, text="Withdraw Money", font=('Eras Demi ITC', 20), width=200,
                                 command=withdraw1)
            btn3.grid(row=1, column=0, padx=10, pady=10)

            btn4 = ctk.CTkButton(buttonframe, text="Deposit Money", font=('Eras Demi ITC', 18), width=200,
                                 command=deposit1)
            btn4.grid(row=1, column=1, padx=10, pady=10)

            btn5 = ctk.CTkButton(buttonframe, text="Update Details", font=('Eras Demi ITC', 18), width=200,
                                 command=Update_details)
            btn5.grid(row=2, column=0, padx=10, pady=10)

            btn6 = ctk.CTkButton(buttonframe, text="Transfer History", font=('Eras Demi ITC', 18), width=200,
                                 command=history)
            btn6.grid(row=2, column=1, padx=10, pady=10)

            btn7 = ctk.CTkButton(buttonframe, text="Change Password", font=('Eras Demi ITC', 18), width=200,
                                 command=forgot_password)
            btn7.grid(row=3, column=0, padx=10, pady=10)

            btn8 = ctk.CTkButton(buttonframe, text="Sign Out", font=('Eras Demi ITC', 20), width=200, command=des)
            btn8.grid(row=3, column=1, padx=10, pady=10)
            buttonframe.pack(padx=40, pady=40)


        else:

            msg.configure(fg_color="red", text="incorrect text")
            return


    def des():
        dash.destroy()
        noti = ctk.CTkLabel(root, text='LOG OUT SUCCESSFUL', font=('Eras Demi ITC', 30), text_color='green')
        noti.place(x=100, y=400)


    def acc_details():
        global email_det
        global balance_det
        global age_det
        global phone_det
        global name_det

        query3 = 'select * from new_details where ACCOUNT_ID={}'.format(acc_no)
        cursor.execute(query3)
        details_data = cursor.fetchall()
        for i in details_data:
            email_det = i[5]
            balance_det = i[7]
            age_det = i[2]
            phone_det = i[4]
            name_det = i[1]

        global acc_details_page
        acc_details_page = Toplevel(root)

        acc_details_page.title("Account Details")
        acc_details_page.configure(background='#1a1a1a')
        acc_details_page.geometry("800x500")
        title_label = ctk.CTkLabel(acc_details_page, text="Account Details", font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))
        l1 = ctk.CTkLabel(acc_details_page, text='NAME', font=('Eras Demi ITC', 24, 'bold'))
        l1.place(x=20, y=70)
        l6 = ctk.CTkLabel(acc_details_page, text='Phone Number', font=('Eras Demi ITC', 22, 'bold'))
        l6.place(x=20, y=170)
        l3 = ctk.CTkLabel(acc_details_page, text='Email-ID', font=('Eras Demi ITC', 24, 'bold'))
        l3.place(x=20, y=270)
        l4 = ctk.CTkLabel(acc_details_page, text='Age', font=('Eras Demi ITC', 24, 'bold'))
        l4.place(x=20, y=120)
        l5 = ctk.CTkLabel(acc_details_page, text='Balance', font=('Eras Demi ITC', 24, 'bold'))
        l5.place(x=20, y=220)
        l7 = ctk.CTkLabel(acc_details_page, text='' + str(balance_det), font=('Eras Demi ITC', 24, 'bold'))
        l7.place(x=200, y=220)
        l8 = ctk.CTkLabel(acc_details_page, text='' + str(phone_det), font=('Eras Demi ITC', 24, 'bold'))
        l8.place(x=200, y=170)
        l9 = ctk.CTkLabel(acc_details_page, text='' + str(email_det), font=('Eras Demi ITC', 24, 'bold'))
        l9.place(x=200, y=270)
        la = ctk.CTkLabel(acc_details_page, text='' + str(name_det), font=('Eras Demi ITC', 24, 'bold'))
        la.place(x=200, y=70)
        la1 = ctk.CTkLabel(acc_details_page, text='' + str(age_det), font=('Eras Demi ITC', 24, 'bold'))
        la1.place(x=200, y=120)


    def forgot_password():
        global for_pass
        global temp_email1
        global temp_phone1
        global notif4
        global temp_slno1

        temp_phone1 = StringVar()
        temp_email1 = StringVar()
        temp_slno1 = StringVar()

        for_pass = Toplevel(root)
        for_pass.geometry("700x450")
        for_pass.title("Reset Password")
        for_pass.configure(background='#1a1a1a')

        notif4 = ctk.CTkLabel(for_pass, text='', font=('Eras Demi ITC', 24, 'bold'))
        notif4.place(x=50, y=250)
        title_label = ctk.CTkLabel(for_pass, text="Enter Your Details", font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))
        l2 = ctk.CTkLabel(for_pass, text="Account ID -", font=('Eras Demi ITC', 24, 'bold'))
        l2.place(x=50, y=70)
        l3 = ctk.CTkLabel(for_pass, text="Email ID -", font=('Eras Demi ITC', 24, 'bold'))
        l3.place(x=50, y=120)
        l4 = ctk.CTkLabel(for_pass, text="Phone Number -", font=('Eras Demi ITC', 24, 'bold'))
        l4.place(x=50, y=170)
        e1 = ctk.CTkEntry(for_pass, textvariable=temp_slno1)
        e1.place(x=300, y=70)
        e2 = ctk.CTkEntry(for_pass, textvariable=temp_email1)
        e2.place(x=300, y=120)
        e3 = ctk.CTkEntry(for_pass, textvariable=temp_phone1)
        e3.place(x=300, y=170)
        b1 = ctk.CTkButton(for_pass, bg_color='#252525', text='Proceed', font=('Eras Demi ITC', 20, 'bold'),
                           command=finish_forgpwd)
        b1.place(x=300, y=220)
        b2 = ctk.CTkButton(for_pass, text='Close', font=('Eras Demi ITC', 20, 'bold'), command=for_pass.destroy)
        b2.place(x=300, y=260)
        for_pass.mainloop()


    def finish_forgpwd():
        global temp_newpwd
        temp_newpwd = StringVar()
        global acc_no1
        acc_no1 = int(temp_slno1.get())
        x1 = "select * from new_details where Account_ID='{}';".format(acc_no1)
        cursor.execute(x1)
        data = cursor.fetchall()
        if data == []:
            notif4.configure(text='Invalid Account number', fg_color='red')
        else:
            for i in data:
                if i[4] == int(temp_phone1.get()) and i[5] == str(temp_email1.get()):
                    notif4.configure(text='Verified!', fg_color='green')

                    global notif5

                    final_forgscreen = Toplevel(root)
                    final_forgscreen.geometry("1000x500")
                    final_forgscreen.title("Update Password")
                    final_forgscreen.configure(background='#252525')
                    title_label = ctk.CTkLabel(final_forgscreen, text="Update Your Password",
                                               font=('Eras Demi ITC', 34, 'bold'))
                    title_label.pack(padx=100, pady=(10, 30))

                    l1 = ctk.CTkLabel(final_forgscreen, text='New password', font=('Eras Demi ITC', 24, 'bold'))
                    l1.place(x=25, y=80)

                    e1 = ctk.CTkEntry(final_forgscreen, textvariable=temp_newpwd, show='*')
                    e1.place(x=325, y=80)
                    b1 = ctk.CTkButton(final_forgscreen, bg_color='#252525', text="Confirm", command=update_psswd)
                    b1.place(x=325, y=130)
                    notif5 = ctk.CTkLabel(final_forgscreen, text="", font=('Eras Demi ITC', 24, 'bold'),
                                          fg_color='green')
                    notif5.place(x=50, y=180)
                    b2 = ctk.CTkButton(final_forgscreen, text='Close', command=final_forgscreen.destroy)
                    b2.place(x=480, y=130)
                else:
                    notif4.configure(text='Invalid Details!', fg_color='red')


    def update_psswd():
        if len(temp_newpwd.get()) == 0:
            notif5.configure(text='New Password can not be empty', fg_color='red')
        else:
            newp = temp_newpwd.get()
            x = "update new_details set password='{}' where Account_ID={};".format(newp, acc_no1)
            cursor.execute(x)
            con.commit()
            notif5.configure(text='Password Successfully changed', fg_color='green')


    def registration():
        Register_screen = Toplevel(root)
        Register_screen.title("Registration")
        Register_screen.geometry("1200x650")
        Register_screen.configure(background='#1a1a1a')

        global notif1
        global notif3

        notif1 = ctk.CTkLabel(Register_screen, text="", font=('Eras Demi ITC', 23, 'bold'))
        notif1.place(x=50, y=450)
        notif3 = ctk.CTkLabel(Register_screen, text="", font=('Eras Demi ITC', 23, 'bold'))
        notif3.place(x=50, y=500)
        title_label = ctk.CTkLabel(Register_screen, text="Enter Your Details",
                                   font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))

        l2 = ctk.CTkLabel(Register_screen, text="Name  ", font=('Eras Demi ITC', 23, 'bold'))
        l2.place(x=50, y=100)
        l3 = ctk.CTkLabel(Register_screen, text="Age  ", font=('Eras Demi ITC', 23, 'bold'))
        l3.place(x=50, y=150)
        l4 = ctk.CTkLabel(Register_screen, text="Gender(M/F)  ", font=('Eras Demi ITC', 23, 'bold'))
        l4.place(x=50, y=200)
        l5 = ctk.CTkLabel(Register_screen, text="Password ", font=('Eras Demi ITC', 23, 'bold'))
        l5.place(x=50, y=250)
        l6 = ctk.CTkLabel(Register_screen, text="Email  ", font=('Eras Demi ITC', 23, 'bold'))
        l6.place(x=50, y=300)
        l7 = ctk.CTkLabel(Register_screen, text='Phone Number  ', font=('Eras Demi ITC', 23, 'bold'))
        l7.place(x=50, y=350)

        global temp_name
        global temp_age
        global temp_gender
        global temp_password
        global temp_email
        global temp_phone

        temp_name = StringVar()
        temp_age = StringVar()
        temp_gender = StringVar()
        temp_password = StringVar()
        temp_email = StringVar()
        temp_phone = StringVar()

        e1 = ctk.CTkEntry(Register_screen, textvariable=temp_name)
        e1.place(x=300, y=100)

        e2 = ctk.CTkEntry(Register_screen, textvariable=temp_age)
        e2.place(x=300, y=150)

        e3 = ctk.CTkEntry(Register_screen, textvariable=temp_gender)
        e3.place(x=300, y=200)

        e4 = ctk.CTkEntry(Register_screen, show='*', textvariable=temp_password)
        e4.place(x=300, y=250)

        e5 = ctk.CTkEntry(Register_screen, textvariable=temp_email)
        e5.place(x=300, y=300)

        e6 = ctk.CTkEntry(Register_screen, textvariable=temp_phone)
        e6.place(x=300, y=350)

        b1 = ctk.CTkButton(Register_screen, text="Register now", font=('Eras Demi ITC', 20, 'bold'), command=finish_reg)
        b1.place(x=300, y=400)


    def finish_reg():
        global acc_no
        global age1
        global pn1

        acc_no = StringVar()

        print('done')
        name = temp_name.get()
        age = (temp_age.get())
        gender = temp_gender.get()
        password = temp_password.get()
        email = temp_email.get()
        pn = (temp_phone.get())

        age1 = int(age)
        pn1 = int(pn)
        if name == "" or age == "" or gender == "" or password == "" or email == "" or pn == "":
            notif1.configure(fg_color="red", text="All fields need to be filled", font=('Eras Demi ITC', 20, 'bold'))
        if bool((re.fullmatch(email_reg, email))) == True:
            check = 0
            x = "use project1;"
            cursor.execute(x)
            query = "select name from new_details;"
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            for i in data:
                if name in i:
                    notif1.configure(fg_color="red", text="Account already exists", font=('Eras Demi ITC', 20, 'bold'))
                    check += 1
                else:
                    notif1.configure(fg_color='green', text='Registration successful',
                                     font=('Eras Demi ITC', 20, 'bold'))
            if check == 0:
                x = "use project1;"
                cursor.execute(x)
                query3 = "insert into new_details (NAME,AGE,GENDER,PHONE_NUMBER,EMAIL,PASSWORD) values('{}',{},'{}',{},'{}','{}');".format(
                    name, age1, gender, pn1, email, password)
                cursor.execute(query3)
                con.commit()
                y = "select Account_ID from new_details where PASSWORD='{}' and EMAIL='{}';".format(
                    password, email)
                cursor.execute(y)
                data = cursor.fetchone()
                acc_no = str(data[0])
                notif3.configure(text="Account number generated : " + acc_no, fg_color='green')

        else:
            notif1.configure(fg_color="red", text="invalid email entered", font=('Eras Demi ITC', 20, 'bold'))


    def transfer():

        global to_acc
        global to_name
        global passwd
        global current_balance_sender
        global curr_bal_rec
        global trans_amt
        global updated_bal_sender
        global updated_bal_rec
        global transfer_notif
        global sender_name
        global transfer_notif1

        to_acc = StringVar()
        trans_amt = StringVar()
        current_balance_sender = IntVar()
        passwd = StringVar()
        to_name = StringVar()
        curr_bal_rec = IntVar()
        updated_bal_sender = IntVar()
        updated_bal_rec = IntVar()
        sender_name = StringVar()

        transfer_notif = Toplevel(root)
        transfer_notif.title("Transfer Screen")
        transfer_notif.geometry("1000x500")
        transfer_notif.configure(background='#1a1a1a')
        title_label = ctk.CTkLabel(transfer_notif, text="Enter Your Details", font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))
        lab2 = ctk.CTkLabel(transfer_notif, text='To Name', font=('Eras Demi ITC', 22, 'bold'))
        lab2.place(x=30, y=50)
        lab3 = ctk.CTkLabel(transfer_notif, text='To Account_ID', font=('Eras Demi ITC', 22, 'bold'))
        lab3.place(x=30, y=100)
        lab4 = ctk.CTkLabel(transfer_notif, text='Amount', font=('Eras Demi ITC', 22, 'bold'))
        lab4.place(x=30, y=150)
        lab5 = ctk.CTkLabel(transfer_notif, text='Password', font=('Eras Demi ITC', 22, 'bold'))
        lab5.place(x=30, y=200)

        ent1 = ctk.CTkEntry(transfer_notif, textvariable=to_name)
        ent1.place(x=250, y=50)
        ent1 = ctk.CTkEntry(transfer_notif, textvariable=to_acc)
        ent1.place(x=250, y=100)
        ent1 = ctk.CTkEntry(transfer_notif, textvariable=trans_amt)
        ent1.place(x=250, y=150)
        ent1 = ctk.CTkEntry(transfer_notif, textvariable=passwd)
        ent1.place(x=250, y=200)

        b1 = ctk.CTkButton(transfer_notif, text='Transfer Now', font=('Portico Diagonal', 22), command=finish_transfer)
        b1.place(x=250, y=300)
        transfer_notif1 = ctk.CTkLabel(transfer_notif, text='', text_color='green', font=('Eras Demi ITC', 30, 'bold'))
        transfer_notif1.place(x=50, y=350)


    def finish_transfer():
        trans1 = "select * from new_details where Account_ID={};".format(int(acc_no))
        cursor.execute(trans1)
        trans_data = cursor.fetchall()
        for i in trans_data:
            current_balance_sender = i[7]
            trans_pwd = i[6]
            sender_name = i[1]
        if passwd.get() == trans_pwd:
            print("valid password")
            if int(trans_amt.get()) > current_balance_sender or int(trans_amt.get()) <= 0:
                transfer_notif1.configure(text="Invalid Amount", text_color='red')
            else:
                updated_bal_sender = current_balance_sender - int(trans_amt.get())
                trans2 = "update new_details set BALANCE='{}' where ACCOUNT_ID='{}';".format(updated_bal_sender,
                                                                                             int(acc_no))
                cursor.execute(trans2)
                con.commit()
                trans3 = "select * from new_details where ACCOUNT_ID={};".format(int(to_acc.get()))
                cursor.execute(trans3)
                tdata = cursor.fetchall()
                if len(tdata) == 0:
                    transfer_notif1.configure(text='Invalid Details', text_color='red')
                else:
                    curr_bal_rec = tdata[0][7]
                    updated_bal_rec = curr_bal_rec + int(trans_amt.get())
                    trans4 = "update new_details set BALANCE={} where ACCOUNT_ID='{}';".format(updated_bal_rec,
                                                                                               int(to_acc.get()))
                    cursor.execute(trans4)
                    con.commit()
                    trans5 = "update new_details set BALANCE={} where ACCOUNT_ID={};".format(updated_bal_sender, acc_no)
                    cursor.execute(trans5)
                    con.commit()
                    history3 = ("insert into trans_history(Account_sender,NAME_rec,Account_rec,TRANSFERED_AMT,"
                                "Balance_before,BALANCE_after) values({},'{}',{},{},{},{});").format(
                        acc_no, to_name.get(), int(to_acc.get()), int(trans_amt.get()), current_balance_sender,
                        updated_bal_sender)
                    cursor.execute(history3)
                    con.commit()
                    history4 = ("insert into rec_history(acc_of_receiver,name_of_sender,Account_sender,TRANSFERED_AMT,"
                                "Balance_before,BALANCE_after) values({},'{}',{},{},{},{});").format(
                        int(to_acc.get()), sender_name, acc_no, int(trans_amt.get()), curr_bal_rec, updated_bal_rec)
                    cursor.execute(history4)
                    con.commit()
                    transfer_notif1.configure(text='Transferred Successfully', text_color='green')
        else:
            transfer_notif1.configure(text='Invalid Password', text_color='Red')


    def withdraw1():

        global acc_no2
        global cur_balance
        global pswd
        global with_amt
        global updated_balance
        global with_notif1

        acc_no2 = StringVar()
        pswd = StringVar()
        cur_balance = IntVar()
        with_amt = StringVar()
        updated_balance = IntVar()

        withnotif = Toplevel(root)
        withnotif.title("Withdraw Money")
        withnotif.geometry("800x500")
        withnotif.configure(background='#1a1a1a')
        title_label = ctk.CTkLabel(withnotif, text="Enter Your Details", font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))
        l1 = ctk.CTkLabel(withnotif, text="Account_No", font=('Eras Demi ITC', 23, 'bold'))
        l1.place(x=30, y=50)
        l2 = ctk.CTkLabel(withnotif, text="Account Password", font=('Eras Demi ITC', 23, 'bold'))
        l2.place(x=30, y=100)
        l3 = ctk.CTkLabel(withnotif, text="Amount to be withdrawn", font=('Eras Demi ITC', 18, 'bold'))
        l3.place(x=30, y=150)

        e1 = ctk.CTkEntry(withnotif, textvariable=acc_no2)
        e1.place(x=270, y=50)
        e2 = ctk.CTkEntry(withnotif, textvariable=pswd, show='*')
        e2.place(x=270, y=100)
        e3 = ctk.CTkEntry(withnotif, textvariable=with_amt)
        e3.place(x=270, y=150)

        b1 = ctk.CTkButton(withnotif, text="Withdraw", font=('Eras Demi ITC', 23, 'bold'), command=finish_withdraw)
        b1.place(x=160, y=250)
        b2 = ctk.CTkButton(withnotif, text="Close", font=('Eras Demi ITC', 23, 'bold'), command=withnotif.destroy)
        b2.place(x=340, y=250)
        with_notif1 = ctk.CTkLabel(withnotif, text='', text_color='green', font=('Eras Demi ITC', 30, 'bold'))
        with_notif1.place(x=50, y=350)


    def finish_withdraw():
        with1 = "select * from new_details where ACCOUNT_ID={};".format(int(acc_no))
        cursor.execute(with1)
        with_data = cursor.fetchall()

        for i in with_data:
            cur_balance = i[7]
            with_pswd = i[6]
            if with_pswd == pswd.get():
                print("account verified")
                if int(with_amt.get()) > cur_balance or int(with_amt.get()) <= 0:
                    with_notif1.configure(text="Invalid Amount", text_color='red')
                else:
                    updated_balance = cur_balance - int(with_amt.get())
                    with2 = "update new_details set BALANCE='{}' where ACCOUNT_ID='{}';".format(updated_balance,
                                                                                                int(acc_no))
                    cursor.execute(with2)
                    con.commit()
                    with_notif1.configure(text="Amount Withdrawn Successfully", text_color='green')
            else:
                with_notif1.configure(text="Invalid Password", text_color='red')


    def deposit1():

        global acc_no3
        global cur_balance
        global pswd
        global dep_amt
        global updated_balance
        global dep_notif1

        acc_no3 = StringVar()
        pswd = StringVar()
        cur_balance = IntVar()
        dep_amt = StringVar()
        updated_balance = IntVar()

        depnotif = Toplevel(root)
        depnotif.title("Deposit Money")
        depnotif.geometry("800x500")
        depnotif.configure(background='#1a1a1a')
        title_label = ctk.CTkLabel(depnotif, text="Enter Your Details", font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))
        l1 = ctk.CTkLabel(depnotif, text="Account_No", font=('Eras Demi ITC', 23, 'bold'))
        l1.place(x=30, y=50)
        l2 = ctk.CTkLabel(depnotif, text="Account Password", font=('Eras Demi ITC', 23, 'bold'))
        l2.place(x=30, y=100)
        l3 = ctk.CTkLabel(depnotif, text="Amount to be deposited", font=('Eras Demi ITC', 18, 'bold'))
        l3.place(x=30, y=150)

        e1 = ctk.CTkEntry(depnotif, textvariable=acc_no3)
        e1.place(x=270, y=50)
        e2 = ctk.CTkEntry(depnotif, textvariable=pswd, show="*")
        e2.place(x=270, y=100)
        e3 = ctk.CTkEntry(depnotif, textvariable=dep_amt)
        e3.place(x=270, y=150)

        b1 = ctk.CTkButton(depnotif, text="Deposit", font=('Eras Demi ITC', 23, 'bold'), command=finish_deposit)
        b1.place(x=160, y=250)
        b2 = ctk.CTkButton(depnotif, text="Close", font=('Eras Demi ITC', 23, 'bold'), command=depnotif.destroy)
        b2.place(x=340, y=250)
        dep_notif1 = ctk.CTkLabel(depnotif, text='', text_color='green', font=('Eras Demi ITC', 30, 'bold'))
        dep_notif1.place(x=50, y=350)


    def finish_deposit():
        dep1 = "select * from new_details where ACCOUNT_ID={};".format(int(acc_no))
        cursor.execute(dep1)
        dep_data = cursor.fetchall()
        for i in dep_data:
            cur_balance = i[7]
            dep_pswd = i[6]
            if dep_pswd == pswd.get():
                print("account verified")
                if int(dep_amt.get()) <= 0:
                    dep_notif1.configure(text="Invalid Amount", text_color='red')
                else:
                    updated_balance = cur_balance + int(dep_amt.get())
                    dep2 = "update new_details set BALANCE={} where ACCOUNT_ID={};".format(updated_balance, int(acc_no))
                    cursor.execute(dep2)
                    con.commit()
                    dep_notif1.configure(text="Amount Deposited Successfully", text_color='green')
            else:
                dep_notif1.configure(text="Invalid Password", text_color='red')


    def Update_details():

        global acc_no4
        global new_name
        global new_email
        global new_phone
        global pasd
        global update_notif

        acc_no4 = StringVar()
        new_name = StringVar()
        new_phone = StringVar()
        new_email = StringVar()
        pasd = StringVar()

        deet = Toplevel(root)
        deet.title("Update Details")
        deet.geometry("1200x600")
        deet.configure(background='#1a1a1a')
        title_label = ctk.CTkLabel(deet, text="Enter Your Details", font=('Eras Demi ITC', 34, 'bold'))
        title_label.pack(padx=100, pady=(10, 30))
        l1 = ctk.CTkLabel(deet, text="Account No.", font=('Eras Demi ITC', 20, 'bold'))
        l1.place(x=30, y=50)
        l2 = ctk.CTkLabel(deet, text="Account Password", font=('Eras Demi ITC', 20, 'bold'))
        l2.place(x=30, y=100)
        l3 = ctk.CTkLabel(deet, text="New Name*", font=('Eras Demi ITC', 20, 'bold'))
        l3.place(x=30, y=150)
        l4 = ctk.CTkLabel(deet, text="New Email*", font=('Eras Demi ITC', 20, 'bold'))
        l4.place(x=30, y=200)
        l5 = ctk.CTkLabel(deet, text="New Phone Number*", font=('Eras Demi ITC', 20, 'bold'))
        l5.place(x=30, y=250)
        l6 = ctk.CTkLabel(deet, text="* -> Enter the previous details if theres no change",
                          font=('Eras Demi ITC', 10, 'bold'))
        l6.place(x=30, y=290)

        e1 = ctk.CTkEntry(deet, textvariable=acc_no4)
        e1.place(x=270, y=50)
        e2 = ctk.CTkEntry(deet, textvariable=pasd, show="*")
        e2.place(x=270, y=100)
        e3 = ctk.CTkEntry(deet, textvariable=new_name)
        e3.place(x=270, y=150)
        e4 = ctk.CTkEntry(deet, textvariable=new_email)
        e4.place(x=270, y=200)
        e5 = ctk.CTkEntry(deet, textvariable=new_phone)
        e5.place(x=270, y=250)

        b1 = ctk.CTkButton(deet, text="Update", font=('Eras Demi ITC', 23, 'bold'), command=finish_update)
        b1.place(x=160, y=350)
        b2 = ctk.CTkButton(deet, text="Close", font=('Eras Demi ITC', 23, 'bold'), command=deet.destroy)
        b2.place(x=340, y=350)
        update_notif = ctk.CTkLabel(deet, text='', text_color='green', font=('Eras Demi ITC', 30, 'bold'))
        update_notif.place(x=50, y=410)


    def finish_update():
        deet1 = "select * from new_details where ACCOUNT_ID={};".format(int(acc_no4.get()))
        cursor.execute(deet1)
        deet_data = cursor.fetchall()
        for i in deet_data:
            deet_psd = i[6]
            if deet_psd == pasd.get():
                print("account found")
                deet2 = "update new_details set NAME='{}',PHONE_NUMBER={},EMAIL='{}' where ACCOUNT_ID={}".format(
                    new_name.get(),
                    new_phone.get(),
                    new_email.get(),
                    int(acc_no4.get()))
                cursor.execute(deet2)
                con.commit()
                update_notif.configure(text="Details Updated Successfully", text_color='green')
            else:
                update_notif.configure(text="Invalid Password", text_color="red")


    def history():

        history = Toplevel(root)
        history.geometry("800x500")
        history.title("History")
        history.configure(background='#1a1a1a')

        history5 = 'select * from trans_history where Account_sender={};'.format(acc_no)
        cursor.execute(history5)
        his_data = cursor.fetchall()

        history6 = 'select * from rec_history where acc_of_receiver={};'.format(acc_no)
        cursor.execute(history6)
        his_data1 = cursor.fetchall()

        for i in his_data:
            global y
            y = 10
            send_acc = i[0]
            rec_name = i[1]
            rec_acc = i[2]
            trans_amount = i[3]
            bala_bef = i[4]
            bala_aft = i[5]
            type = i[6]
            label1 = ctk.CTkLabel(history, text=' ' + str(rec_name) + '   ' + str(rec_acc) + '   -' + str(
                trans_amount) + '   ' + str(bala_bef) + '   ' + str(bala_aft) + '   ' + str(type),
                                  font=("Eras Demi ITC", 20),
                                  text_color='white')
            label1.grid(padx=20, pady=y)
            y += 10

        for i in his_data1:
            rece_acc = i[0]
            send_na = i[1]
            send_ac = i[2]
            trans_amount = i[3]
            bala_bef = i[4]
            bala_aft = i[5]
            type = i[6]
            label1 = ctk.CTkLabel(history, text=' ' + str(send_na) + '   ' + str(send_ac) + '   +' + str(
                trans_amount) + '   ' + str(bala_bef) + '   ' + str(bala_aft) + '   ' + str(type),
                                  font=("Eras Demi ITC", 20),
                                  text_color='white')
            label1.grid(padx=20, pady=y)


    # welcome page
    b1 = ctk.CTkButton(root, text='Log In', font=('Eras Demi ITC', 20, 'bold'), command=login)
    b2 = ctk.CTkButton(root, text='Sign Up', font=('Eras Demi ITC', 20, 'bold'), command=registration)
    image = ctk.CTkImage(dark_image=Image.open(r"logo.png"), size=(180, 150))
    image_label = ctk.CTkLabel(root, image=image, text="")
    image_label.pack()
    b1.place(x=205, y=280)
    b2.place(x=365, y=280)

root.mainloop()
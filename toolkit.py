import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import hashlib
import time 
import pyautogui
import os
import shutil
import threading
import socket
import string
import smtplib
import platform
import random
import requests

# -----------------------------------------------------------------ui
BG_COLOR = "#1e1e1e"      
FG_COLOR = "white"        
BTN_COLOR = "#2c3e50"     
BTN_TEXT = "white"
TITLE_COLOR = "cyan"



def load_users():
    if not os.path.exists("users.txt"):
        return
    
    with open("users.txt","r") as f:
        for line in f:
            username,password = line.strip().split(",")
            users[username] = password

users = {}

#-------------------------------------------------------------- log file function
def log_activity(text):
    with open("log_file.txt","a") as f:
        f.write(f"{text} time {time.ctime()} \n")

# -----------------------------------------------------------creative ui window label button
def create_window(title, size="350x300"):
    win = tk.Toplevel()
    win.title(title)
    win.geometry(size)
    win.configure(bg=BG_COLOR)
    return win


def create_label(parent, text):
    return tk.Label(parent, text=text, bg=BG_COLOR, fg=FG_COLOR)


def create_button(parent, text, command):
    return tk.Button(parent, text=text, command=command,
                     bg=BTN_COLOR, fg=BTN_TEXT, width=20)
# ------------------------------------------------------------------


def show_success_popup(title,message):

    win = tk.Toplevel()
    win.title(title)
    win.geometry("450x200")
    win.configure(bg="#1e1e1e")

    tk.Label(
        win,
        text=message,
        font=("Arial",12,"bold"),
        fg="lime",
        bg="#1e1e1e",
        wraplength=380,
        justify="center"
    ).pack(pady=30)

    tk.Button(
        win,
        text="OK",
        width=10,
        bg="#2c3e50",
        fg="white",
        command=win.destroy
    ).pack()

def show_warning_popup(title, message):

    win = tk.Toplevel()
    win.title(title)
    win.geometry("320x150")
    win.configure(bg=BG_COLOR)

    tk.Label(
        win,
        text=message,
        font=("Arial",12,"bold"),
        fg="orange",
        bg=BG_COLOR
    ).pack(pady=30)

    tk.Button(
        win,
        text="OK",
        command=win.destroy,
        bg=BTN_COLOR,
        fg=BTN_TEXT,
        width=10
    ).pack()

def show_error_popup(title, message):

    win = tk.Toplevel()
    win.title(title)
    win.geometry("350x170")
    win.configure(bg=BG_COLOR)

    tk.Label(
        win,
        text=message,
        font=("Arial",11,"bold"),
        fg="red",
        bg=BG_COLOR,
        wraplength=300
    ).pack(pady=30)

    tk.Button(
        win,
        text="Close",
        bg=BTN_COLOR,
        fg=BTN_TEXT,
        width=10,
        command=win.destroy
    ).pack()

# -------------------------------signin and signup   
def signup():
    username = entry_username.get()
    password = entry_password.get()

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if username in users:
        show_warning_popup("User Exists", "User already registered ⚠")
        return
    
    users[username]=password_hash
    with open("users.txt","a") as f:
        f.write(f"{username},{password_hash}\n")
        
    log_activity(f"{username} - new user signup")
    
    show_success_popup("Account Created",f"Welcome {username} 🎉")

    
def signin():
    name = entry_username.get()
    password = entry_password.get()

    password_hashed = hashlib.sha256(password.encode()).hexdigest()

    if name in users and users[name] == password_hashed:
        log_activity(f"{name} user logged in")
        show_success_popup("Login Success",f"Welcome back {name} 🔐")

        open_main_menu()
    else:
        show_error_popup("Error","Invalid credentials")

# -------------------------------------arrange files

def arrange_file():

    path = filedialog.askdirectory(title="Select Folder to Arrange")

    if not path:
        return

    for file in os.listdir(path):

        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            extension = file.split(".")[-1]
            folder = os.path.join(path, extension)
            if not os.path.exists(folder):
                os.makedirs(folder)
            shutil.move(file_path, os.path.join(folder, file))

    show_success_popup("Success", "Files arranged successfully 📂")
    log_activity("Arrange files")

# -----------------------------take screenshots {show output }

def screenshot():

    folder = "screenshots"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_name = f"screenshot_{int(time.time())}.png"
    file_path = os.path.join(folder, file_name)

    img = pyautogui.screenshot(file_path)

    log_activity("screenshot saved")

    show_success_popup(
        "Screenshot Saved",
        f"Saved at:\n{file_path}\n\nYou can open from screenshots folder."
    )

    os.startfile(file_path) 

#------------------------------------- find domain name
def ip_address_perform():
    domain_name = entry_domainname.get()

    ip_a = socket.gethostbyname(domain_name)

    show_success_popup("IP Address", ip_a)
    log_activity("ip address performed")

def ip_address():
    win = create_window("Domain to IP Address", "350x250")
    create_label(win, "Enter Domain Name").pack(pady=10)
    
    global entry_domainname
    entry_domainname = tk.Entry(win,width=30)
    entry_domainname.pack()

    create_button(win, "Find IP", ip_address_perform).pack(pady=20)

# -----------------------------------------------------password strength

def password_strength():

    password = enter_password.get()
    length = len(password)>=8
    upper = any(p.isupper() for p in password)
    lower = any(p.islower() for p in password)
    digit = any(p.isdigit() for p in password)
    special = any(p in string.punctuation for p in password)

    passsum = sum([length, upper, lower, digit, special])
    
    local_password_list = ["admin","password","12345678","kali","test"]
    
    for p in local_password_list:
        if p == password:
            result = "It is very weak password \n It can be easily cracked"
            show_success_popup(f"Passowrd strength", result) 
            log_activity("Password strength checked")
            return
            
    if passsum == 5:
        result = "Strong Password"
    elif passsum >=3:
        result = "Average Password"
    else:
        result = "Weak Password"
        
    show_success_popup(f"Passowrd strength", result) 
    log_activity("Password Strength Checked")

#--------------------------------- password strength gui
def password_strength_gui():

    win = create_window("Password Checker","350x250")

    create_label(win,"Enter Password").pack(pady=10)

    global enter_password
    enter_password = tk.Entry(win,width=30)
    enter_password.pack()

    create_button(win,"Check Strength",password_strength).pack(pady=15)
    
# -------------------------------------------------------sql injection check

sql_errors = ["sql syntax","mysql","syntax error","database error","unknown column","unclosed quotation"]
def sql_check():
    url = enter_url.get()
    parameter = enter_parameter.get()
    test = enter_test.get()
    
    try:
        payload = {parameter:test}
        response = requests.get(url,params = payload,timeout=5)
        text = response.text.lower()

        for error in sql_errors:
            if error in text:
                messagebox.showwarning("sql injection","Possible vulnerability detected")
                log_activity("sql injection detection performed")
                return
        show_success_popup("SQL Injection", "No SQL Error Detected")
        log_activity("sql injection detection performed")
    except:
        show_error_popup("Connection Error","❌ Unable to connect to the website.\nCheck URL or internet connection.")
        log_activity("sql injection detection performed")

# ----------------------------------------------------sql injectoin gui
def sql_check_gui():

    win = create_window("Sql injection Detection","400x300")
    
    tk.Label(win, text="SQL Injection Checker",font=("Arial",14,"bold"),bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=10)
    
    create_label(win,"Enter URL").pack()
    
    global enter_url
    enter_url = tk.Entry(win,width=40)
    enter_url.pack()
    
    create_label(win,"Parameter Name").pack()
    global enter_parameter
    enter_parameter = tk.Entry(win)
    enter_parameter.pack()
    
    create_label(win,"Test Payload").pack()
    global enter_test
    enter_test = tk.Entry(win)
    enter_test.pack()
    
    create_button(win, "Check SQL Injection",sql_check).pack(pady=15)



# ------------------------------------------------------------open ports detect
def open_ports():
    ip_a = enter_ipaddress.get()
    start_port = int(enter_startingport.get())
    end_port = int(enter_endport.get())
    open_ports_list = []
    
    show_success_popup("scanning",f"[+] Scanning for {ip_a} ")

    for i in range(start_port , end_port + 1):
        scan = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        scan.settimeout(1)

        connection = scan.connect_ex((ip_a,i))
        if connection == 0:
            open_ports_list.append(i)
        scan.close()
    if open_ports_list:
        show_success_popup("Open Ports", f"Open Ports: {open_ports_list}")
    else:
        show_success_popup("Result", "No open ports found")
    log_activity("Open ports detection")


# ------------------------------------------------------------open ports gui
def open_ports_gui():

    win = create_window("Open Ports Detection","350x300")

    create_label(win,"IP Address").pack()

    global enter_ipaddress
    enter_ipaddress = tk.Entry(win)
    enter_ipaddress.pack()

    create_label(win,"Starting Port").pack()

    global enter_startingport
    enter_startingport = tk.Entry(win)
    enter_startingport.pack()

    create_label(win,"End Port").pack()

    global enter_endport
    enter_endport = tk.Entry(win)
    enter_endport.pack()

    create_button(win,"Scan Ports",open_ports).pack(pady=15)
    
#----------------------------------------------------- Mail sender

def mail_sender():
    sender = ""
    password = ""
    receiver = enter_receiverid.get()

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    server.login(sender,password)

    message = enter_message.get()
    server.sendmail(sender,receiver,message)

    server.quit()
    show_success_popup("Successful","Mail Sent")
    log_activity("Mail Sent")
# --------------------------------------------------mail send gui
def mail_send_gui():

    win = create_window("Mail Sender","350x250")

    create_label(win,"Receiver Email").pack()

    global enter_receiverid
    enter_receiverid = tk.Entry(win,width=30)
    enter_receiverid.pack()

    create_label(win,"Message").pack()

    global enter_message
    enter_message = tk.Entry(win,width=30)
    enter_message.pack()

    create_button(win,"Send Mail",mail_sender).pack(pady=15)
    
# -------------------------------------------------system information 
def system_info():

    info = (
        f"System: {platform.system()}\n"
        f"Node Name: {platform.node()}\n"
        f"Release: {platform.release()}\n"
        f"Version: {platform.version()}\n"
        f"Machine: {platform.machine()}\n"
        f"Processor: {platform.processor()}"
    )
    label_sysinfo.config(text=info)
    log_activity("System information")

# --------------------------------------------system information gui

def system_info_gui():

    win = create_window("System Information","450x350")

    create_label(win,"System Information").pack(pady=10)

    global label_sysinfo
    label_sysinfo = tk.Label(win,bg=BG_COLOR,fg=FG_COLOR,justify="left")
    label_sysinfo.pack(pady=10)

    create_button(win,"Show System Info",system_info).pack()
    

# ----------------------------------------------------password generator
def password_generator(length=8):

    password = ""
    characters = string.ascii_letters + string.digits + string.punctuation 

    for i in range(length):
        ch = random.choice(characters)
        password = password + ch
    show_success_popup("Password Generated" , f"Generated password is : {password}" )
    log_activity("Password generated")
#----------------------------------------------------- password generator gui
def password_generator_gui():

    win = create_window("Password Generator","350x250")

    create_label(win,"Generate Secure Password").pack(pady=20)

    create_button(win,"Generate Password",password_generator).pack()
# ----------------------------------------------------------subdomain finder -

def subdomain_finder(domain):

    subdomains = ["www","mail","ftp","test","dev","api","blog","shop","admin"]

    found_subdomains = []

    for sub in subdomains:
        url = f"http://{sub}.{domain}"

        try:
            response = requests.get(url, timeout=3)

            if response.status_code < 400:
                found_subdomains.append(url)

        except:
            pass
    log_activity("subdomain finder")
    return found_subdomains

def run_subdomain_scan():

    domain = entry_subdomain.get()

    result_box.delete(1.0, tk.END)

    results = subdomain_finder(domain)

    if results:
        for r in results:
            result_box.insert(tk.END, r + "\n")
    else:
        result_box.insert(tk.END, "No subdomains found")
# --------------------------------------------------------subdomain gui
def subdomain_window():

    win = create_window("Subdomain Finder", "400x300")

    create_label(win, "Enter Domain").pack(pady=10)

    global entry_subdomain
    entry_subdomain = tk.Entry(win, width=30)
    entry_subdomain.pack()

    create_button(win, "Find Subdomains", run_subdomain_scan).pack(pady=10)

    global result_box
    result_box = tk.Text(win, height=10, width=45)
    result_box.pack()

# UI
load_users()
root = tk.Tk()
root.title("Cyber Security Toolkit")
root.geometry("600x400")
root.configure(bg=BG_COLOR)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=40)
title = tk.Label(frame,
                 text="Cyber Security Toolkit",
                 font=("Arial",18,"bold"),
                 fg="cyan",
                 bg="#1e1e1e")
title.grid(row=0,column=0,columnspan=2,pady=10)

tk.Label(frame,text="Username",
         fg="white",bg="#1e1e1e").grid(row=1,column=0,pady=5)

entry_username = tk.Entry(frame,width=25)
entry_username.grid(row=1,column=1)

tk.Label(frame,text="Password",
         fg="white",bg="#1e1e1e").grid(row=2,column=0,pady=5)

entry_password = tk.Entry(frame,show="*",width=25)
entry_password.grid(row=2,column=1)

tk.Button(frame,text="Sign Up",bg="#2ecc71",width=10, command=signup).grid(row=3,column=0,pady=15)

tk.Button(frame,text="Sign In", bg="#3498db", width=10, command=signin).grid(row=3,column=1)


# -----------------------------------------------all button gui resize
def open_main_menu():
    menu = tk.Toplevel(root)
    menu.title("Main Menu")
    menu.geometry("400x500")
    menu.configure(bg="#1e1e1e")

    tk.Label(menu,text="Cyber Security Toolkit",font=("Arial",16,"bold"),fg=TITLE_COLOR,bg=BG_COLOR).pack(pady=15)
    btn_style = {
    "width":25,
    "bg":"#2c3e50",
    "fg":"white"
    }
    # buttons
    tk.Button(menu,text="Arrange Files",command=arrange_file,**btn_style).pack(pady=5)
    tk.Button(menu,text="Take Screenshot",command=screenshot,**btn_style).pack(pady=5)
    tk.Button(menu,text="Find IP",command=ip_address,**btn_style).pack(pady=5)
    tk.Button(menu,text="Password Strength",command=password_strength_gui,**btn_style).pack(pady=5)
    tk.Button(menu,text="SQL Injection Check",command=sql_check_gui,**btn_style).pack(pady=5)
    tk.Button(menu,text="Open Ports Scanner",command=open_ports_gui,**btn_style).pack(pady=5)
    tk.Button(menu,text="Mail Sender",command=mail_send_gui,**btn_style).pack(pady=5)
    tk.Button(menu, text="System Info", command=system_info_gui,**btn_style).pack(pady=5)
    tk.Button(menu,text="Subdomain Finder",command=subdomain_window,**btn_style).pack(pady=5)
    tk.Button(menu,text="Password Generator", command=password_generator_gui,**btn_style).pack(pady=5)

    
root.mainloop()

# chat-bot-gui.py  (Clean White UI Version)

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests

SERVER_URL = "http://localhost:5000"


# ─────────── App State ───────────
class AppState:
    def __init__(self):
        self.token = None
        self.username = None
        self.context = ""
        self.is_responding = False

    def set_logged_in(self, token, username):
        self.token = token
        self.username = username
        self.context = ""

    def logout(self):
        self.token = None
        self.username = None
        self.context = ""
        self.is_responding = False

    @property
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}


state = AppState()


# ─────────── UI Setup ───────────
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("600x520")
root.configure(bg="white")


# Colors
BG = "white"
FG = "black"
BTN_BG = "black"
BTN_FG = "white"
ERR = "red"


# Entry style
style = ttk.Style()
style.theme_use("clam")
style.configure("TEntry",
    fieldbackground="white",
    foreground="black",
    padding=6,
    borderwidth=1,
    relief="solid"
)


# Button
def make_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        bg=BTN_BG,
        fg=BTN_FG,
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=6,
        relief="flat",
        command=command,
        cursor="hand2"
    )


# Entry with label
def labeled_entry(parent, text, show=None):
    tk.Label(parent, text=text, bg=BG, fg=FG).pack(anchor="w", pady=(8, 2))
    e = ttk.Entry(parent, show=show)
    e.pack(fill="x")
    return e


# Frame switching
container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True)

def show_frame(frame):
    for f in container.winfo_children():
        f.pack_forget()
    frame.pack(fill="both", expand=True)


# ─────────── Login ───────────
login_frame = tk.Frame(container, bg=BG)

tk.Label(login_frame, text="AI Chatbot", bg=BG, fg=FG, font=("Segoe UI", 18, "bold")).pack(pady=10)

login_user = labeled_entry(login_frame, "Username")
login_pass = labeled_entry(login_frame, "Password", show="*")

login_error = tk.Label(login_frame, text="", bg=BG, fg=ERR)
login_error.pack()


def login():
    username = login_user.get()
    password = login_pass.get()

    try:
        r = requests.post(f"{SERVER_URL}/api/auth/login",
                          json={"username": username, "password": password})
        data = r.json()

        if r.status_code == 200:
            state.set_logged_in(data["token"], data["username"])
            open_chat()
        else:
            login_error.config(text=data.get("error"))
    except:
        login_error.config(text="Cannot reach server")


make_button(login_frame, "Sign In", login).pack(pady=10)

tk.Button(login_frame, text="Create account →", bg=BG, fg="black",
          relief="flat", command=lambda: show_frame(register_frame)).pack()


# ─────────── Register ───────────
register_frame = tk.Frame(container, bg=BG)

tk.Label(register_frame, text="Create Account", bg=BG, fg=FG,
         font=("Segoe UI", 18, "bold")).pack(pady=10)

reg_user = labeled_entry(register_frame, "Username")
reg_pass = labeled_entry(register_frame, "Password", show="*")
reg_pass2 = labeled_entry(register_frame, "Confirm Password", show="*")

reg_error = tk.Label(register_frame, text="", bg=BG, fg=ERR)
reg_error.pack()


def register():
    username = reg_user.get()
    password = reg_pass.get()
    confirm = reg_pass2.get()

    if password != confirm:
        reg_error.config(text="Passwords do not match")
        return

    try:
        r = requests.post(f"{SERVER_URL}/api/auth/register",
                          json={"username": username, "password": password})
        data = r.json()

        if r.status_code == 201:
            state.set_logged_in(data["token"], data["username"])
            open_chat()
        else:
            reg_error.config(text=data.get("error"))
    except:
        reg_error.config(text="Cannot reach server")


make_button(register_frame, "Create Account", register).pack(pady=10)

tk.Button(register_frame, text="← Back to Login", bg=BG, fg="black",
          relief="flat", command=lambda: show_frame(login_frame)).pack()


# ─────────── Chat ───────────
chat_frame = tk.Frame(container, bg=BG)

top = tk.Frame(chat_frame, bg=BG)
top.pack(fill="x")

user_label = tk.Label(top, text="", bg=BG, fg=FG)
user_label.pack(side="left", padx=10)


def logout():
    state.logout()
    show_frame(login_frame)


make_button(top, "Logout", logout).pack(side="right", padx=10)


chat_box = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED,
                                     bg="#f5f5f5", fg="black")
chat_box.pack(fill="both", expand=True, padx=10, pady=10)

input_box = tk.Entry(chat_frame, bg="white", fg="black")
input_box.pack(fill="x", padx=10)


def send():
    msg = input_box.get()
    if not msg:
        return

    input_box.delete(0, tk.END)

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {msg}\n")

    try:
        r = requests.post(f"{SERVER_URL}/api/chat",
                          json={"question": msg},
                          headers=state.auth_headers)
        data = r.json()

        chat_box.insert(tk.END, f"Bot: {data.get('response')}\n\n")
    except:
        chat_box.insert(tk.END, "Error connecting to server\n\n")

    chat_box.config(state=tk.DISABLED)


make_button(chat_frame, "Send", send).pack(pady=5)


def open_chat():
    user_label.config(text=f"Logged in as {state.username}")
    show_frame(chat_frame)


# ─────────── Start ───────────
show_frame(login_frame)
root.mainloop()
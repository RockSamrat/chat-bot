import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from datetime import datetime

SERVER_URL = "http://localhost:5000"


# ─────────── App State ───────────
class AppState:
    def __init__(self):
        self.token = None
        self.username = None

    def set_logged_in(self, token, username):
        self.token = token
        self.username = username

    def logout(self):
        self.token = None
        self.username = None

    @property
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}


state = AppState()


# ─────────── Main Window ───────────
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("520x650")
root.configure(bg="#f5f5f5")
root.resizable(False, False)

BG_MAIN = "#f5f5f5"
CARD_BG = "white"
TEXT = "black"
SUBTEXT = "#6b7280"
ENTRY_BG = "#fafafa"
ENTRY_BORDER = "#d1d5db"
BTN_BG = "#1f1f1f"
BTN_HOVER = "#333333"
BTN_FG = "white"
LINK = "#2563eb"
ERROR = "#dc2626"

# Bubble colors
USER_BUBBLE_BG = "#1f1f1f"
USER_BUBBLE_FG = "white"
BOT_BUBBLE_BG = "#f0f0f0"
BOT_BUBBLE_FG = "#1a1a1a"
TIMESTAMP_COLOR = "#9ca3af"


# ─────────── Styles ───────────
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Custom.TEntry",
    fieldbackground=ENTRY_BG,
    background=ENTRY_BG,
    foreground="black",
    bordercolor=ENTRY_BORDER,
    lightcolor=ENTRY_BORDER,
    darkcolor=ENTRY_BORDER,
    borderwidth=1,
    relief="solid",
    padding=(12, 0),
    font=("Segoe UI", 11)
)


def make_dark_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=BTN_BG,
        fg=BTN_FG,
        activebackground=BTN_HOVER,
        activeforeground=BTN_FG,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=14
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_BG))
    return btn


def make_link_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=CARD_BG,
        fg=LINK,
        activebackground=CARD_BG,
        activeforeground=LINK,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10)
    )


def create_labeled_entry(parent, placeholder="", show=None):
    entry = ttk.Entry(parent, style="Custom.TEntry", show=show)
    entry.pack(fill="x", pady=8, ipady=4)
    entry.insert(0, placeholder)
    entry.configure(foreground="#9ca3af")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground="black")
            if show:
                entry.configure(show=show)

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(foreground="#9ca3af")
            if show:
                entry.configure(show="")

    if show:
        entry.configure(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    return entry


# ─────────── Container ───────────
container = tk.Frame(root, bg=BG_MAIN)
container.pack(fill="both", expand=True)


def show_frame(frame):
    for widget in container.winfo_children():
        widget.pack_forget()
    frame.pack(fill="both", expand=True)


# ─────────── Register Frame ───────────
register_frame = tk.Frame(container, bg=BG_MAIN)

register_card = tk.Frame(register_frame, bg=CARD_BG, width=420, height=560)
register_card.place(relx=0.5, rely=0.5, anchor="center")
register_card.pack_propagate(False)

tk.Label(
    register_card,
    text="Create a free account",
    bg=CARD_BG,
    fg=TEXT,
    font=("Segoe UI", 24, "bold")
).pack(pady=(35, 10))

signin_row = tk.Frame(register_card, bg=CARD_BG)
signin_row.pack()

tk.Label(
    signin_row,
    text="Already have an account?",
    bg=CARD_BG,
    fg=SUBTEXT,
    font=("Segoe UI", 11)
).pack(side="left")

make_link_button(signin_row, "Sign in", lambda: show_frame(login_frame)).pack(side="left", padx=(4, 0))

google_btn = tk.Button(
    register_card,
    text="Sign up with Google",
    bg="white",
    fg=TEXT,
    relief="solid",
    bd=1,
    font=("Segoe UI", 11),
    cursor="hand2",
    padx=10,
    pady=12
)
google_btn.pack(fill="x", padx=38, pady=(25, 20))

or_row = tk.Frame(register_card, bg=CARD_BG)
or_row.pack(fill="x", padx=38, pady=(0, 18))

tk.Frame(or_row, bg="#e5e7eb", height=1).pack(side="left", fill="x", expand=True, pady=10)
tk.Label(or_row, text="or", bg=CARD_BG, fg=SUBTEXT, font=("Segoe UI", 11)).pack(side="left", padx=18)
tk.Frame(or_row, bg="#e5e7eb", height=1).pack(side="left", fill="x", expand=True, pady=10)

form_frame = tk.Frame(register_card, bg=CARD_BG)
form_frame.pack(fill="x", padx=38)

reg_name = create_labeled_entry(form_frame, "Your name (optional)")
reg_user = create_labeled_entry(form_frame, "Email address")
reg_pass = create_labeled_entry(form_frame, "Password", show="*")

reg_error = tk.Label(register_card, text="", bg=CARD_BG, fg=ERROR, font=("Segoe UI", 10))
reg_error.pack(pady=(8, 0))


def register():
    username = reg_user.get().strip()
    password = reg_pass.get().strip()

    if username in ["", "Email address"] or password in ["", "Password"]:
        reg_error.config(text="Please fill all required fields")
        return

    try:
        r = requests.post(
            f"{SERVER_URL}/api/auth/register",
            json={"username": username, "password": password}
        )
        data = r.json()

        if r.status_code == 201:
            state.set_logged_in(data["token"], data["username"])
            open_chat()
        else:
            reg_error.config(text=data.get("error", "Registration failed"))
    except Exception:
        reg_error.config(text="Cannot reach server")


make_dark_button(register_card, "Sign up", register).pack(fill="x", padx=38, pady=(22, 16))

tk.Label(
    register_card,
    text="By signing up to create an account, you are\naccepting our terms of service and privacy policy",
    bg=CARD_BG,
    fg=SUBTEXT,
    font=("Segoe UI", 9),
    justify="center"
).pack(pady=(0, 10))


# ─────────── Login Frame ───────────
login_frame = tk.Frame(container, bg=BG_MAIN)

login_card = tk.Frame(login_frame, bg=CARD_BG, width=420, height=500)
login_card.place(relx=0.5, rely=0.5, anchor="center")
login_card.pack_propagate(False)

tk.Label(
    login_card,
    text="Sign in",
    bg=CARD_BG,
    fg=TEXT,
    font=("Segoe UI", 24, "bold")
).pack(pady=(45, 12))

signup_row = tk.Frame(login_card, bg=CARD_BG)
signup_row.pack()

tk.Label(
    signup_row,
    text="Don't have an account?",
    bg=CARD_BG,
    fg=SUBTEXT,
    font=("Segoe UI", 11)
).pack(side="left")

make_link_button(signup_row, "Sign up", lambda: show_frame(register_frame)).pack(side="left", padx=(4, 0))

login_form = tk.Frame(login_card, bg=CARD_BG)
login_form.pack(fill="x", padx=38, pady=(30, 0))

login_user = create_labeled_entry(login_form, "Email address")
login_pass = create_labeled_entry(login_form, "Password", show="*")

login_error = tk.Label(login_card, text="", bg=CARD_BG, fg=ERROR, font=("Segoe UI", 10))
login_error.pack(pady=(12, 0))


def login():
    username = login_user.get().strip()
    password = login_pass.get().strip()

    if username in ["", "Email address"] or password in ["", "Password"]:
        login_error.config(text="Please enter email and password")
        return

    try:
        r = requests.post(
            f"{SERVER_URL}/api/auth/login",
            json={"username": username, "password": password}
        )
        data = r.json()

        if r.status_code == 200:
            state.set_logged_in(data["token"], data["username"])
            open_chat()
        else:
            login_error.config(text=data.get("error", "Login failed"))
    except Exception:
        login_error.config(text="Cannot reach server")


make_dark_button(login_card, "Sign in", login).pack(fill="x", padx=38, pady=(25, 0))


# ─────────── Chat Frame ───────────
chat_frame = tk.Frame(container, bg=BG_MAIN)

chat_card = tk.Frame(chat_frame, bg="white")
chat_card.pack(fill="both", expand=True, padx=20, pady=20)

top_bar = tk.Frame(chat_card, bg="white")
top_bar.pack(fill="x", padx=20, pady=20)

user_label = tk.Label(top_bar, text="", bg="white", fg="black", font=("Segoe UI", 11, "bold"))
user_label.pack(side="left")


def logout():
    state.logout()
    show_frame(login_frame)


make_dark_button(top_bar, "Logout", logout).pack(side="right")

# ─────────── Chat Bubble Canvas ───────────
chat_canvas = tk.Canvas(chat_card, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_card, orient="vertical", command=chat_canvas.yview)
chat_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y", padx=(0, 20))
chat_canvas.pack(fill="both", expand=True, padx=(20, 0), pady=(0, 10))

bubble_frame = tk.Frame(chat_canvas, bg="white")
bubble_window = chat_canvas.create_window((0, 0), window=bubble_frame, anchor="nw")


def on_frame_configure(event):
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))


def on_canvas_configure(event):
    chat_canvas.itemconfig(bubble_window, width=event.width)


bubble_frame.bind("<Configure>", on_frame_configure)
chat_canvas.bind("<Configure>", on_canvas_configure)


def scroll_to_bottom():
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)


loading_label = None


def add_bubble(sender, message, is_user=False):
    """Add a chat bubble to the chat area."""
    now = datetime.now().strftime("%I:%M %p")

    outer = tk.Frame(bubble_frame, bg="white")
    outer.pack(fill="x", pady=4, padx=10)

    if is_user:
        # Timestamp right-aligned
        ts = tk.Label(outer, text=now, bg="white", fg=TIMESTAMP_COLOR, font=("Segoe UI", 8))
        ts.pack(anchor="e", padx=6, pady=(0, 2))

        bubble = tk.Label(
            outer,
            text=message,
            bg=USER_BUBBLE_BG,
            fg=USER_BUBBLE_FG,
            font=("Segoe UI", 11),
            wraplength=310,
            justify="left",
            padx=14,
            pady=10
        )
        bubble.pack(anchor="e")
    else:
        # Timestamp left-aligned
        ts = tk.Label(outer, text=f"Bot · {now}", bg="white", fg=TIMESTAMP_COLOR, font=("Segoe UI", 8))
        ts.pack(anchor="w", padx=6, pady=(0, 2))

        bubble = tk.Label(
            outer,
            text=message,
            bg=BOT_BUBBLE_BG,
            fg=BOT_BUBBLE_FG,
            font=("Segoe UI", 11),
            wraplength=310,
            justify="left",
            padx=14,
            pady=10
        )
        bubble.pack(anchor="w")

    scroll_to_bottom()
    return bubble


def show_loading():
    """Show a typing... indicator."""
    global loading_label
    outer = tk.Frame(bubble_frame, bg="white")
    outer.pack(fill="x", pady=4, padx=10)
    outer.pack_info()  # ensure it's tracked

    loading_label = tk.Label(
        outer,
        text="Bot is typing...",
        bg=BOT_BUBBLE_BG,
        fg=TIMESTAMP_COLOR,
        font=("Segoe UI", 10, "italic"),
        padx=14,
        pady=10
    )
    loading_label.pack(anchor="w")
    scroll_to_bottom()
    return outer


def remove_loading(loading_outer):
    """Remove the typing indicator."""
    loading_outer.destroy()


# ─────────── Input Bar ───────────
bottom_bar = tk.Frame(chat_card, bg="white")
bottom_bar.pack(fill="x", padx=20, pady=(0, 20))

input_container = tk.Frame(bottom_bar, bg="#f0f0f0", highlightbackground="#d1d5db", highlightthickness=1)
input_container.pack(side="left", fill="x", expand=True, padx=(0, 10))

input_box = tk.Entry(
    input_container,
    font=("Segoe UI", 11),
    bg="#f0f0f0",
    fg="black",
    relief="flat",
    bd=0,
    insertbackground="black"
)
input_box.pack(fill="x", expand=True, padx=12, pady=10)

input_box.bind("<FocusIn>", lambda e: input_container.config(highlightbackground="#1f1f1f"))
input_box.bind("<FocusOut>", lambda e: input_container.config(highlightbackground="#d1d5db"))


def send(event=None):
    msg = input_box.get().strip()
    if not msg:
        return

    input_box.delete(0, tk.END)
    add_bubble("You", msg, is_user=True)

    # Show loading indicator
    loading_outer = show_loading()
    root.update()

    try:
        r = requests.post(
            f"{SERVER_URL}/api/chat",
            json={"question": msg},
            headers=state.auth_headers
        )
        data = r.json()
        response = data.get("response", "No response")
    except Exception:
        response = "Error connecting to server."

    remove_loading(loading_outer)
    add_bubble("Bot", response, is_user=False)


send_btn = tk.Button(
    bottom_bar,
    text="Send →",
    command=send,
    bg=BTN_BG,
    fg=BTN_FG,
    activebackground=BTN_HOVER,
    activeforeground=BTN_FG,
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=16,
    pady=10
)
send_btn.bind("<Enter>", lambda e: send_btn.config(bg=BTN_HOVER))
send_btn.bind("<Leave>", lambda e: send_btn.config(bg=BTN_BG))
send_btn.pack(side="right")

input_box.bind("<Return>", send)


def open_chat():
    # Clear previous bubbles
    for widget in bubble_frame.winfo_children():
        widget.destroy()

    user_label.config(text=f"Logged in as {state.username}")

    # Welcome message
    name = state.username.split("@")[0] if "@" in state.username else state.username
    add_bubble("Bot", f"Hi {name}! 👋 I'm your AI assistant. How can I help you today?", is_user=False)

    show_frame(chat_frame)
    input_box.focus()


show_frame(register_frame)
root.mainloop()
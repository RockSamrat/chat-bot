"""
chat-bot-gui.py  – AI Chatbot with authentication (Neon PostgreSQL + JWT)

Flow:
  1. App opens on Login screen.
  2. User logs in or registers → receives JWT from Flask server.
  3. JWT is stored in-memory; every chat request sends it in Authorization header.
  4. Logout clears the token and returns to Login screen.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests

# ── Configuration ────────────────────────────────────────────
SERVER_URL = "http://localhost:5000"   # adjust if server runs elsewhere


# ════════════════════════════════════════════════════════════
#  App State
# ════════════════════════════════════════════════════════════
class AppState:
    def __init__(self):
        self.token: str | None = None
        self.username: str | None = None
        self.context: str = ""
        self.is_responding: bool = False

    def set_logged_in(self, token: str, username: str):
        self.token = token
        self.username = username
        self.context = ""

    def logout(self):
        self.token = None
        self.username = None
        self.context = ""
        self.is_responding = False

    @property
    def auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}


state = AppState()


# ════════════════════════════════════════════════════════════
#  Main window
# ════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("640x560")
root.resizable(True, True)
root.configure(bg="#1a1a2e")

# ── Color palette ────────────────────────────────────────────
# ── Color palette ────────────────────────────────────────────
BG       = "#ffffff"
SURFACE  = "#ffffff"
CARD     = "#e0e0e0"
ACCENT   = "#000000"
ACCENT2  = "#333333"
FG       = "#000000"
FG_DIM   = "#555555"
ENTRY_BG = "#ffffff"
ERR      = "#d9534f"
OK       = "#28a745"

FONT_BODY  = ("Consolas", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_BTN   = ("Segoe UI", 11, "bold")

# ttk style
style = ttk.Style()
style.theme_use("clam")
style.configure("TEntry",
    fieldbackground=ENTRY_BG, background=ENTRY_BG,
    foreground=FG, insertcolor=FG,
    bordercolor=CARD, lightcolor=CARD, darkcolor=CARD,
    padding=8)
style.configure("TLabel", background=BG, foreground=FG, font=FONT_LABEL)
style.configure("Dim.TLabel", background=BG, foreground=FG_DIM, font=FONT_LABEL)


# ════════════════════════════════════════════════════════════
#  Helper widgets
# ════════════════════════════════════════════════════════════
def make_button(parent, text, command, color=ACCENT, fg=FG, width=None):
    kwargs = dict(bg=color, fg=fg, font=FONT_BTN, relief="flat",
                  cursor="hand2", padx=14, pady=7, bd=0,
                  activebackground=ACCENT2, activeforeground=FG,
                  command=command)
    if width:
        kwargs["width"] = width
    btn = tk.Button(parent, text=text, **kwargs)
    return btn


def make_entry(parent, show=None, width=30):
    e = ttk.Entry(parent, font=FONT_BODY, width=width, show=show or "")
    e.configure(style="TEntry")
    return e


def labeled_entry(parent, label_text, show=None):
    tk.Label(parent, text=label_text, bg=BG, fg=FG_DIM, font=FONT_LABEL).pack(anchor="w", pady=(10, 2))
    e = make_entry(parent, show=show)
    e.pack(fill="x", ipady=2)
    return e


# ════════════════════════════════════════════════════════════
#  Frames container
# ════════════════════════════════════════════════════════════
container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True)


def show_frame(frame):
    for f in container.winfo_children():
        f.pack_forget()
    frame.pack(fill="both", expand=True)


# ════════════════════════════════════════════════════════════
#  Login Frame
# ════════════════════════════════════════════════════════════
login_frame = tk.Frame(container, bg=BG)

# Card
login_card = tk.Frame(login_frame, bg=SURFACE, padx=40, pady=40,
                       relief="flat", bd=0)
login_card.place(relx=0.5, rely=0.5, anchor="center", width=380)

tk.Label(login_card, text="AI Chatbot", font=FONT_TITLE,
          bg=SURFACE, fg=ACCENT).pack(pady=(0, 4))
tk.Label(login_card, text="Sign in to continue", font=FONT_LABEL,
          bg=SURFACE, fg=FG_DIM).pack(pady=(0, 20))

login_user_entry = labeled_entry(login_card, "Username")
login_user_entry.master.configure(bg=SURFACE)
login_pass_entry = labeled_entry(login_card, "Password", show="•")
login_pass_entry.master.configure(bg=SURFACE)

# Fix label backgrounds inside card
for w in login_card.winfo_children():
    if isinstance(w, tk.Label):
        w.configure(bg=SURFACE)

login_err_label = tk.Label(login_card, text="", bg=SURFACE, fg=ERR,
                            font=FONT_LABEL, wraplength=300)
login_err_label.pack(pady=(8, 0))


def _do_login():
    username = login_user_entry.get().strip()
    password = login_pass_entry.get()
    if not username or not password:
        login_err_label.config(text="Please fill in all fields.")
        return
    login_err_label.config(text="")
    threading.Thread(target=_login_request,
                     args=(username, password), daemon=True).start()


def _login_request(username, password):
    try:
        r = requests.post(f"{SERVER_URL}/api/auth/login",
                          json={"username": username, "password": password},
                          timeout=8)
        data = r.json()
        if r.status_code == 200:
            state.set_logged_in(data["token"], data["username"])
            root.after(0, _on_login_success)
        else:
            root.after(0, login_err_label.config,
                       {"text": data.get("error", "Login failed.")})
    except requests.ConnectionError:
        root.after(0, login_err_label.config,
                   {"text": "Cannot reach server. Is server.py running?"})
    except Exception as e:
        root.after(0, login_err_label.config, {"text": str(e)})


def _on_login_success():
    login_user_entry.delete(0, "end")
    login_pass_entry.delete(0, "end")
    login_err_label.config(text="")
    chat_user_label.config(text=f"Logged in as  {state.username}")
    chat_display.config(state=tk.NORMAL)
    chat_display.delete("1.0", tk.END)
    chat_display.insert(tk.END, f"Welcome, {state.username}! Start chatting below.\n\n")
    chat_display.config(state=tk.DISABLED)
    show_frame(chat_frame)


login_btn = make_button(login_card, "Sign In", _do_login, width=20)
login_btn.pack(pady=(18, 6))

tk.Label(login_card, text="Don't have an account?", bg=SURFACE,
          fg=FG_DIM, font=FONT_LABEL).pack()


def _go_register():
    login_err_label.config(text="")
    show_frame(register_frame)


tk.Button(login_card, text="Create account →", bg=SURFACE, fg=ACCENT,
          font=("Segoe UI", 10, "bold"), relief="flat", bd=0, cursor="hand2",
          command=_go_register).pack(pady=2)

login_user_entry.bind("<Return>", lambda e: login_pass_entry.focus())
login_pass_entry.bind("<Return>", lambda e: _do_login())


# ════════════════════════════════════════════════════════════
#  Register Frame
# ════════════════════════════════════════════════════════════
register_frame = tk.Frame(container, bg=BG)

reg_card = tk.Frame(register_frame, bg=SURFACE, padx=40, pady=40,
                     relief="flat", bd=0)
reg_card.place(relx=0.5, rely=0.5, anchor="center", width=380)

tk.Label(reg_card, text="Create Account", font=FONT_TITLE,
          bg=SURFACE, fg=ACCENT).pack(pady=(0, 4))
tk.Label(reg_card, text="Join to use the AI Chatbot", font=FONT_LABEL,
          bg=SURFACE, fg=FG_DIM).pack(pady=(0, 20))

reg_user_entry = labeled_entry(reg_card, "Username")
reg_user_entry.master.configure(bg=SURFACE)
reg_pass_entry = labeled_entry(reg_card, "Password (min 8 chars)", show="•")
reg_pass_entry.master.configure(bg=SURFACE)
reg_pass2_entry = labeled_entry(reg_card, "Confirm Password", show="•")
reg_pass2_entry.master.configure(bg=SURFACE)

for w in reg_card.winfo_children():
    if isinstance(w, tk.Label):
        w.configure(bg=SURFACE)

reg_err_label = tk.Label(reg_card, text="", bg=SURFACE, fg=ERR,
                          font=FONT_LABEL, wraplength=300)
reg_err_label.pack(pady=(8, 0))


def _do_register():
    username = reg_user_entry.get().strip()
    password = reg_pass_entry.get()
    confirm  = reg_pass2_entry.get()

    if not username or not password or not confirm:
        reg_err_label.config(text="Please fill in all fields.")
        return
    if password != confirm:
        reg_err_label.config(text="Passwords do not match.")
        return

    reg_err_label.config(text="")
    threading.Thread(target=_register_request,
                     args=(username, password), daemon=True).start()


def _register_request(username, password):
    try:
        r = requests.post(f"{SERVER_URL}/api/auth/register",
                          json={"username": username, "password": password},
                          timeout=8)
        data = r.json()
        if r.status_code == 201:
            state.set_logged_in(data["token"], data["username"])
            root.after(0, _on_login_success)
            root.after(0, _clear_reg_form)
        else:
            root.after(0, reg_err_label.config,
                       {"text": data.get("error", "Registration failed.")})
    except requests.ConnectionError:
        root.after(0, reg_err_label.config,
                   {"text": "Cannot reach server. Is server.py running?"})
    except Exception as e:
        root.after(0, reg_err_label.config, {"text": str(e)})


def _clear_reg_form():
    reg_user_entry.delete(0, "end")
    reg_pass_entry.delete(0, "end")
    reg_pass2_entry.delete(0, "end")
    reg_err_label.config(text="")


make_button(reg_card, "Create Account", _do_register, width=20).pack(pady=(18, 6))

tk.Label(reg_card, text="Already have an account?", bg=SURFACE,
          fg=FG_DIM, font=FONT_LABEL).pack()
tk.Button(reg_card, text="← Back to Login", bg=SURFACE, fg=ACCENT,
          font=("Segoe UI", 10, "bold"), relief="flat", bd=0, cursor="hand2",
          command=lambda: show_frame(login_frame)).pack(pady=2)

reg_user_entry.bind("<Return>", lambda e: reg_pass_entry.focus())
reg_pass_entry.bind("<Return>", lambda e: reg_pass2_entry.focus())
reg_pass2_entry.bind("<Return>", lambda e: _do_register())


# ════════════════════════════════════════════════════════════
#  Chat Frame
# ════════════════════════════════════════════════════════════
chat_frame = tk.Frame(container, bg=BG)

# Top bar
top_bar = tk.Frame(chat_frame, bg=SURFACE, pady=8)
top_bar.pack(fill="x", padx=0)

tk.Label(top_bar, text="AI Chatbot", font=("Segoe UI", 13, "bold"),
          bg=SURFACE, fg=ACCENT).pack(side="left", padx=14)

chat_user_label = tk.Label(top_bar, text="", bg=SURFACE, fg=FG_DIM, font=FONT_LABEL)
chat_user_label.pack(side="left", padx=6)


def _logout():
    if messagebox.askyesno("Log out", "Are you sure you want to log out?"):
        state.logout()
        show_frame(login_frame)


make_button(top_bar, "Logout", _logout, color=CARD, fg=FG_DIM).pack(side="right", padx=12)

# Chat display
chat_display = scrolledtext.ScrolledText(
    chat_frame, wrap=tk.WORD, state=tk.DISABLED,
    font=FONT_BODY, bg=SURFACE, fg=FG,
    insertbackground=FG, relief="flat", bd=0,
    selectbackground=CARD, padx=14, pady=10
)
chat_display.pack(padx=10, pady=8, fill="both", expand=True)

# Color tags
chat_display.tag_config("user", foreground=OK)
chat_display.tag_config("bot",  foreground=FG)
chat_display.tag_config("err",  foreground=ERR)

# Input bar
input_bar = tk.Frame(chat_frame, bg=BG, pady=6)
input_bar.pack(fill="x", padx=10, pady=(0, 8))

user_input = tk.Entry(input_bar, font=FONT_BODY, bg=ENTRY_BG, fg=FG,
                       insertbackground=FG, relief="flat", bd=0)
user_input.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

send_button = make_button(input_bar, "Send", lambda: _on_send(), width=8)
send_button.pack(side="right")

# Status
status_label = tk.Label(chat_frame, text="Ready", bg=BG, fg=FG_DIM, font=FONT_LABEL)
status_label.pack(padx=10, pady=(0, 4), anchor="w")


# ── Chat logic ────────────────────────────────────────────────

def _append(text: str, tag: str = "bot"):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, text, tag)
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)


def _stream_response(user_text: str):
    try:
        r = requests.post(
            f"{SERVER_URL}/api/chat",
            json={"question": user_text, "context": state.context},
            headers=state.auth_headers,
            timeout=120,
        )
        data = r.json()

        if r.status_code == 401:
            root.after(0, _append, "\nSession expired. Please log in again.\n\n", "err")
            root.after(0, _logout_silently)
            return

        if r.status_code != 200:
            msg = data.get("error", "Unknown server error.")
            root.after(0, _append, f"\nError: {msg}\n\n", "err")
            return

        response_text = data.get("response", "")
        root.after(0, _append, response_text, "bot")
        root.after(0, _append, "\n\n", "bot")
        state.context += f"\nUser: {user_text}\nAI: {response_text}"

    except requests.ConnectionError:
        root.after(0, _append,
                   "\nError: Could not reach server. Is server.py running?\n\n", "err")
    except Exception as e:
        root.after(0, _append, f"\nError: {e}\n\n", "err")
    finally:
        state.is_responding = False
        root.after(0, status_label.config, {"text": "Ready"})
        root.after(0, send_button.config, {"state": tk.NORMAL})
        root.after(0, user_input.config, {"state": tk.NORMAL})
        root.after(0, user_input.focus)


def _logout_silently():
    state.logout()
    show_frame(login_frame)


def _on_send(event=None):
    if state.is_responding:
        return

    user_text = user_input.get().strip()
    if not user_text:
        return

    user_input.delete(0, tk.END)
    _append(f"You: {user_text}\n", "user")
    _append("Bot: ", "bot")

    state.is_responding = True
    status_label.config(text="Thinking…")
    send_button.config(state=tk.DISABLED)
    user_input.config(state=tk.DISABLED)

    threading.Thread(target=_stream_response, args=(user_text,), daemon=True).start()


send_button.config(command=_on_send)
user_input.bind("<Return>", _on_send)


# ════════════════════════════════════════════════════════════
#  Boot
# ════════════════════════════════════════════════════════════
show_frame(login_frame)
root.mainloop()
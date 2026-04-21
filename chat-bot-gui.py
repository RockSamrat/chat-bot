from main import chain
import tkinter as tk
from tkinter import scrolledtext
import threading

# --- Main window setup ---
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("600x500")

context = ""
is_responding = False

# --- Chat display ---
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 11))
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# --- Input box and Send button ---
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

user_input = tk.Entry(input_frame, font=("Arial", 11))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

send_button = tk.Button(input_frame, text="Send", width=8)
send_button.pack(side=tk.RIGHT)

# --- Status label ---
status_label = tk.Label(root, text="Ready", anchor="w")
status_label.pack(padx=10, pady=(0, 5), fill=tk.X)


# --- Helper: add text to chat ---
def append(text):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, text)
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)


# --- Stream bot response in background thread ---
def stream_response(user_text):
    global context, is_responding

    try:
        full_response = ""
        for chunk in chain.stream({"context": context, "question": user_text}):
            full_response += chunk
            root.after(0, append, chunk)  # update UI safely from thread

        root.after(0, append, "\n\n")
        context += f"\nUser: {user_text}\nAI: {full_response}"

    except ConnectionError:
        root.after(0, append, "Error: Could not connect to Ollama. Is it running?\n\n")
    except Exception as e:
        root.after(0, append, f"Error: {e}\n\n")
    finally:
        is_responding = False
        root.after(0, status_label.config, {"text": "Ready"})
        root.after(0, send_button.config, {"state": tk.NORMAL})
        root.after(0, user_input.config, {"state": tk.NORMAL})
        root.after(0, user_input.focus)


# --- Send button logic ---
def on_send(event=None):
    global is_responding

    if is_responding:
        return

    user_text = user_input.get().strip()
    if not user_text:
        return

    user_input.delete(0, tk.END)
    append(f"You: {user_text}\nBot: ")

    is_responding = True
    status_label.config(text="Thinking...")
    send_button.config(state=tk.DISABLED)
    user_input.config(state=tk.DISABLED)

    threading.Thread(target=stream_response, args=(user_text,), daemon=True).start()


# --- Bind Enter key and Send button ---
send_button.config(command=on_send)
user_input.bind("<Return>", on_send)
user_input.focus()

# --- Start the app ---
root.mainloop()
from main import chain
import tkinter as tk
from tkinter import scrolledtext
import threading
import time


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.root.geometry("700x520")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)

        self.context = ""
        self.is_responding = False

        self._build_ui()

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────
        header = tk.Frame(self.root, bg="#16213e", pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="⬡  AI Chatbot",
            font=("Courier New", 16, "bold"),
            fg="#00d4ff",
            bg="#16213e",
        ).pack()

        self.status_label = tk.Label(
            header,
            text="● Ready",
            font=("Courier New", 9),
            fg="#44ff88",
            bg="#16213e",
        )
        self.status_label.pack()

        # ── Chat display ─────────────────────────────────────────────
        chat_frame = tk.Frame(self.root, bg="#1a1a2e", padx=12, pady=8)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Courier New", 11),
            bg="#0f0f1a",
            fg="#e0e0e0",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            padx=10,
            pady=8,
            state=tk.DISABLED,
            borderwidth=0,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Colour tags
        self.chat_display.tag_config("user", foreground="#00d4ff")
        self.chat_display.tag_config("bot", foreground="#c0f0c0")
        self.chat_display.tag_config("meta", foreground="#666699", font=("Courier New", 9))
        self.chat_display.tag_config("error", foreground="#ff6666")
        self.chat_display.tag_config("system", foreground="#888899", font=("Courier New", 9, "italic"))

        # ── Input row ────────────────────────────────────────────────
        input_frame = tk.Frame(self.root, bg="#16213e", padx=12, pady=10)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.user_input = tk.Entry(
            input_frame,
            font=("Courier New", 12),
            bg="#0f0f1a",
            fg="#e0e0e0",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            bd=0,
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
        self.user_input.bind("<Return>", self._on_send)
        self.user_input.bind("<Shift-Return>", lambda e: None)  # allow shift-enter later
        self.user_input.focus()

        self.send_btn = tk.Button(
            input_frame,
            text="Send ▶",
            font=("Courier New", 11, "bold"),
            bg="#00d4ff",
            fg="#0f0f1a",
            activebackground="#0099cc",
            activeforeground="#0f0f1a",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self._on_send,
        )
        self.send_btn.pack(side=tk.RIGHT)

        # Clear button
        tk.Button(
            input_frame,
            text="Clear",
            font=("Courier New", 10),
            bg="#333355",
            fg="#aaaacc",
            activebackground="#444466",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self._clear_chat,
        ).pack(side=tk.RIGHT, padx=(0, 6))

        # Welcome message
        self._append("system", "Welcome! Type a message and press Enter or click Send.\n\n")

    # ── Helpers ──────────────────────────────────────────────────────

    def _append(self, tag, text):
        """Thread-safe append to chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def _set_status(self, text, color):
        self.status_label.config(text=text, fg=color)

    def _set_ui_busy(self, busy: bool):
        self.is_responding = busy
        state = tk.DISABLED if busy else tk.NORMAL
        self.send_btn.config(state=state)
        self.user_input.config(state=state)
        if busy:
            self._set_status("● Thinking…", "#ffcc00")
        else:
            self._set_status("● Ready", "#44ff88")
            self.user_input.focus()

    def _clear_chat(self):
        if self.is_responding:
            return
        self.context = ""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._append("system", "Conversation cleared.\n\n")

    # ── Send logic ───────────────────────────────────────────────────

    def _on_send(self, event=None):
        if self.is_responding:
            return
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.user_input.delete(0, tk.END)
        self._append("user", f"You: {user_text}\n")
        self._set_ui_busy(True)

        threading.Thread(
            target=self._stream_response,
            args=(user_text,),
            daemon=True,
        ).start()

    def _stream_response(self, user_text: str):
        try:
            self.root.after(0, self._append, "bot", "Bot: ")
            full_response = ""
            start = time.time()

            for chunk in chain.stream({"context": self.context, "question": user_text}):
                full_response += chunk
                self.root.after(0, self._append, "bot", chunk)

            elapsed = time.time() - start
            self.root.after(0, self._append, "meta", f"\n  (responded in {elapsed:.2f}s)\n\n")
            self.context += f"\nUser: {user_text}\nAI: {full_response}"

        except ConnectionError:
            self.root.after(
                0, self._append, "error",
                "\nError: Could not connect to Ollama. Is it running?\n\n"
            )
        except Exception as exc:
            self.root.after(
                0, self._append, "error",
                f"\nSomething went wrong: {exc}\n\n"
            )
        finally:
            self.root.after(0, self._set_ui_busy, False)


def main():
    root = tk.Tk()
    ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
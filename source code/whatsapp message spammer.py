import tkinter as tk
from tkinter import ttk
import webbrowser
import pyautogui
import time

# Enable the hard-kill switch (slam mouse to screen corner to stop)
pyautogui.FAILSAFE = True

# Initialize the main window
root = tk.Tk()
root.title("whatsapp message spammer")
root.geometry("450x550")  # Set a nice default window size

# --- UI COLOR PALETTE ---
BG_COLOR = "#E8F5E9"  # Very light mint green background
TEXT_COLOR = "#1B5E20"  # Dark forest green for text
BTN_COLOR = "#4CAF50"  # Primary bright green for buttons
BTN_HOVER = "#388E3C"  # Darker green for when you hover/click buttons
LIST_BG = "#F1F8E9"  # Slightly off-white green for the text box

root.configure(bg=BG_COLOR)

# --- STYLE CONFIGURATION ---
style = ttk.Style()
# 'clam' theme allows us to easily change background colors of buttons and remove 3D borders
style.theme_use('clam')

style.configure("TFrame", background=BG_COLOR)

style.configure("TLabel",
                background=BG_COLOR,
                foreground=TEXT_COLOR,
                font=("Segoe UI", 11, "bold"))

style.configure("TButton",
                background=BTN_COLOR,
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                borderwidth=0,
                padding=8)
style.map("TButton", background=[("active", BTN_HOVER)])

style.configure("TEntry",
                fieldbackground="white",
                foreground=TEXT_COLOR,
                font=("Segoe UI", 11),
                borderwidth=0,
                padding=5)

# State variables
step = 1
phone_number = ""
msg = ""
is_sending = False
msg_count = 0


def on_press_entry_btn():
    global step, phone_number, msg, msg_count

    input_text = entry1.get()

    if not input_text:
        return

    if step == 1:
        phone_number = input_text
        text_list.insert(tk.END, f"📱 Phone: {phone_number}")
        entry1.delete(0, tk.END)
        lbl1.configure(text="Enter your message:")
        step = 2

    elif step == 2:
        msg = input_text
        text_list.insert(tk.END, f"💬 Msg: {msg}")
        entry1.delete(0, tk.END)
        lbl1.configure(text="How many times to send?")
        step = 3

    elif step == 3:
        try:
            msg_count = int(input_text)
            text_list.insert(tk.END, f"🔁 Ready to send {msg_count} times.")
            entry1.delete(0, tk.END)
            lbl1.configure(text="Configuration set! Press 'Start' to begin.")
        except ValueError:
            lbl1.configure(text="Error: Please enter a whole number!")


def start_sending_process():
    global is_sending

    if is_sending:
        is_sending = False
        time.sleep(0.5)

    is_sending = True

    try:
        text_list.insert(tk.END, "🌐 Opening WhatsApp Web...")
        web_url = f"https://web.whatsapp.com/send?phone={phone_number}"
        webbrowser.open(web_url)

        text_list.insert(tk.END, "⏳ Waiting 15s for WhatsApp to load...")
        root.update()
        time.sleep(6)

        for i in range(msg_count):
            # Check if active window is a web browser (where WhatsApp runs)
            active_window = pyautogui.getActiveWindow()
            if active_window is None or not any(
                    browser in active_window.title.lower()
                    for browser in ["chrome", "brave", "edge", "firefox", "whatsapp"]
            ):
                is_sending = False
                text_list.insert(tk.END, "🛑 Stopped cause of you not being in the whatsapp tab")
                text_list.yview(tk.END)
                lbl1.configure(text="Stopped! Start again or Configure new values:")
                break

            if not is_sending:
                text_list.insert(tk.END, "🛑 Sending cancelled.")
                text_list.yview(tk.END)
                break

            pyautogui.write(msg)
            time.sleep(0.00001)
            pyautogui.press("enter")

            text_list.insert(tk.END, f"✅ Sent message {i + 1} of {msg_count}")
            text_list.yview(tk.END)  # Auto-scroll to bottom
            root.update()
            time.sleep(0.00001)

        if is_sending:
            is_sending = False
            lbl1.configure(text="Finished! Start again or Configure new values:")

    except pyautogui.FailSafeException:
        is_sending = False
        text_list.insert(tk.END, "⚠️ Mouse Failsafe Triggered! Stopped.")
        text_list.yview(tk.END)
        lbl1.configure(text="Emergency Stop! Check your windows.")

    except Exception as e:
        lbl1.configure(text="Error occurred during sending.")


def stop_sending():
    global is_sending
    is_sending = False
    text_list.insert(tk.END, "🛑 Stopped by user.")
    text_list.yview(tk.END)
    lbl1.configure(text="Stopped! Start again or Configure new values:")


def reset_fields():
    global step, phone_number, msg, msg_count, is_sending
    step = 1
    phone_number = ""
    msg = ""
    msg_count = 0
    is_sending = False
    entry1.delete(0, tk.END)
    text_list.insert(tk.END, "--- 🔄 Config Cleared ---")
    text_list.yview(tk.END)
    lbl1.configure(text="Enter phone number (e.g., +972501234567):")


# --- LAYOUT SETUP ---
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Main container with padding to let the UI breathe
frame1 = ttk.Frame(root)
frame1.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
frame1.columnconfigure(0, weight=1)

# Input Field
entry1 = ttk.Entry(frame1)
entry1.grid(row=0, column=0, sticky="ew", pady=(0, 10))
entry1.bind("<Return>", lambda event: on_press_entry_btn())

# Next Button
entry1_btn = ttk.Button(frame1, text="Next ➔", command=on_press_entry_btn)
entry1_btn.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))

# Status Listbox (Custom styled using standard tk to match the flat green theme)
text_list = tk.Listbox(frame1,
                       bg=LIST_BG,
                       fg=TEXT_COLOR,
                       font=("Segoe UI", 10),
                       selectbackground=BTN_COLOR,
                       relief="flat",
                       borderwidth=0,
                       highlightthickness=1,
                       highlightcolor=BTN_COLOR,
                       highlightbackground="#C8E6C9")
text_list.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(5, 15))
frame1.rowconfigure(1, weight=1)  # Makes the listbox expand to fill space

# Instruction Label
lbl1 = ttk.Label(frame1, text="Enter phone number (e.g., +972501234567):")
lbl1.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 10))

# Action Buttons Container
btn_frame = ttk.Frame(frame1)
btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
btn_frame.columnconfigure(0, weight=1)
btn_frame.columnconfigure(1, weight=1)
btn_frame.columnconfigure(2, weight=1)

# Action Buttons
start_btn = ttk.Button(btn_frame, text="▶ Start", command=start_sending_process)
start_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

stop_btn = ttk.Button(btn_frame, text="⬛ Stop", command=stop_sending)
stop_btn.grid(row=0, column=1, sticky="ew", padx=(5, 5))

configure_btn = ttk.Button(btn_frame, text="⚙ Configure", command=reset_fields)
configure_btn.grid(row=0, column=2, sticky="ew", padx=(5, 0))

root.mainloop()
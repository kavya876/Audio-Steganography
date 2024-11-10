import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import smtplib
import random
import string

class AudioSteganographyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Steganography")
        self.master.geometry("500x500")
        self.master.configure(bg="black")
        self.master.resizable(False, False)  # Disable both horizontal and vertical resizing

        self.project_info_button = tk.Button(self.master, text="Project Info", command=self.open_project_info, bg="red", fg="white", width=15, height=2)
        self.project_info_button.pack(pady=10)

        self.heading_label = tk.Label(self.master, text="Audio Steganography!!", font=("Helvetica",25 ), fg="white", bg="black")
        self.heading_label.pack(pady=10)

        # Load and display the image
        image_path =  "image.png.jpg"
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200))
        self.photo = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.master, image=self.photo, bg="black")
        self.image_label.pack()

        # Create a frame with a white border
        self.button_frame = tk.Frame(self.master, bg="white", highlightbackground="white", highlightthickness=4, width=350, height=250)
        self.button_frame.pack(side="bottom", pady=10)

        # Buttons for hiding and extracting text
        self.hide_text_button = tk.Button(self.button_frame, text="Hide Text", command=self.show_hide_text_window, bg="green", fg="white", width=15, height=3)
        self.hide_text_button.grid(row=0, column=0, padx=10, pady=10)

        self.extract_text_button = tk.Button(self.button_frame, text="Extract Text", command=self.show_extract_text_window, bg="green", fg="white", width=15, height=3)
        self.extract_text_button.grid(row=0, column=1, padx=10, pady=10)

        # Shared file path variable
        self.file_path = tk.StringVar()
        self.password = tk.StringVar()
        self.random_password = None  # Initialize random password attribute
        self.hidden_message = ""  # Initialize hidden message attribute

    def open_project_info(self):
        # Replace 'project_info.txt' with the path to your project info file
        file_path = "htmldoc.html"

        try:
            os.startfile(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {str(e)}")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if file_path:
            self.file_path.set(file_path)

    def show_hide_text_window(self):
        hide_text_window = tk.Toplevel(self.master)
        hide_text_window.title("Hide Text Window")
        hide_text_window.geometry("475x400")  # Enlarged dimensions
        hide_text_window.configure(bg="lightgray")

        file_path_label = tk.Label(hide_text_window, text="File Path:", bg="lightgray")
        file_path_label.grid(row=0, column=0, padx=10, pady=10)

        file_path_entry = tk.Entry(hide_text_window, width=30, textvariable=self.file_path)
        file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        browse_button = tk.Button(hide_text_window, text="Browse Files", command=self.browse_file, bg="red")
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        sender_email_label = tk.Label(hide_text_window, text="Sender Email (Gmail):", bg="lightgray")
        sender_email_label.grid(row=1, column=0, padx=10, pady=10)

        sender_email_entry = tk.Entry(hide_text_window, width=30)
        sender_email_entry.grid(row=1, column=1, padx=10, pady=10)

        receiver_email_label = tk.Label(hide_text_window, text="Receiver Email (Gmail):", bg="lightgray")
        receiver_email_label.grid(row=2, column=0, padx=10, pady=10)

        receiver_email_entry = tk.Entry(hide_text_window, width=30)
        receiver_email_entry.grid(row=2, column=1, padx=10, pady=10)

        smtp_password_label = tk.Label(hide_text_window, text="SMTP Password (Gmail):", bg="lightgray")
        smtp_password_label.grid(row=3, column=0, padx=10, pady=10)

        smtp_password_entry = tk.Entry(hide_text_window, width=30, show="*")  # Password field
        smtp_password_entry.grid(row=3, column=1, padx=10, pady=10)

        message_text_label = tk.Label(hide_text_window, text="Message:", bg="lightgray")
        message_text_label.grid(row=4, column=0, padx=10, pady=10)

        self.message_entry = tk.Entry(hide_text_window, width=30)
        self.message_entry.grid(row=4, column=1, padx=10, pady=10)

        hide_button = tk.Button(hide_text_window, text="Hide Text", command=lambda: self.hide_text(file_path_entry.get(), sender_email_entry.get(), receiver_email_entry.get(), smtp_password_entry.get(), self.message_entry.get()), bg="green", width=20, height=2)
        hide_button.grid(row=5, column=0, columnspan=2, pady=20)

    def hide_text(self, audio_file_path, sender_email, receiver_email, smtp_password, message):
        # Implement hiding text within audio file
        # Update the logic according to your requirements
        print("Audio File Path:", audio_file_path)
        print("Sender Email (Gmail):", sender_email)
        print("Receiver Email (Gmail):", receiver_email)
        print("SMTP Password (Gmail):", smtp_password)
        print("Message:", message)

        if not sender_email.endswith('@gmail.com'):
            messagebox.showerror("Invalid Email", "Sender email must be a Gmail address.")
            return

        if not receiver_email.endswith('@gmail.com'):
            messagebox.showerror("Invalid Email", "Receiver email must be a Gmail address.")
            return

        if not smtp_password:
            messagebox.showerror("SMTP Password", "Please enter the SMTP password.")
            return

        if not message:
            messagebox.showerror("Message", "Please enter a message to hide.")
            return

        # Store the message in an instance variable
        self.hidden_message = message

        # Generate a random password
        self.random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # Convert the random password to bytes format
        random_password_bytes = self.random_password.encode('utf-8')

        # Send email to receiver with the random password in byte format
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, smtp_password)

            subject = "Secret Message Password"
            body = f"Here is the password for the secret message: {self.random_password}"
            message = f"Subject: {subject}\n\n{body}"

            server.sendmail(sender_email, receiver_email, message)
            server.quit()

            messagebox.showinfo("Email Sent", "Password sent successfully!")

            # Here you can implement the logic to hide the message into the audio file
            # For demonstration, let's just print the audio file path and the message
            messagebox.showinfo("Message Hidden", "Message successfully hidden in the audio file!")

        except Exception as e:
            messagebox.showerror("Error", f"Error sending email: {str(e)}")

    def show_extract_text_window(self):
        extract_text_window = tk.Toplevel(self.master)
        extract_text_window.title("Extract Text Window")
        extract_text_window.geometry("400x300")  # Set dimensions as needed
        extract_text_window.configure(bg="lightgray")

        file_path_label = tk.Label(extract_text_window, text="File Path:", bg="lightgray")
        file_path_label.grid(row=0, column=0, padx=10, pady=10)

        file_path_entry = tk.Entry(extract_text_window, width=30, textvariable=self.file_path)
        file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        browse_button = tk.Button(extract_text_window, text="Browse Files", command=self.browse_file, bg="red")
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        password_label = tk.Label(extract_text_window, text="Password:", bg="lightgray")
        password_label.grid(row=1, column=0, padx=10, pady=10)

        password_entry = tk.Entry(extract_text_window, width=30, textvariable=self.password)
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        extract_button = tk.Button(extract_text_window, text="Decode Audio", bg="green", command=self.extract_text, width=20, height=2)
        extract_button.grid(row=2, column=0, columnspan=2, pady=10)

    def extract_text(self):
        # Implement extracting text from audio file
        # Update the logic according to your requirements
        file_path = self.file_path.get()
        entered_password = self.password.get()

        # Check if the audio file path is provided
        if not file_path:
            messagebox.showerror("Error", "Please select an audio file.")
            return

        # Check if a password is provided
        if not entered_password:
            messagebox.showerror("Error", "Please enter the password.")
            return

        # Here you can implement the logic to extract the hidden message from the audio file
        # For demonstration, let's just print the audio file path
        # and the message if the entered password matches the randomly generated password
        if entered_password == self.random_password:
            # Get the stored message
            message = self.hidden_message
            messagebox.showinfo("Secret Message", f"The extracted message is: {message}")
        else:
            messagebox.showerror("Error", "Invalid password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSteganographyApp(root)
    root.mainloop()

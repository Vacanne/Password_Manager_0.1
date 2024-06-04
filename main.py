from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# Default email
DEFAULT_MAIL = "defaultmail@gmail.com"
DATA_FILE = "data.json"  # Constant for data file path

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Generate a random password
def generate_password():
    # Define possible characters
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    # Generate random components
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    # Combine and shuffle components
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    # Create final password and insert it into the entry field
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)  # Copy to clipboard

# ---------------------------- SAVE PASSWORD ------------------------------- #

# Save the entered password to a file
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # Check if any field is empty
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        # Confirm with the user
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                # Read existing data
                with open(DATA_FILE, "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                # If file not found, create it
                data = new_data
            else:
                # Update existing data with new entry
                data.update(new_data)

            # Write updated data back to file
            with open(DATA_FILE, "w") as data_file:
                json.dump(data, data_file, indent=4)

            # Clear the website and password fields
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #

# Find and display the password for the entered website
def find_password():
    website = website_entry.get()
    try:
        # Read data from file
        with open(DATA_FILE) as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        # Check if the website exists in the data
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No information found for {website}")

# ---------------------------- UI SETUP ------------------------------- #

# Create main window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Add canvas with logo
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=25)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=48)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, DEFAULT_MAIL)
password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password, width=18)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=41, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=18, command=find_password)
search_button.grid(row=1, column=2)

# Start the main loop
window.mainloop()

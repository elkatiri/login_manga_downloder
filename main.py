import requests
from bs4 import BeautifulSoup
import os
from io import BytesIO
from PIL import Image
import re
import csv
from customtkinter import *

# Function to scrape manga chapter images
def scrape_manga_chapter(chapter_number, base_folder='downloaded_images'):
    # Construct the URL with the chapter number
    url = f'https://3asq.org/manga/jujutsu-kaisen-2/{chapter_number}/'

    # Make a GET request to the webpage
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch the webpage. {e}")
        return []

    # Create a base folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Create a subfolder for the current chapter
    chapter_folder = os.path.join(base_folder, f'chapter_{chapter_number}')
    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags within elements with the specified class
    images = soup.select('.page-break img.wp-manga-chapter-img')

    # Download and save the images to the folder
    downloaded_images = []
    for i, image in enumerate(images):
        # Get the image data
        image_url = image['src']
        try:
            response = requests.get(image_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to download image. {e}")
            continue

        # Save the image to the subfolder
        image_filename = os.path.join(chapter_folder, f'image{i + 1}.jpg')
        with open(image_filename, 'wb') as f:
            f.write(response.content)
            downloaded_images.append(image_filename)

    return downloaded_images

# Initialize the Tkinter app
app = CTk()
app.title("Download Manga App")
app.iconbitmap("animelek_logo.ico")
app.minsize(800, 600)
app.maxsize(800, 600)
# dark mode
set_appearance_mode("system")  # default
set_appearance_mode("dark")

# Images
side_img_data = Image.open("gojo_satoro.png")
email_icon_data = Image.open("email-icon.png")
password_icon_data = Image.open("password-icon.png")
google_icon_data = Image.open("google-icon.png")

# CTkImage instances
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

# CTkLabel and CTkEntry instances
CTkLabel(app, text="", image=side_img).pack(expand=True, side="left")
frame = CTkFrame(app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")
CTkLabel(frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
CTkLabel(frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
email_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
email_entry.pack(anchor="w", padx=(25, 0))
CTkLabel(frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))
#the button login is in the bottom because we didnt initalise our fonction notyet

# Function to handle button click event
def button_click_event():
    # Get the values from email and password entry widgets
    email_value = email_entry.get()
    password_value = password_entry.get()

    # Validate email using a regular expression
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    is_valid_email = bool(email_pattern.match(email_value))

    # Validate password using a regular expression
    password_pattern = re.compile(r'^.{6,}$')
    is_valid_password = bool(password_pattern.match(password_value))

    # Check if email and password are valid
    if is_valid_email and is_valid_password:
        # Set both borders to green
        email_entry.configure(border_color="green", border_width=2)
        password_entry.configure(border_color="green", border_width=2)
        # add info to a csv file
        with open('info.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([email_value, password_value])
        # Proceed to the next window or perform any other actions
        open_next_window()
    else:
        if is_valid_password and not is_valid_email:
            email_entry.configure(border_color="red")
        elif is_valid_email and not is_valid_password:
            password_entry.configure(border_color="red")
        else:
            email_entry.configure(border_color="red")
            password_entry.configure(border_color="red")

# Function to open the next window
def open_next_window():
    # Destroy the current window if needed
    app.destroy()
    # dark mode
    set_appearance_mode("system")  # default
    set_appearance_mode("dark")
    # Create a new window
    next_window = CTk()
    next_window.title("Downloader Manga")
    next_window.iconbitmap("animelek_logo.ico")
    # min and max size
    next_window.minsize(800, 600)
    next_window.maxsize(800, 600)

    # Add widgets and configurations for the new window as needed
    # sokona slide image
    side_img_data = Image.open("sokona.png")
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    CTkLabel(next_window, text="", image=side_img).pack(expand=True, side="left")
    # create frame
    myframe = CTkFrame(next_window, width=340, height=480, fg_color="#ffffff")
    myframe.pack_propagate(0)
    myframe.pack(expand=True, side="right")
    myurl = StringVar()

    # Welcome message with a Japanese greeting "こんにちは=konnichiwa"
    hi_img_data = Image.open("hi2.jpg")
    hi_img = CTkImage(dark_image=hi_img_data, light_image=hi_img_data, size=(50, 50))
    CTkLabel(myframe, text="こんにちは!  ", image=hi_img, compound="right", font=("Arial Bold", 24),
    text_color="#601E88").pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(myframe, text="Enjouy Using My App", text_color="#7E7E7E", anchor="w", justify="left",
    font=("Arial Bold", 16)).pack(anchor="w", pady=(10, 5), padx=(25, 0))
    # label url
    url_label = CTkLabel(myframe, text="Your URL From 3asq Manga", text_color="#601E88", anchor="w", justify="center",
    font=("Arial Bold", 17))
    url_label.pack(pady=(38, 0))
    myurl.set("https://3asq.org/manga/jujutsu-kaisen-2/number/")
    url_entry = CTkEntry(myframe, text_color="#601E88", width=300, height=40, fg_color="#EEEEEE",
    border_color="#601E88",
    border_width=1, textvariable=myurl)
    url_entry.pack(anchor="w", pady=(20, 0), padx=(20, 0), ipadx=4, ipady=2)
    # download button
    download_button = CTkButton(myframe, text="download", fg_color="#601E88", hover_color="#E44982",
    font=("Arial Bold", 14), text_color="#ffffff", width=225)
    download_button.pack(anchor="w", pady=(30, 0), padx=(55, 0), ipadx=4, ipady=2)

    # Function to handle download button click event
    def download_button_clicked():
        url_value = myurl.get()
        url_pattern = re.compile(r'^https://3asq\.org/manga/jujutsu-kaisen-2/(\d+)/$')
        match = url_pattern.match(url_value)

        if match:
            chapter_number = match.group(1)
            # Highlight the chapter number separately
            highlighted_text = f"start downloading...- Chapter {chapter_number}"
            url_label.configure(text=highlighted_text, text_color="green")
            url_entry.configure(border_color="green")
            next_window.update()
            # Call the manga scraping function
            # Call the manga scraping function
            downloaded_images = scrape_manga_chapter(chapter_number)

            # Update label with success message and downloaded image count
            success_message = f"Download successful! {len(downloaded_images)} images downloaded."
            url_label.configure(text=success_message, text_color="green")
        else:
            url_entry.configure(border_color="red")

    # Set the download_button_clicked function as the command for the download button
    download_button.configure(command=download_button_clicked)

    # Start the main loop for the new window
    next_window.mainloop()

# Set the button_click_event function as the command for the Login button
CTkButton(frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
text_color="#ffffff", width=225, command=button_click_event).pack(anchor="w", pady=(40, 0), padx=(25, 0))
CTkButton(frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#F5EEE6", font=("Arial Bold", 12),
text_color="#601E88", width=225, image=google_icon, compound="right").pack(anchor="w", pady=(20, 0),padx=(25, 0))

# Start the Tkinter main loop
app.mainloop()

import csv
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import uuid
from PIL import Image, ImageTk

# Singleton Pattern: File Handler
class FileHandler:
    _instances = {}

    @staticmethod
    def get_instance(file_name):
        if file_name not in FileHandler._instances:
            FileHandler._instances[file_name] = FileHandler(file_name)
        return FileHandler._instances[file_name]

    def __init__(self, file_name):
        if file_name in FileHandler._instances:
            raise Exception("This is a singleton class!")
        self.file_name = file_name

    def read_data(self):
        try:
            with open(self.file_name, mode="r") as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            return []

    def write_data(self, data, fieldnames):
        with open(self.file_name, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


# Base Booking Component
class Booking:
    def __init__(self, ticket_price):
        self.ticket_price = ticket_price

    def calculate_price(self):
        return self.ticket_price


# Decorator Base Class
class BookingDecorator(Booking):
    def __init__(self, booking):
        self.booking = booking

    def calculate_price(self):
        return self.booking.calculate_price()


# Snack Decorator
class SnackDecorator(BookingDecorator):
    def __init__(self, booking, snack_price):
        super().__init__(booking)
        self.snack_price = snack_price

    def calculate_price(self):
        return super().calculate_price() + self.snack_price


# Beverage Decorator
class BeverageDecorator(BookingDecorator):
    def __init__(self, booking, beverage_price):
        super().__init__(booking)
        self.beverage_price = beverage_price

    def calculate_price(self):
        return super().calculate_price() + self.beverage_price


# Factory Pattern: For UI Components
class ComponentFactory:
    @staticmethod
    def create_label(root, text, font=("Arial", 15), **kwargs):
        return tk.Label(root, text=text, font=font, **kwargs)

    @staticmethod
    def create_button(root, text, command, **kwargs):
        return tk.Button(root, text=text, command=command, **kwargs)

    @staticmethod
    def create_entry(root, **kwargs):
        return tk.Entry(root, **kwargs)

    @staticmethod
    def create_combobox(root, values, **kwargs):
        combobox = ttk.Combobox(root, values=values, **kwargs)
        return combobox


# Command Pattern: Encapsulate Operations
class Command:
    def execute(self):
        pass


class BookTicketCommand(Command):
    def __init__(self, show_id, seat_number, user_id):
        self.show_id = show_id
        self.seat_number = seat_number
        self.user_id = user_id

    def execute(self):
        seats = FileHandler.get_instance("seats.csv").read_data()
        bookings = FileHandler.get_instance("bookings.csv").read_data()

        for seat in seats:
            if seat["show_id"] == self.show_id and seat["seat_number"] == self.seat_number:
                if seat["is_booked"] == "Y":
                    messagebox.showerror("Error", "Seat already booked!")
                    return
                seat["is_booked"] = "Y"

                bookings.append({
                    "user_id": self.user_id,
                    "show_id": self.show_id,
                    "seat_number": self.seat_number,
                    "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })

                FileHandler.get_instance("seats.csv").write_data(seats, seats[0].keys())
                FileHandler.get_instance("bookings.csv").write_data(bookings, bookings[0].keys())
                messagebox.showinfo("Success", "Ticket booked successfully!")
                return

class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("900x600")
        self.root.configure(bg='#C25F5C')
        self.user_id = None
        self.show_entry_page()

    def show_entry_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()
        ComponentFactory.create_label(self.root, "Movie Ticket Booking System", font=("Arial", 20, "bold"),bg='#011838', fg='white', height =2).place(x=400, y = 40)
        ComponentFactory.create_button(self.root, "Admin", command=self.show_admin_login,height=3,width=15).place(x= 500,y=200)
        ComponentFactory.create_button(self.root, "Customer", command=self.show_customer_login,height=3,width=15).place(x= 500, y= 350)

    def show_admin_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.show_image()
        ComponentFactory.create_label(self.root, "Admin Login", font=("Arial", 18, "bold"), bg='#011838', fg='white', height =2).place(x= 600, y=100)
        tk.Label(self.root, text="Username: ",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=200)
        username_entry = ComponentFactory.create_entry(self.root)
        username_entry.place(x=670, y=200)
        tk.Label(self.root, text="Password",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=250)
        
        password_entry = ComponentFactory.create_entry(self.root, show="*")
        password_entry.place(x=670, y=250)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            users = FileHandler.get_instance("users.csv").read_data()
            for user in users:
                if user["username"] == username and user["password"] == password and user["status"] == "admin":
                    self.show_admin_dashboard()
                    return
            messagebox.showerror("Error", "Invalid credentials!")

        ComponentFactory.create_button(self.root, "Login", command=login,font=("Arial", 10), height =2,width=10).place(x= 630, y= 310)
        ComponentFactory.create_button(self.root, "Back", command=self.show_entry_page,font=("Arial", 10), height =2,width=10).place(x= 770, y=35)

    def show_customer_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()
        ComponentFactory.create_label(self.root, "Customer Login", font=("Arial", 18, "bold"), bg='#011838', fg='white', height =2).place(x= 600, y=100)
        tk.Label(self.root, text="Username: ",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=200)
        username_entry = ComponentFactory.create_entry(self.root)
        username_entry.place(x=670, y=200)
        tk.Label(self.root, text="Password",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=250)
        
        password_entry = ComponentFactory.create_entry(self.root, show="*")
        password_entry.place(x=670, y=250)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            users = FileHandler.get_instance("users.csv").read_data()
            for user in users:
                if user["username"] == username and user["password"] == password and user["status"] == "customer":
                    self.user_id = user["user_id"]
                    self.show_customer_dashboard()
                    return
            messagebox.showerror("Error", "Invalid credentials!")

        ComponentFactory.create_button(self.root, "Login", command=login,font=("Arial", 10), height =2,width=10).place(x= 630, y= 310)
        ComponentFactory.create_button(self.root, "Back", command=self.show_entry_page,font=("Arial", 10), height =2,width=10).place(x= 770, y=35)

    def show_admin_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()
        ComponentFactory.create_label(self.root, "Admin Dashboard", font=("Arial", 20, "bold"), bg='#011838', fg='white', height =2).place(x= 540, y=40)
        ComponentFactory.create_button(self.root, "Add Movie", command=self.add_movie,font=("Arial", 10), bg='white' ,height =2,width=10).place(x= 600, y=150)
        ComponentFactory.create_button(self.root, "Add Show", command=self.add_show,font=("Arial", 10), bg='white',  height =2,width=10).place(x= 600, y=220)
        #ComponentFactory.create_button(self.root ,"Remove show" , command = self.remove_show,font=("Arial", 10), bg='white', height =2,width=10).place(x= 600, y=360)
        ComponentFactory.create_button(self.root, "Logout", command=self.show_entry_page,font=("Arial", 10), bg='white', height =2,width=10).place(x= 600, y=360)

    def show_customer_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()
        ComponentFactory.create_label(self.root, "Customer Dashboard", font=("Arial", 20, "bold") ,bg='#011838', fg='white', height =2).place(x= 600, y=40)
        ComponentFactory.create_button(self.root, "Book Ticket", command=self.book_ticket,font=("Arial", 10), height =2,width=15).place(x= 670, y=140)
        ComponentFactory.create_button(self.root, "Display Bookings", command=self.display_bookings,font=("Arial", 10), height =2,width=15).place(x= 670, y=200)
        ComponentFactory.create_button(self.root, "Logout", command=self.show_entry_page,font=("Arial", 10), height =2,width=15).place(x= 670, y=260)

    def add_movie(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ComponentFactory.create_label(self.root, "Add Movie", font=("Arial", 20)).pack(pady=10)
        ComponentFactory.create_label(self.root, "Title").pack(pady=5)
        title_entry = ComponentFactory.create_entry(self.root)
        title_entry.pack(pady=5)
        ComponentFactory.create_label(self.root, "Duration (in minutes)").pack(pady=5)
        duration_entry = ComponentFactory.create_entry(self.root)
        duration_entry.pack(pady=5)

        def submit_movie():
            title = title_entry.get()
            duration = duration_entry.get()
            if not title or not duration.isdigit():
                messagebox.showerror("Error", "Invalid input. Title and duration must be provided.")
                return

            movies = FileHandler.get_instance("movies.csv").read_data()
            movie_id = str(uuid.uuid4())[:8]
            movies.append({"movie_id": movie_id, "title": title, "duration": duration})
            FileHandler.get_instance("movies.csv").write_data(movies, ["movie_id", "title", "duration"])

            messagebox.showinfo("Success", "Movie added successfully!")
            self.show_admin_dashboard()

        ComponentFactory.create_button(self.root, "Add Movie", command=submit_movie).pack(pady=10)
        ComponentFactory.create_button(self.root, "Back", command=self.show_admin_dashboard).pack(pady=10)

    def add_show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        movies = FileHandler.get_instance("movies.csv").read_data()
        screens = [{"screen_id": "1"}, {"screen_id": "2"}]  # Example screen data

        ComponentFactory.create_label(self.root, "Add Show", font=("Arial", 20)).pack(pady=10)
        ComponentFactory.create_label(self.root, "Select Movie").pack(pady=5)
        movie_ids = [movie["title"] for movie in movies]
        movie_combobox = ComponentFactory.create_combobox(self.root, movie_ids)
        movie_combobox.pack(pady=5)
        ComponentFactory.create_label(self.root, "Select Screen").pack(pady=5)
        screen_ids = [screen["screen_id"] for screen in screens]
        screen_combobox = ComponentFactory.create_combobox(self.root, screen_ids)
        screen_combobox.pack(pady=5)
        ComponentFactory.create_label(self.root, "Show Time (YYYY-MM-DD HH:MM)").pack(pady=5)
        showtime_entry = ComponentFactory.create_entry(self.root)
        showtime_entry.pack(pady=5)

        def submit_show():
            selected_movie = movie_combobox.get()
            selected_screen = screen_combobox.get()
            show_time = showtime_entry.get()
            try:
                datetime.strptime(show_time, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid showtime format.")
                return

            shows = FileHandler.get_instance("shows.csv").read_data()
            show_id = str(uuid.uuid4())[:8]
            shows.append({"show_id": show_id, "movie_id": selected_movie, "screen_id": selected_screen, "show_time": show_time})
            FileHandler.get_instance("shows.csv").write_data(shows, ["show_id", "movie_id", "screen_id", "show_time"])

            messagebox.showinfo("Success", "Show added successfully!")
            self.show_admin_dashboard()

        ComponentFactory.create_button(self.root, "Add Show", command=submit_show).pack(pady=10)
        ComponentFactory.create_button(self.root, "Back", command=self.show_admin_dashboard).pack(pady=10)

    def load_shows(movies):
        with open('shows.csv', 'r') as file:
            reader = csv.DictReader(file)
            shows = []
            for row in reader:
                movie_name = movies[row['movie_id']]
                show_time = datetime.strptime(row['show_time'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                shows.append(f"Movie: {movie_name}, Screen: {row['screen_id']}, Time: {show_time}")
        return shows

    def book_ticket(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ComponentFactory.create_label(self.root, "Book Ticket", font=("Arial", 20)).pack(pady=10)
        shows = FileHandler.get_instance("shows.csv").read_data()
        movies = FileHandler.get_instance("movies.csv").read_data()  # Load movie data

        if not shows:
            messagebox.showerror("Error", "No shows available!")
            self.show_customer_dashboard()
            return

        # Create a mapping of movie_id to movie_name for easy lookup
        movie_dict = {movie["movie_id"]: movie["title"] for movie in movies}

        # Debug: print the movie_dict to check if it contains all expected movie ids
        print("Movie Dictionary: ", movie_dict)

        ComponentFactory.create_label(self.root, "Select Show").pack(pady=5)

        # Create a list of show details with movie name, screen, and time
        show_details = []
        for show in shows:
            movie_id = show["movie_id"]
            # Debug: Check if the movie_id exists in the movie_dict
            if movie_id in movie_dict:
                show_details.append(f"{movie_dict[movie_id]} - Screen {show['screen_id']} - {show['show_time']}")
            else:
                print(f"Warning: Movie ID {movie_id} not found in movie_dict!")

        if not show_details:
            messagebox.showerror("Error", "No valid shows found!")
            self.show_customer_dashboard()
            return
        # Using the show details as the options in the combobox
        show_combobox = ComponentFactory.create_combobox(self.root, show_details)
        show_combobox.pack(pady=5)

        def select_seat():
            selected_show = show_combobox.get()
            if not selected_show:
                messagebox.showerror("Error", "Please select a show!")
                return

            # Extract the show_id from the selected show string (it will be at the start)
            selected_show_id = None
            for show in shows:
                if f"{movie_dict[show['movie_id']]} - Screen {show['screen_id']} - {show['show_time']}" == selected_show:
                    selected_show_id = show["show_id"]
                    break

            seats = FileHandler.get_instance("seats.csv").read_data()
            available_seats = [seat for seat in seats if seat["show_id"] == selected_show_id and seat["is_booked"] == "N"]

            for widget in self.root.winfo_children():
                widget.destroy()

            ComponentFactory.create_label(self.root, "Select Seat", font=("Arial", 20)).pack(pady=10)
            seat_numbers = [seat["seat_number"] for seat in available_seats]
            seat_combobox = ComponentFactory.create_combobox(self.root, seat_numbers)
            seat_combobox.pack(pady=5)

            def choose_addons():
                selected_seat = seat_combobox.get()
                if not selected_seat:
                    messagebox.showerror("Error", "Please select a seat!")
                    return

                for widget in self.root.winfo_children():
                    widget.destroy()

                ComponentFactory.create_label(self.root, "Choose Add-ons", font=("Arial", 20)).pack(pady=10)
                snack_var = tk.BooleanVar()
                beverage_var = tk.BooleanVar()
                tk.Checkbutton(self.root, text="Snacks (₹50)", variable=snack_var).pack(pady=5)
                tk.Checkbutton(self.root, text="Beverages (₹30)", variable=beverage_var).pack(pady=5)

                def confirm_booking():
                    booking = Booking(ticket_price=200)  # Assume ticket price is ₹200

                    if snack_var.get():
                        booking = SnackDecorator(booking, snack_price=50)
                    if beverage_var.get():
                        booking = BeverageDecorator(booking, beverage_price=30)

                    final_price = booking.calculate_price()
                    confirm = messagebox.askyesno("Confirm Booking", f"Total Price: ₹{final_price}\nConfirm?")

                    if confirm:
                        command = BookTicketCommand(show_id=selected_show_id, seat_number=selected_seat, user_id=self.user_id)
                        command.execute()
                        self.show_customer_dashboard()

                ComponentFactory.create_button(self.root, "Confirm Booking", command=confirm_booking).pack(pady=10)
                ComponentFactory.create_button(self.root, "Back", command=self.book_ticket).pack(pady=10)

            ComponentFactory.create_button(self.root, "Next", command=choose_addons).pack(pady=10)
            ComponentFactory.create_button(self.root, "Back", command=self.book_ticket).pack(pady=10)

        ComponentFactory.create_button(self.root, "Select Seat", command=select_seat).pack(pady=10)
        ComponentFactory.create_button(self.root, "Back", command=self.show_customer_dashboard).pack(pady=10)

    def display_bookings(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ComponentFactory.create_label(self.root, "Your Bookings", font=("Arial", 20)).pack(pady=10)

        # Read bookings data and filter by the logged-in user's ID
        bookings = FileHandler.get_instance("bookings.csv").read_data()
        user_bookings = [booking for booking in bookings if booking["user_id"] == self.user_id]

        if not user_bookings:
            messagebox.showinfo("No Bookings", "You have no bookings yet!")
            self.show_customer_dashboard()
            return

        # Read shows data for movie name and show time details
        shows = FileHandler.get_instance("shows.csv").read_data()
        movies = FileHandler.get_instance("movies.csv").read_data()  # Load movie data

        # Create a mapping of movie_id to movie_name for easy lookup
        movie_dict = {movie["movie_id"]: movie["title"] for movie in movies}

        # Display bookings
        for booking in user_bookings:
            show_id = booking["show_id"]
            seat_number = booking["seat_number"]

            # Find show details
            show_details = next((show for show in shows if show["show_id"] == show_id), None)
            if show_details:
                movie_name = movie_dict.get(show_details["movie_id"], "Unknown Movie")
                screen_id = show_details["screen_id"]
                show_time = show_details["show_time"]

                booking_info = f"Movie: {movie_name} - Screen: {screen_id} - Time: {show_time} - Seat: {seat_number}"
                ComponentFactory.create_label(self.root, booking_info, font=("Arial", 14)).pack(pady=5)

        # Add a back button to go back to the dashboard
        ComponentFactory.create_button(self.root, "Back", command=self.show_customer_dashboard).pack(pady=10)


    def show_image(self):
        IMAGE_PATH = 'C:/Users/hello/summa.png'
        try:
            img = Image.open(IMAGE_PATH)
            self.img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.img, bg="white").place(x=0, y=0)
        except FileNotFoundError:
            print("Error: Image file not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieBookingApp(root)
    root.mainloop()

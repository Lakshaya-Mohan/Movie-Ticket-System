import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
import cx_Oracle

from tkinter import messagebox, ttk

connection = cx_Oracle.connect("system/Lakhs_123@localhost:1521/xe")

class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("900x600")
        
        self.entry()

    def entry(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()
        tk.Label(self.root, text="Movie Ticket Booking System", font=("Arial", 20), bg='#011838', fg='white', height =2).place(x=400, y = 40)
        tk.Button(self.root, text="Admin", command=self.show_admin_login, height = 3, width =15, font=("Arial", 15)).place(x= 500,y=200)
        tk.Button(self.root, text="Customer", command=self.show_customer_login, height = 3, width =15,font=("Arial", 15)).place(x= 500, y= 350)

    def show_admin_login(self):
        #Admin login page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.show_image()
        
        tk.Label(self.root, text="Admin Login", font=("Arial", 20), bg='#011838', fg='white', height =2).place(x= 600, y=100)
        tk.Label(self.root, text="Username: ",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=200)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.place(x=670, y=200)
        tk.Label(self.root, text="Password:",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=250)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.place(x=670, y=250)
        
        tk.Button(self.root, text="Login", command=self.admin_login,font=("Arial", 10), bg='#011838', fg='white', height =2,width=10).place(x= 630, y= 310)
        tk.Button(self.root, text="Back", command=self.entry,font=("Arial", 10), bg='#011838', fg='white', height =2,width=10).place(x= 770, y=35)

    def show_customer_login(self):
        #Customer login and registration page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.show_image()
        
        tk.Label(self.root, text="Customer Login", font=("Arial", 20), bg='#011838', fg='white', height =2).place(x= 600, y=100)
        tk.Label(self.root, text="Username: ",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=200)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.place(x=670, y=200)
        tk.Label(self.root, text="Password:",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=250)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.place(x=670, y=250)
        
        tk.Button(self.root, text="Login", command=self.customer_login,font=("Arial", 10), bg='#011838', fg='white', height =2,width=10).place(x= 630, y= 310)
        tk.Button(self.root, text="Register", command=self.show_register,font=("Arial", 10), bg='#011838', fg='white', height =2,width=10).place(x= 630, y=370)
        tk.Button(self.root, text="Back", command=self.entry,font=("Arial", 10), bg='#011838', fg='white', height =2,width=10).place(x= 770, y=35)

    def show_register(self):
        #Customer registration page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.show_image()
        
        tk.Label(self.root, text="Customer Registration",font=("Arial", 20), bg='#011838', fg='white', height =2).place(x= 560, y=80)
        tk.Label(self.root, text="Username: ",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=200)
        self.reg_username_entry = tk.Entry(self.root)
        self.reg_username_entry.place(x=670, y=200)
        tk.Label(self.root, text="Password:",bg='#011838',fg='white',font=("Arial", 15)).place(x= 550, y=250)
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.place(x=670, y=250)
        
        tk.Button(self.root, text="Register", command=self.register_user,font=("Arial", 10), bg='#011838', fg='white', height =2,width=10).place(x= 630, y=370)
        tk.Button(self.root, text="Back to login", command=self.show_customer_login,font=("Arial", 10), bg='#011838', fg='white', height =2,width=10).place(x= 770, y=35)

    

    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        status = 'customer' 

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = :1", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists.")
        else:
            cursor.execute(
                "INSERT INTO Users (username, password, status) VALUES (:1, :2, :3)",
                (username, password, status)
            )
            connection.commit()
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.show_customer_login()
        
        cursor.close()

    def admin_login(self):
        self.show_image()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = :1 AND password = :2 AND status = 'admin'", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        
        if admin:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials")

    def customer_login(self):
        #Customer login logic
        self.show_image()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = :1 AND password = :2 AND status = 'customer'", (username, password))
        customer = cursor.fetchone()
        cursor.close()
        
        if customer:
            self.user_id = customer[0]
            messagebox.showinfo("Login Successful", "Welcome, Customer!")
            self.show_customer_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid customer credentials")

        
        try:
            user_id = int(self.user_id)  #Convert to integer if user_id is not integer
        except ValueError:
            messagebox.showerror("Error", "Invalid user ID")
            return


    def show_admin_dashboard(self):
        #Admin dashboard
        
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20,'bold'), bg='#011838', fg='white', height =2).place(x= 540, y=40)
        tk.Button(self.root, text="Add Movie", command=self.add_movie,font=("Arial", 10), bg='white' ,height =2,width=10).place(x= 600, y=150)
        
        tk.Button(self.root, text="Add Show", command=self.add_show,font=("Arial", 10), bg='white',  height =2,width=10).place(x= 600, y=220)
        
        tk.Button(self.root, text="Remove Show", command=self.remove_show,font=("Arial", 10), bg='white', height =2,width=10).place(x= 600, y=290)
        
        tk.Button(self.root, text="Logout", command=self.entry,font=("Arial", 10), bg='white', height =2,width=10).place(x= 600, y=360)
        

    def show_customer_dashboard(self):
        #Customer dashboard
        
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()
        tk.Label(self.root, text="Customer Dashboard", font=("Arial", 20), bg='#011838', fg='white', height =2).place(x= 600, y=40)
        tk.Button(self.root, text="Book Ticket", command=self.show_movie,font=("Arial", 10), height =2,width=10).place(x= 670, y=140)
        tk.Button(self.root, text="Cancel Ticket", command=self.cancel_ticket,font=("Arial", 10), height =2,width=10).place(x= 670, y=200)
        tk.Button(self.root, text="Logout", command=self.entry,font=("Arial", 10), height =2,width=10).place(x= 670, y=260)

        
    def show_movie(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        IMAGE_PATH = 'C:/Users/hello/firstpic.jpg'
        try:
            img = Image.open(IMAGE_PATH)
            self.img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.img, bg="white").place(x=0, y=0)
        except FileNotFoundError:
            print("Error: Image file not found.")

        tk.Button(self.root, text="Back", command=self.show_customer_dashboard, height =2 ,width =10).place(x= 780, y=40)

        tk.Label(
            self.root, 
            text="Select Movie Show", 
            fg="white", 
            bg="black", 
            font=("Times New Roman", 20, "bold")
        ).place(x= 340 , y=70)

        canvas = tk.Canvas(self.root, width=500, height=330, bg="lightgrey")
        canvas.place(x=180, y=150)

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollbar.place(x=680, y=150, height=334)

        content_frame = tk.Frame(canvas)
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        

        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT s.show_id, m.title, s.show_time, s.screen_id
                FROM Shows s
                JOIN Movies m ON s.movie_id = m.movie_id
                WHERE s.show_time > SYSTIMESTAMP
            """)
            shows = cursor.fetchall()
            for i, show in enumerate(shows):
                show_id, title, show_time, screen_id = show
                tk.Button(content_frame,
                          text=f"{title} - {show_time} - Screen: {screen_id}",
                          height=2, width=70,
                          command=lambda sid=show_id: self.select_seat(sid)
                          ).grid(row=i, column=0, pady=5, padx=10, sticky="w")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()

    def select_seat(self, show_id):
        #Clear screen and display seats for the chosen show
        for widget in self.root.winfo_children():
            widget.destroy()

        
        tk.Label(self.root, text="Select Seat", font=("Arial", 18)).pack(pady=10)
        
        seat_frame = tk.Frame(self.root)
        seat_frame.pack(pady=20)

        cursor = connection.cursor()
        try:
            #Retrieve seats and their booking status
            cursor.execute("""
                SELECT seat_number, is_booked 
                FROM Seats 
                WHERE show_id = :1 
                ORDER BY seat_number
            """, (show_id,))
            seats = cursor.fetchall()
            
            for i, (seat_number, is_booked) in enumerate(seats):
                row = i // 10
                col = i % 10
                state = "disabled" if is_booked == 'Y' else "normal"
                btn = tk.Button(seat_frame, text=seat_number, width=3, state=state, 
                                command=lambda sn=seat_number: self.confirm_booking(show_id, sn))
                btn.grid(row=row, column=col, padx=5, pady=5)
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()

        tk.Button(self.root, text="Back", command=self.show_movie).pack(pady=1)

    def confirm_booking(self, show_id, seat_number):
        #Confirmation dialog for booking
        confirm = messagebox.askyesno("Confirm Booking", f"Do you want to book seat {seat_number} for this show?")
        if confirm:
            self.book_seat(show_id, seat_number)
            
    def book_seat(self, show_id, seat_number):
        cursor = connection.cursor()
        try:
            cursor.callproc("book_seat", [int(show_id), seat_number, int(self.user_id)])
            connection.commit()
            messagebox.showinfo("Success", "Ticket booked successfully")
            self.show_movie()  # Return to show selection screen
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()

                
    def cancel_ticket(self):
        cursor = connection.cursor()
        #Fetch tickets booked by the user
        cursor.execute("""
            SELECT B.booking_id, M.title, S.show_time, B.seat_number
            FROM Bookings B
            JOIN Shows S ON B.show_id = S.show_id
            JOIN Movies M ON S.movie_id = M.movie_id
            WHERE B.user_id = :1
        """, (self.user_id,))
        
        bookings = cursor.fetchall()
        cursor.close()

        if not bookings:
            messagebox.showinfo("Info", "No bookings found.")
            return

        #Display booked tickets in a selection window
        booking_window = tk.Toplevel(self.root)
        booking_window.title("Select a Ticket to Cancel")

        tk.Label(booking_window, text="Your Booked Tickets:", font=("Arial", 14)).pack(pady=10)

        #Create a frame to list bookings with scrollable view if necessary
        booking_list_frame = tk.Frame(booking_window)
        booking_list_frame.pack(fill=tk.BOTH, expand=True)
        booking_listbox = tk.Listbox(booking_list_frame, width=100, height=20)
        booking_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(booking_list_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        booking_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=booking_listbox.yview)

        #Insert user's bookings into the listbox with booking details
        for booking in bookings:
            booking_listbox.insert(tk.END, f"Movie: {booking[1]}, Time: {booking[2]}, Seat: {booking[3]}")
        
        def on_cancel_selection():
            selected_index = booking_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Warning", "Please select a ticket to cancel.")
                return

            booking_id, show_id = bookings[selected_index[0]][0], bookings[selected_index[0]][1]
            self.cancel_ticket_in_db(booking_id)
            booking_window.destroy()

        tk.Button(booking_window, text="Cancel Selected Ticket", command=on_cancel_selection).pack(pady=10)

        
    def cancel_ticket_in_db(self, booking_id):
        cursor = connection.cursor()
        try:
            #First, find the show_id and seat_number from the booking being canceled
            cursor.execute("SELECT show_id, seat_number FROM Bookings WHERE booking_id = :1", (booking_id,))
            result = cursor.fetchone()
            
            if result:
                show_id, seat_number = result
                
                #Delete the booking entry
                cursor.execute("DELETE FROM Bookings WHERE booking_id = :1", (booking_id,))
                
                #Update the seat to be available again for the same show
                cursor.execute("""
                    UPDATE Seats 
                    SET is_booked = 'N' 
                    WHERE show_id = :1 AND seat_number = :2
                """, (show_id, seat_number))
                
                connection.commit()
                messagebox.showinfo("Success", "Ticket canceled successfully and seat is now available for booking.")
            else:
                messagebox.showwarning("Warning", "Booking ID not found.")
        except cx_Oracle.DatabaseError as e:
            connection.rollback()
            messagebox.showerror("Error", f"Failed to cancel ticket: {e}")
        finally:
            cursor.close()


    def add_show(self):
        self.show_image()
        #Fetch available movies and screens for the dropdown menus
        cursor = connection.cursor()
        cursor.execute("SELECT movie_id, title FROM Movies")
        movies = cursor.fetchall()
        
        cursor.execute("SELECT screen_id FROM Screens")
        screens = cursor.fetchall()
        cursor.close()

        #Pass movies and screens to the show_input_page method
        self.show_input_page("Add Show", ["Show Time (YYYY-MM-DD HH24:MI:SS)"], self.add_show_to_db, movies=movies, screens=screens)

    def show_input_page(self, title, labels, submit_func, movies=None, screens=None):
        #Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()

        tk.Label(self.root, text=title, font=("Arial", 18)).pack(pady=10)

        #Movie dropdown
        tk.Label(self.root, text="Select Movie").pack(pady=5)
        self.movie_var = tk.StringVar()
        self.movie_dropdown = ttk.Combobox(self.root, textvariable=self.movie_var)
        self.movie_dropdown["values"] = [f"{movie[1]} (ID: {movie[0]})" for movie in movies]
        self.movie_dropdown.pack(pady=5)

        #Screen dropdown
        tk.Label(self.root, text="Select Screen").pack(pady=5)
        self.screen_var = tk.StringVar()
        self.screen_dropdown = ttk.Combobox(self.root, textvariable=self.screen_var)
        self.screen_dropdown["values"] = [screen[0] for screen in screens]
        self.screen_dropdown.pack(pady=5)

        #Other inputs
        self.entries = []
        for label_text in labels:
            tk.Label(self.root, text=label_text).pack(pady=5)
            entry = tk.Entry(self.root)
            entry.pack(pady=5)
            self.entries.append(entry)

        #Submit and Back buttons
        tk.Button(self.root, text="Submit", command=lambda: submit_func([entry.get() for entry in self.entries])).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_admin_dashboard).pack(pady=5)
    def add_show_to_db(self, inputs):
        cursor = None
        try:
            movie_selection = self.movie_dropdown.get()
            movie_id = int(movie_selection.split("ID: ")[1][:-1])
            
            screen_selection = self.screen_dropdown.get()
            screen_id = int(screen_selection)

            show_time = inputs[0]

            try:
                datetime.strptime(show_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter the date and time in the correct format.")
                return

            cursor = connection.cursor()
            cursor.execute("INSERT INTO Shows (movie_id, screen_id, show_time) VALUES (:1, :2, TO_TIMESTAMP(:3, 'YYYY-MM-DD HH24:MI:SS'))", 
                           (movie_id, screen_id, show_time))
            connection.commit()
            messagebox.showinfo("Success", "Show added successfully")
            self.show_admin_dashboard()
        except cx_Oracle.DatabaseError as e:
            if "check_show_conflict" in str(e):
                messagebox.showerror("Error", "Screen is already occupied at the selected time.")
            else:
                messagebox.showerror("Database Error", str(e))
        finally:
            if cursor:
                cursor.close()
                
    def remove_show(self):
        #Fetch all available shows for the listbox
        cursor = connection.cursor()
        cursor.execute("SELECT show_id, show_time FROM Shows")
        shows = cursor.fetchall()
        cursor.close()
        self.show_image()

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Remove Show", font=("Arial", 18)).pack(pady=10)
        
        #Show Listbox for selecting a show to delete
        self.show_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width =50, height =10)
        for show in shows:
            self.show_listbox.insert(tk.END, f"Show ID: {show[0]}, Time: {show[1]}")
        self.show_listbox.pack(pady=5)
        
        tk.Button(self.root, text="Delete Show", command=self.remove_show_from_db).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_admin_dashboard).pack(pady=5)

    def remove_show_from_db(self):

        self.show_image()
        try:
            selected_index = self.show_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a show to delete.")
                return

            selected_text = self.show_listbox.get(selected_index)
            show_id = int(selected_text.split("Show ID: ")[1].split(",")[0])

            cursor = connection.cursor()
            cursor.execute("DELETE FROM Shows WHERE show_id = :1", (show_id,))
            connection.commit()
            messagebox.showinfo("Success", "Show removed successfully")
            self.remove_show()  # Refresh the list
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close() 


    def add_movie(self):
        # Clear current frame
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_image()

        tk.Label(self.root, text="Add Movie", font=("Arial", 20), bg='#011838', fg='white').place(x= 530, y=40)

        # Title Input
        tk.Label(self.root, text="Movie Title",font=("Arial", 13), bg='#011838', fg='white').place(x= 530, y=100)

        self.title_entry = tk.Entry(self.root)
        self.title_entry.place(x= 510, y=140)


        # Duration Input
        tk.Label(self.root, text="Duration (in minutes)",font=("Arial", 13), bg='#011838', fg='white').place(x= 500, y=200)

        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.place(x= 510, y=250)


        # Buttons
        tk.Button(self.root, text="Add Movie", font=("Arial", 10),command=self.add_movie_to_db,width =10).place(x= 530, y=300)

        tk.Button(self.root, text="Back", font=("Arial", 10),command=self.show_admin_dashboard,width=10).place(x= 530, y=360)


    def add_movie_to_db(self):
        title = self.title_entry.get()
        duration = self.duration_entry.get()

        # Validate inputs
        if not title:
            messagebox.showerror("Input Error", "Movie title cannot be empty.")
            return

        if not duration.isdigit():
            messagebox.showerror("Input Error", "Duration must be a number.")
            return

        # Insert into database
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Movies (title, duration) VALUES (:1, :2)", (title, int(duration)))
            connection.commit()
            messagebox.showinfo("Success", "Movie added successfully")
            self.show_admin_dashboard()  # Return to admin dashboard
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()

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

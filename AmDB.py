import sqlite3
import tkinter as tk
import io
import os
import protected as protected
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter.filedialog


class AmDB(tk.Tk):
    data = []

    def __init__(self):
        super().__init__()
        self.geometry('1200x700')
        self.title("Знаменитые физики России")
        # Configure grid weights to allow proper resizing
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        #self.newData()
        self.data = self.getData()
        self.creatingBoxes()
        self.creatingButtons()

    def getData(self):
        conn = sqlite3.connect('AmDB.db')
        cursor = conn.cursor()
        # with open('140344_Periodic-Table-Mendeleev-C0135223-Dmitry_Mendeleyev-_Russian_chemist-SPL.jpg', 'rb') as file:
        # image_data = file.read()
        # cursor.execute("INSERT INTO data (name, text, image) VALUES (?, ?, ?)", ('Name', 'Some info', image_data))
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows

    def newData(self):
        conn = sqlite3.connect('AmDB.db')
        cursor = conn.cursor()
        # cursor.execute("DELETE FROM data WHERE id=?", ('3'))
        # fileName = 'nesmeyanov1.jpg'
        # with open(fileName, 'rb') as file:
        #     image_data = file.read()
        # cursor.execute("UPDATE data SET image=? WHERE id=?", (image_data, 3))
        # name = 'Александр Несмеянов'
        # info = 'Александр Николаевич Несмеянов был выдающимся российским химиком и лауреатом Нобелевской премии по ' \
        #        'химии. Его исследования в области химических кинетических реакций помогли установить основы ' \
        #        'физической химии и привели к разработке новых методов синтеза.'
        # fileName = 'nesmeyanov.jpeg'
        # with open(fileName, 'rb') as file:
        #     image_data = file.read()
        # cursor.execute("INSERT INTO data (name, text, image) VALUES (?, ?, ?)", (name, info, image_data))
        conn.commit()
        conn.close()

    def creatingBoxes(self):
        def on_name_selected(event):
            # Retrieve the selected name from the listbox
            selected_name = listbox.get(listbox.curselection())
            # Find the corresponding data for the selected name
            selected_data = next(item for item in self.data if item[3] == selected_name)
            # Convert the image data from bytes to a PIL Image object
            image = Image.open(io.BytesIO(selected_data[2]))
            # Resize the image to a desired size
            image = image.resize((self.winfo_width() // 3, self.winfo_height()), Image.LANCZOS)
            # Convert the PIL Image to a Tkinter-compatible format
            photo_image = ImageTk.PhotoImage(image)
            # Update the photo and text with the selected data
            photo_label.configure(image=photo_image)
            photo_label.image = photo_image  # Keep a reference to prevent image from being garbage collected
            text.delete("1.0", tk.END)
            text.insert(tk.END, selected_data[1])

        # Create the listbox for names
        listbox = tk.Listbox(self)
        for item0 in self.data:
            listbox.insert(tk.END, item0[3])
        listbox.grid(row=1, column=0, sticky="nsew")
        listbox.bind("<<ListboxSelect>>", on_name_selected)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # Create the photo display area
        photo_label = tk.Label(self)
        photo_label.grid(row=1, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # Create the text display area
        text = tk.Text(self)
        text.grid(row=1, column=2, sticky="nsew")
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def creatingButtons(self):
        add_window = None
        del_window = None
        change_window = None
        find_window = None
        show_window = None
        def show_popup_fond(event):
            popup_fond.post(event.x_root, event.y_root)

        def show_popup_info(event):
            popup_info.post(event.x_root, event.y_root)

        def addCommand():
            nonlocal add_window
            if add_window is not None:
                # The "Add" window is already open
                add_window.lift()  # Bring the window to the front
                return
            
            def on_window_close():
                nonlocal add_window
                add_window.destroy()
                add_window = None

            def save_data():
                nonlocal add_window
                # Retrieve the entered values from the entry fields
                name = name_entry.get()
                foto = foto_entry.get()
                text = text_entry.get("1.0", tk.END)
                if not name or not foto or not text:
                    messagebox.showerror("Error", "Please enter all the required data.")
                    add_window = None
                    return

                if not os.path.isfile(foto):
                    messagebox.showerror("Error", "The image file does not exist.")
                    add_window = None
                    return
                try:
                    with open(foto, 'rb') as file:
                        image_data = file.read()
                    # Perform the database operation to add the data
                    conn = sqlite3.connect('AmDB.db')
                    cursor = conn.cursor()
                    # Insert the new data into the database
                    cursor.execute("INSERT INTO data (name, text, image) VALUES (?, ?, ?)", (name, text, image_data))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Data added successfully.")
                    # Close the add window
                    add_window.destroy()
                    add_window = None
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    add_window.destroy()
                    add_window = None

            # Create a new window for adding data
            add_window = tk.Toplevel(self)
            add_window.title("Добавить информацию")
            add_window.protocol("WM_DELETE_WINDOW", on_window_close)  # Bind window close event
            # Create labels and entry fields for the user to enter data
            name_label = tk.Label(add_window, text="Имя:")
            name_label.pack()
            name_entry = tk.Entry(add_window)
            name_entry.pack()

            foto_label = tk.Label(add_window, text="Полный путь к файлу:")
            foto_label.pack()
            foto_entry = tk.Entry(add_window)
            foto_entry.pack()

            text_label = tk.Label(add_window, text="Текст:")
            text_label.pack()
            text_entry = tk.Text(add_window, height=5)
            text_entry.pack()

            # Create a button to save the entered data
            save_button = tk.Button(add_window, text="Сохранить", command=save_data)
            save_button.pack()


        def delCommand():
            nonlocal del_window
            if del_window is not None:
                # The "del" window is already open
                del_window.lift()  # Bring the window to the front
                return
            
            def on_window_close():
                nonlocal del_window
                del_window.destroy()
                del_window = None

            def del_data():
                nonlocal del_window
                name = name_entry.get()
                if not name:
                    messagebox.showerror("Error", "Please enter all the required data.")
                    del_window = None
                    return
                try:
                    # Perform the database operation to delete the data
                    conn = sqlite3.connect('AmDB.db')
                    cursor = conn.cursor()
                    # Check if any records match the input name
                    cursor.execute("SELECT * FROM data WHERE name=?", (name,))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        messagebox.showerror("Error", "No matching records found.")
                        conn.close()
                        change_window = None
                        return

                    # Delete the data from the database based on the name
                    cursor.execute("DELETE FROM data WHERE name=?", (name,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Data deleted successfully.")
                    del_window.destroy()
                    del_window = None
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    del_window.destroy()
                    del_window = None

            # Create a new window for deleting data
            del_window = tk.Toplevel(self)
            del_window.title("Удалить информацию")
            del_window.protocol("WM_DELETE_WINDOW", on_window_close)  # Bind window close event
            # Create labels and entry fields for the user to enter data
            name_label = tk.Label(del_window, text="Имя химика информацию о котором надо удалить:")
            name_label.pack()
            name_entry = tk.Entry(del_window)
            name_entry.pack()

            # Create a button to delete the data
            del_button = tk.Button(del_window, text="Удалить", command=del_data)
            del_button.pack()


        def changeCommand():
            nonlocal change_window
            if change_window is not None:
                # The "change" window is already open
                change_window.lift()  # Bring the window to the front
                return
            def browse_image():
                filename = tkinter.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
                new_image_entry.delete(0, tk.END)
                new_image_entry.insert(tk.END, filename)

            def on_window_close():
                nonlocal change_window
                change_window.destroy()
                change_window = None

            def change_data():
                nonlocal change_window
                name_to_change = name_to_change_entry.get()
                new_name = new_name_entry.get()
                new_image = new_image_entry.get()
                new_text = new_text_entry.get()
                if not name_to_change and (not new_name or not new_image or not new_text):
                    messagebox.showerror("Error", "Please enter all the required data.")
                    change_window.lift()
                    return
                if not os.path.isfile(new_image) and new_image:
                    messagebox.showerror("Error", "The image file does not exist.")
                    change_window.lift()
                    return
                try:
                    # Perform the database operation to change the data
                    conn = sqlite3.connect('AmDB.db')
                    cursor = conn.cursor()
                    # Check if any records match the input name
                    cursor.execute("SELECT * FROM data WHERE name=?", (name_to_change,))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        messagebox.showerror("Error", "No matching records found.")
                        change_window.lift()
                        conn.close()
                        return

                    # Prepare the SQL statement based on the new values provided
                    update_statement = "UPDATE data SET"
                    params = []
        
                    if new_name:
                        update_statement += " name=?,"
                        params.append(new_name)
                    if new_text:
                        update_statement += " text=?,"
                        params.append(new_text)
                    if new_image:
                        update_statement += " image=?,"
                        with open(new_image, 'rb') as file:
                            image_data = file.read()
                        params.append(image_data)
        
                    update_statement = update_statement.rstrip(",") + " WHERE name=?"
                    params.append(name_to_change)
        
                    # Execute the SQL statement with the parameters
                    cursor.execute(update_statement, tuple(params))
                    conn.commit()
                    conn.close()
        
                    messagebox.showinfo("Success", "Data changed successfully.")
                    change_window.destroy()
                    change_window = None
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    change_window.destroy()
                    change_window = None

            # Create a new window for deleting data
            change_window = tk.Toplevel(self)
            change_window.title("Изменить информацию")
            change_window.protocol("WM_DELETE_WINDOW", on_window_close)  # Bind window close event
            # Create labels and entry fields for the user to enter data
            name_to_change_label = tk.Label(change_window, text="Имя химика информацию(должен быть хотя бы один пункт) о котором надо изменить:")
            name_to_change_label.pack()
            name_to_change_entry = tk.Entry(change_window)
            name_to_change_entry.pack()
            new_name_label = tk.Label(change_window, text="Имя:")
            new_name_label.pack()
            new_name_entry = tk.Entry(change_window)
            new_name_entry.pack()
            new_text_label = tk.Label(change_window, text="Информация:")
            new_text_label.pack()
            new_text_entry = tk.Entry(change_window)
            new_text_entry.pack()
            new_image_label = tk.Label(change_window, text="Полный путь к файлу:")
            new_image_label.pack()
            new_image_entry = tk.Entry(change_window)
            new_image_entry.pack()
            # Create a button to browse for image file
            browse_button = tk.Button(change_window, text="Обзор", command=browse_image)
            browse_button.pack()
            # Create a button to delete the data
            change_button = tk.Button(change_window, text="Изменить", command=change_data)
            change_button.pack()


        def findCommand():
            nonlocal find_window
            if find_window is not None:
                # The "change" window is already open
                find_window.lift()  # Bring the window to the front
                return
            def on_window_close():
                nonlocal find_window
                find_window.destroy()
                find_window = None

            def search_data():
                nonlocal find_window
                name = name_entry.get()
                if not name:
                    messagebox.showerror("Error", "Please enter a name.")
                    find_window.lift()
                    return

                try:
                    # Perform the database operation to search for data
                    conn = sqlite3.connect('AmDB.db')
                    cursor = conn.cursor()

                    # Retrieve the data based on the name
                    cursor.execute("SELECT * FROM data WHERE name=?", (name,))
                    data = cursor.fetchall()

                    if len(data) == 0:
                        messagebox.showinfo("Information", "No matching records found.")
                        conn.close()
                        return

                    # Display the retrieved data
                    image = Image.open(io.BytesIO(data[0][2]))
                    image.show()

                    messagebox.showinfo("Information", f"Name: {data[0][0]}\nText: {data[0][1]}")

                    conn.close()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    find_window.destroy()
                    find_window = None

            # Create a new window for searching data
            find_window = tk.Toplevel(self)
            find_window.title("Find Data")
            find_window.protocol("WM_DELETE_WINDOW", on_window_close)  # Bind window close event

            # Create a label and entry field for the user to enter the name
            name_label = tk.Label(find_window, text="Enter a name:")
            name_label.pack()
            name_entry = tk.Entry(find_window)
            name_entry.pack()

            # Create a button to search for data
            search_button = tk.Button(find_window, text="Search", command=search_data)
            search_button.pack()

        def exitCommand():
            self.quit()

        def showContent():
            nonlocal show_window
            if show_window is not None:
                # The "change" window is already open
                show_window.lift()  # Bring the window to the front
                return
            def on_window_close():
                nonlocal show_window
                show_window.destroy()
                show_window = None
            show_window = tk.Toplevel(self)
            show_window.title("Справка")
            show_window.protocol("WM_DELETE_WINDOW", on_window_close)  # Bind window close event
            show_label = tk.Label(show_window, text="База данных 'Знаменитые химики России'\n"
                                            "Позволяет: добавлять, изменять и удалять информацию\n"
                                            "Клавиши программы:\n"
                                            "F1-вызов справки по программе\n"
                                            "F2-добавить в базу данных\n"
                                            "F3-удалить из базы данных\n"
                                            "F4-изменить запись в базе данных")
            show_label.pack()

        def showProgramInfo():
            info_window = tk.Toplevel(self)
            info_window.title("О программе")
            info_window.geometry("300x200")  # Set the window size 
            info_window.resizable(False, False)  # Disable window resizing

            info_label = tk.Label(info_window, text="База данных 'Знаменитые химики России'\n"
                                                    "Author: Egor        Version: 1.0")
            info_label.pack()

            ok_button = tk.Button(info_window, text="OK", command=info_window.destroy)
            ok_button.pack()

            # Set the window as a modal window
            info_window.transient(self)
            info_window.grab_set()
            self.wait_window(info_window)

        # Create a button
        buttonFond = tk.Button(self, text="Фонд")
        # Create a popup menu
        popup_fond = tk.Menu(self, tearoff=0)
        popup_fond.add_command(label="Найти...", command=findCommand)
        popup_fond.add_command(label="Добавить  F2", command=addCommand)
        # Bind the F2 key event to the addCommand function
        self.bind("<F2>", lambda event: addCommand())
        popup_fond.add_command(label="Удалить  F3", command=delCommand)
        self.bind("<F3>", lambda event: delCommand())
        popup_fond.add_command(label="Изменить  F4", command=changeCommand)
        self.bind("<F4>", lambda event: changeCommand())
        popup_fond.add_command(label="Выход    Ctrl+x", command=exitCommand)
        self.bind("<Control-x>", lambda event: exitCommand())
        # Bind the button to open the popup menu on right-click
        buttonFond.bind("<Button-3>", show_popup_fond)
        buttonFond.bind("<Button-1>", show_popup_fond)
        buttonFond.grid(row=0, column=0, sticky="nw")
        # Create a button
        buttonInfo = tk.Button(self, text="Справка")
        # Create a popup menu
        popup_info = tk.Menu(self, tearoff=0)
        popup_info.add_command(label="Содержание", command=showContent)
        self.bind("<F1>", lambda event: showContent())
        popup_info.add_command(label="О программе", command=showProgramInfo)
        # Bind the button to open the popup menu on right-click
        buttonInfo.bind("<Button-3>", show_popup_info)
        buttonInfo.bind("<Button-1>", show_popup_info)
        buttonInfo.grid(row=0, column=0, sticky="nw")
        buttonInfo.place(x=65)
        # Create empty space for buttons in the left upper corner
        button_space_top = tk.Label(self)
        button_space_top.grid(row=0, column=1)
        # Create empty space for buttons in the left lower corner
        button_space_bottom = tk.Label(self)
        button_space_bottom.grid(row=2, column=1)


AmDB = AmDB()
AmDB.mainloop()

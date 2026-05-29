''' making an interactive gui app for a to do this that we can add, 
delete and mark completions of tasks'''

import tkinter as tk 
'''#tkinter is built in graphical user int tool, buttons, windows, etc. 
'as' means alias for short form '''

from tkinter import messagebox 
''' messagebox provides small dialoge popups. 
i.e to clear all, it will ask for confirmation with a popup'''

''' class is an all encompasing container for all widgets, functions, etc'''
class TodoApp: 
    def __init__(self, root): # init method runs automatically, root is the parameter/ main application window 
        self.root = root # store root inside the class to be referenced at any point 
        self.root.title("To-Do List 2026") # the title of the page 
        self.root.geometry("500x450") # app page margin size to fit buttons, passing string values, app will be 500 pixels wide and 4050 pixels tall
        self.root.resizable(False, False) # prevents draging of page to enlarge, to keep lay out consistent, and prevent stretching and odd placement
        self.root.configure(bg ="#f0f4f7") # background color, set to hex color 

        self.tasks = [] # list for all to do items and will be stored as small dictionary 
        self.setup_ui() # our entire User Interface setup 

    def setup_ui(self): #visual layout of UI
        title_label=tk.Label(
            self.root,
            text = "TO-DO-LIST",
            font =("Helvetica", 22, "bold"),
            bg = "#f0f4f7",
            fg = "#333"
        )
        
        title_label.pack(pady=10) # places label at top with some space
        
        input_frame = tk.Frame(self.root, bg = "#f0f4f7") # 
        input_frame.pack(pady=10) # vertical spacing before and after 

        self.task_entry = tk.Entry(  # task entry box 
            input_frame,
            font = ("Helvetica", 12),
            width = 30
        ) 
        self.task_entry.pack(side="left", padx=(0, 10)) # on left had side 
        add_button = tk.Button(
            input_frame, 
            text = "Add Task",
            font = ("Helvetica", 11, "bold"),
            bg = "#27ae60",
            fg = "white",
            padx =10, 
            command= self.add_task 
        )
        
        add_button.pack(side="left") # buttons on left hand side

        list_frame = tk.Frame(self.root, bg = "#f0f4f7")
        list_frame.pack(pady=10, fill = "both", expand = True)

        self.task_listbox = tk.Listbox( # list boxes 
            list_frame, 
            font = ("Helvetica", 12),
            width = 45,
            height = 10,
            activestyle= "none"
        )
        self.task_listbox.pack(side="left", fill="both", expand=True) # makes list box grow along with windows size constraints 

        scrollbar = tk.Scrollbar(list_frame) # create a scroll bar for long list 
        scrollbar.pack(side="right", fill="y") # put it on the right side 

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview) #tells to scroll when the scroll bar is moved 

        self.info_label = tk.Label( # information label to sit nicely under task list, for status when actions happen 
            self.root, # passes in the window not list frame
            font = ("Helvetica", 11),
            bg = "#f0f4f7", # background match window 
            fg = "#007acc"  # text color 
        )
        self.info_label.pack(pady=5)

    # now for the action buttons of task 

        button_frame = tk.Frame(self.root, bg = "#f0f4f7")
        button_frame.pack(pady=10) # vertical line spacing 

        mark_done_button = tk.Button( # mark as complete button frame 
            button_frame,
            text = "Mark as done", 
            font = ("Helvetica", 11, "bold"),
            bg = "#2980b9",
            fg = "white",
            padx= 10,
            command=self.mark_done # when user clicks, will call mark down method 
        )
        mark_done_button.pack(side="left", padx=5)

        delete_button = tk.Button( # Deletes a task
            button_frame,
            text = "Delete Task",
            font = ("Helvetica", 11, "bold"),
            bg = "#c0392b", # Background is set to red to evoke a critical operation 
            fg = "white",
            padx=10,
            command=self.delete_task # will call the delete task method 
        )
        delete_button.pack(side="left", padx=5)

        clear_button = tk.Button( # clear all button OP
            button_frame,
            text =  "Clear All",
            font = ("Helvetica", 11, "bold"),
            bg = "#7f8c8d",
            fg = "white",
            padx=10,
            command=self.clear_all # call clear all method to clear all tasks after confirmation 
        )
        clear_button.pack(side="left", padx=5)

    def refresh_listbox(self): #clears the list, reads eveyr item with a number and an emoji on wheter or not its done
        self.task_listbox.delete(0, tk.END) 
        for index, task in enumerate(self.tasks, start=1): # START INDEX from one
            status = "✅" if task["done"] else "❌" #markers for if task is complete 
            display_text = f"{index}.{task['task']} [{status}]" # display text 
            self.task_listbox.insert(tk.END, display_text)  #each item on new line at bottom of list box 
            # 

    def add_task(self): # method to be done for when a task is added button
        task_text = self.task_entry.get().strip() # strip removes white space 
        if not task_text: # if empty 
            self.info_label.config(text = "Please enter a task first.")
            return
        
        self.tasks.append({"task" : task_text, "done" : False}) #append tasks if there is tasks in the dictionary
        self.task_entry.delete(0, tk.END) #removes everything from entry widget to add new task
        self.info_label.config(text = f"Task '{task_text}' added!") # task confirmation
        self.refresh_listbox() # show the new task updated alongside the existing ones 

    def get_selected_index(self): 
        selection = self.task_listbox.curselection() # if user selects task. tuple will select its index
        if not selection: # if empty 
            messagebox.showinfo("No Selection", "Pleasae select a task first")
            return None
        return selection[0] # returns the first selected index 
    
    def mark_done(self): # mark task as completed 
        index = self.get_selected_index()
        if index is None: # if empty 
            return
        
        self.tasks[index]["done"] = True # task is considered completed 
        self.info_label.config(text = "Task marked as done!")
        self.refresh_listbox() # refreshes and shows check beside task marked as done 

    def delete_task(self): # delete a single task 
        index = self.get_selected_index()
        if index is None:
            return
        
        removed = self.tasks.pop(index)
        self.info_label.config(text = f"Deleted Task: {removed['task']}")
        self.refresh_listbox()

    def clear_all(self): # clear all tasks
        if not self.tasks:
            self.info_label.config(text = "No tasks to Clear.")
            return
        
        if messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?"): # will prompt yes or no on whether to proceed
            self.tasks.clear()
            self.refresh_listbox()
            self.info_label.config(text = "All tasks cleared!")

# launch the app

if __name__ == "__main__": #code executes when script is run directly, not imported 
    root = tk.Tk() # create a tkinter window
    app = TodoApp(root)
    root.mainloop() # keeps the program running waiting for user input 




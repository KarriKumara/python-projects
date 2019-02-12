from Tkinter import *
import tkFileDialog
import datetime

class SundayFinder:

    def __init__(self, master):
        """
        This initializes the Sunday Finder application.
        """
        
        self.master = master
        master.title("Sunday Finder")
        master.geometry("500x800")

        #This part defines the date entry textboxes.
        self.label_entry_1 = Label(master, text="Enter the earlier date in the format DAY.MONTH.YEAR")
        self.label_entry_1.pack(anchor = W)
        
        self.entry_1 = Entry(master)
        self.entry_1.pack(anchor = W)
        
        
        self.label_entry_2 = Label(master, text="Enter the later date in the format DAY.MONTH.YEAR")
        self.label_entry_2.pack(anchor = W)
        
        self.entry_2 = Entry(master)
        self.entry_2.pack(anchor = "w");
        
        self.entry_button = Button(master, text="Find the sundays", command=self.enter_input)
        self.entry_button.pack(anchor = "w")

        self.label_whitespace_2 = Label(master)
        self.label_whitespace_2.pack(anchor = "w")
        


        #This part defines three radio buttons used for choosing whether to print the results in the interface,
        #into a file or both.
        self.label_entry_4 = Label(master, text="Choose how to print the results")
        self.label_entry_4.pack(anchor = "w")
        
        self.var_print_option = IntVar(value = 1)
        
        self.radiobutton_print_interface = Radiobutton(master, text="Print to interface", variable=self.var_print_option, value=1)
        self.radiobutton_print_interface.pack(anchor = "w")
        self.radiobutton_print_file = Radiobutton(master, text="Print to file", variable=self.var_print_option, value=2)
        self.radiobutton_print_file.pack(anchor = "w")
        self.radiobutton_print_both = Radiobutton(master, text="Print to both", variable=self.var_print_option, value=3)
        self.radiobutton_print_both.pack(anchor = "w")
        
        self.label_whitespace_3 = Label(master)
        self.label_whitespace_3.pack(anchor = "w")
        
        
        #This part defines two radio buttons used for choosing between printing the result dates in ascending or #descending order.
        self.label_entry_4 = Label(master, text="Choose display order for the dates")
        self.label_entry_4.pack(anchor = "w")
        
        self.var_descending = IntVar(value = 1)
        self.radiobutton_descending = Radiobutton(master, text="Descending", variable=self.var_descending, value=1)
        self.radiobutton_ascending = Radiobutton(master, text="Ascending", variable=self.var_descending, value=2)
        self.radiobutton_descending.pack(anchor= "w")
        self.radiobutton_ascending.pack(anchor= "w")

        self.label_whitespace_4 = Label(master)
        self.label_whitespace_4.pack(anchor = "w")
        
        self.label_output = Label(master, text ="Read the output here:")
        self.label_output.pack(anchor = "w")
        
        #This defines the output box into which the results and exception messages can be printed.
        self.output_box = Listbox(self.master)
        self.scrollbar = Scrollbar(self.output_box, orient="vertical", command=self.output_box.yview)
        self.output_box.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.output_box.pack(anchor = "w", fill=BOTH, expand=True)
        

    def enter_input(self):
        """
        This retrieves the dates input by the user and begins the sunday finding process.
        """
        
        date1 = self.entry_1.get()
        date2 = self.entry_2.get()
        
        #Check that the dates are valid before proceeding.
        date1_is_valid = self.check_input_validity(self.entry_1.get())
        date2_is_valid = self.check_input_validity(self.entry_2.get())
        
        if date1_is_valid and date2_is_valid:
            sunday_array = self.get_sundays(date1, date2)
            if sunday_array:
                self.print_sundays(sunday_array, date1, date2)
        else:
            self.output_box.insert(END, "Invalid input data.")
            self.output_box.insert(END, "Process cancelled")
            self.output_box.insert(END, "")
            
        self.output_box.pack(anchor = "w")
        self.output_box.see(END)

        
    def check_input_validity(self, input_string):
        """
        This checks that a given date input by the user is a valid date in the correct format.
        """
                
        try:
            day, month, year = input_string.split('.')
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            self.output_box.insert(END, "The date input \"" + input_string + "\" is not a valid date in the DAY.MONTH.YEAR format." )
            self.output_box.pack(anchor = "w")
            self.output_box.see(END)
            return False
        
    def get_sundays(self, date1, date2):
        """
        This returns the sundays between the given input dates, if any.
        If the second date is before the first, the process is cancelled.
        """
        
        day1, month1, year1 = date1.split('.')
        date1_datetime = datetime.datetime(int(year1), int(month1), int(day1))
        
        day2, month2, year2 = date2.split('.')
        date2_datetime = datetime.datetime(int(year2), int(month2), int(day2))
        
        if date1_datetime > date2_datetime:
            self.output_box.insert(END, "The first input date should be earlier than the second.")
            self.output_box.insert(END, "Invalid input data.")
            self.output_box.insert(END, "Process cancelled")
            self.output_box.pack(anchor = "w")
            self.output_box.insert(END, "")

            self.output_box.see(END)
            return
        
        #Finding the first sunday
        weekday1 = date1_datetime.weekday()
        days_until_first_sunday = 6 - weekday1
                
        #Calculating the total number of days between the given dates.
        days_between = (date2_datetime - date1_datetime).days
        
        
        #Beginning from the first sunday, the while-loop goes forward one week from one sunday to the next until the
        #second date is reached or passed.
        #Each sunday found is added to the array to be returned.
        sunday_array = []
        i = days_until_first_sunday
        while i < days_between:
            sunday_array.append(date1_datetime + datetime.timedelta(days=i))
            i = i + 7
        
        return sunday_array
    
    def print_sundays(self, sunday_array, date1, date2):
        """
        This handles the printing of the results.
        """     
        
        #If the print_option variable is 1, the results are printed in the interface.
        #If it is 2, the results are saved into a file.
        #If it is 3, the results are both printed in the interface and saved into a file.
        print_option = self.var_print_option.get()
        
        if print_option == 1:
            #This prints the results in the user interface.
            self.output_box.insert(END, "Sundays between dates " + date1 + " and " + date2 + " were")
            if self.var_descending.get() == 1:
                for sunday in sunday_array:
                    self.output_box.insert(END, sunday.strftime("%d.%m.%Y"))
            else:
                for sunday in reversed(sunday_array):
                    self.output_box.insert(END, sunday.strftime("%d.%m.%Y"))
            self.output_box.insert(END, "")
            self.output_box.pack(anchor = "w")
            self.output_box.see(END)
        elif print_option == 2:
            #This saves the results into a file
            save_this = "Counting sundays\n"
            if self.var_descending.get() == 1:
                save_this = save_this + "Starting date: " + date1
                for sunday in sunday_array:
                    save_this = save_this + "\n" + sunday.strftime("%d.%m.%Y")
                save_this = save_this + "Ending date: " + date2
            else:
                save_this = save_this + "Ending date: " + date2
                for sunday in reversed(sunday_array):
                    save_this = save_this + "\n" + sunday.strftime("%d.%m.%Y")
                save_this = save_this + "\nStarting date: " + date1
            self.file_save(save_this)
        elif print_option == 3:
            #This prints the results in the user interface and saves them to a file.
            self.output_box.insert(END, "Sundays between dates " + date1 + " and " + date2 + " were")
            save_this = "Counting sundays\n"
            if self.var_descending.get() == 1:
                save_this = save_this + "Starting date: " + date1
                for sunday in sunday_array:
                    self.output_box.insert(END, sunday.strftime("%d.%m.%Y"))
                    save_this = save_this + "\n" + sunday.strftime("%d.%m.%Y")
            else:
                save_this = save_this + "Ending date: " + date2
                for sunday in reversed(sunday_array):
                    self.output_box.insert(END, sunday.strftime("%d.%m.%Y"))
                    save_this = save_this + "\n" + sunday.strftime("%d.%m.%Y")
                save_this = save_this + "\nStarting date: " + date1
            self.output_box.insert(END, "")
            self.output_box.pack(anchor = "w")
            self.output_box.see(END)
            self.file_save(save_this)
        else:
            #This should not happen, but let's handle it just in case.
            self.output_box.insert(END, "Internal value error: The variable var_print_option should be 1, 2 or 3." )
            self.output_box.insert(END, "Process cancelled." )
            self.output_box.insert(END, "" )
            self.output_box.pack(anchor = "w")
            self.output_box.see(END)
            
        
    def file_save(self, save_this):
        """
        This opens a save file dialog, allowing the user to save the results to a text file.
        """
        filename = tkFileDialog.asksaveasfilename(defaultextension=".txt")
        if filename is None:
            return
        f = open(filename, 'w')
        f.write(save_this)
        f.close()
        
root = Tk()
my_gui = SundayFinder(root)
root.mainloop()

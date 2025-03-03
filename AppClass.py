import tkinter as tk
from tkinter import messagebox, filedialog


class DangerTyping:
    def __init__(self, controller):
        self.controller = controller
        self.background_color = "#FFFFFF"
        self.color_range = ["#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00"] # Shifting colors fo the timer
        self.font = "Courier"
        self.controller.title("Dangerous Writing")
        self.controller.geometry('1000x500')
        self.controller.config(bg=self.background_color)

        self.danger_timer = None # The danger timer
        self.timer = None # The session timer

        # Labels
        self.explanation_label = tk.Label(controller, bg=self.background_color, text="Welcome to the Dangerous writing app!\n" 
                                          "You will have 1 minute to write what you want, but if you do not type anything for 5 seconds, All will be lost! "
                                          )
        self.input_text = tk.Text(controller, # Input box where we will write all of our text
                     height=15,
                     width=70)
        self.timer_label = tk.Label(controller, text="00:00", font=(self.font, 45, "bold"), bg=self.background_color)
        self.danger_label = tk.Label(controller, text="0", font=(self.font, 60, "bold"), bg=self.background_color)
        

        # Buttons
        self.start_button = tk.Button(controller, text="Start", command=self.start_app)
        self.reset_button = tk.Button(controller, text="Reset", command=self.reset_app)

        self.explanation_label.pack(padx=20, pady=10) # We pack the explanation label
        self.input_text.pack() # We pack the input label

        self.start_button.pack(pady=5) # Packing the Start button
        self.reset_button.pack() # Packing Reset Button

        self.timer_label.pack()
        self.danger_label.pack()

        # Bind widget with key presses
        self.input_text.bind("<KeyPress>", self.reset_danger_timer)

    # Countdown Functions
    def countdown(self, t):
        """Countdown Mechanism"""
        if t > 0: # Loops until not 0
            mins, secs = divmod(t, 60) # Calculates the minutes and remaining seconds using divmod function
            self.timer_label.config(text="{:02d}:{:02d}".format(mins, secs)) # Formating configuration for the timer
            self.timer = self.controller.after(1000, self.countdown, t - 1) # The functions runs again after 1 second
            t -= 1 # Inputed secons reduced by 1
        else:
            self.timer_label.config(text="00:00")
            self.controller.after_cancel(self.timer)
            self.controller.after_cancel(self.danger_timer)
            self.danger_label.config(text="0")
            self.well_done()
            
    def danger_countdown(self, t):
        """The danger Countdown Mechanism"""
        if t > 0: # Loops until 0
            self.controller.config(bg=self.color_range[t - 1])
            self.danger_label.config(text=t, bg=self.color_range[t - 1])
            self.timer_label.config(bg=self.color_range[t - 1])
            self.danger_timer = self.controller.after(1000, self.danger_countdown, t - 1)
            t -= 1
        else:
            self.danger_label.config(text="0")
            self.clear_text()
            self.controller.after_cancel(self.timer) # Should cancel the previous timer
            self.timer_label.config(text="00:00") # Sets the timer back to 0

    # Button Functions
    def start_app(self):
        """Start Mechanism"""
        self.input_text.focus_set() # Sents the focus on the text box
        self.countdown(t=60) # Can change to what you want here, default 1 min   
        self.danger_countdown(5)
    
    def reset_app(self):
        """Reset the app to Original state"""
        self.controller.after_cancel(self.danger_timer) # Cancel the timers
        self.controller.after_cancel(self.timer)
        self.clear_text()
        self.timer_label.config(text="00:00", bg=self.background_color) # Reset the texts
        self.danger_label.config(text="0", bg=self.background_color)
        self.controller.config(bg=self.background_color) # Resets the background
        
    # Support Functions
    def reset_danger_timer(self, event):
        """The event listener for key presses"""
        if self.danger_timer:
            self.controller.after_cancel(self.danger_timer)
        self.danger_countdown(5)

    def clear_text(self):
        """Text deletion Function"""
        self.input_text.delete("1.0", tk.END)

    # Pop-up Functions
    def well_done(self):
        """A pop up window if you survived the desired time"""
        self.pop_up = tk.Toplevel()
        self.pop_up.title("Well Done, Writer!")
        self.pop_up.geometry("300x300")

        # Labels
        self.well_done_label = tk.Label(self.pop_up, text="Well Done on your writing. \n" 
                                   "You can choose to save what you wrote or \n "
                                   "delete and reset the app.")
        # Buttons
        self.save_button = tk.Button(self.pop_up, text="Save", command=self.save_text)
        self.delete_button = tk.Button(self.pop_up, text="Delete", command=self.combined_well_done)

        # Packing
        self.well_done_label.pack()
        self.save_button.pack(pady=5)
        self.delete_button.pack()

    def save_text(self):
        """The text save function, Currently only as .txt"""
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if self.file_path: # This should check if the user has chosen a File Path
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.input_text.get("1.0", tk.END)) # Will save the Text
                messagebox.showinfo("Success", f"File Saved: {self.file_path}")
                self.pop_up.destroy()
                self.reset_app()
            except Exception as e:
                messagebox.showerror("Error", f"Unable to save file:\n{e}")

    def combined_well_done(self):
        """A simple combination to be called out on the Delete button"""
        self.pop_up.destroy()
        self.reset_app()

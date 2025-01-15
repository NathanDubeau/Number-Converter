import os
import sys
import tkinter as tk
from tkinter import messagebox

class TextToNumber:
    def __init__(self):
        # Define numbers zero [0] through nineteen [19] - Easier to parse these directly than adding a ones digit to ten for teen conversions.
        self.units = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
            'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19
        }
        # Define each of increment of ten - After the 'tens' is read if a 'ones' follows we can add them together for the sum to be printed.
        self.tens = {
            'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
            'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
        }
        
        # Scales (multipliers) - These are the words that represent the scale of the number, such as hundred, thousand, million, etc.
        self.scales = {
            'hundred': 100, 'thousand': 1000, 'million': 1000000
        }
    # Use 'and' or a space to seperate values though 'and' is not required but can be used for clarity and in the case thats how the user types their numbers.
    def parse(self, text):
        words = text.lower().replace(' and', '').split()
        result = 0
        current_value = 0
        last_scale = 1

        for word in words:
            if word in self.units:
                current_value += self.units[word]
            elif word in self.tens:
                current_value += self.tens[word]
            elif word in self.scales:
                scale_value = self.scales[word]

                # Handle the scale logic.
                if scale_value == 100:  # For hundred, multiply current_value.
                    current_value *= scale_value
                elif scale_value > last_scale:  # Thousand, Million, etc. This is used for scaling up the number ex: 100,000 uses both hundred and thousand.
                    result += current_value * scale_value
                    current_value = 0
                else:  # If scale is smaller than the last scale, add current_value. This works in cases like 10,100 where we dont want the 100 to use the thousand scale that came before it.
                    result += current_value
                    current_value = scale_value

                last_scale = scale_value

        result += current_value  # Add the last part if anything is left over.
        return result

#Start of the number to text conversion
    def number_to_text(self, num):
        if num == 0:
            return 'zero'
# Dictionary of numbers to words
#Starting again with zero [0] to nineteen [19] - This is the same as the text to number conversion but in reverse.
        units = [
            'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
            'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'
        ]
# Continuing with the tens [20] through [90] - This is the same as the text to number conversion but in reverse.
        tens = [
            '', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
        ]
#Continuing with the scales [100] through [billion] - This is the same as the text to number conversion but in reverse.
        scales = [
            '', 'thousand', 'million', 'billion'
        ]
# Function to convert a number to words between 0 and 999.
        def convert_chunk(n):
            """ Convert a number between 0 and 999 to words """
            if n == 0:
                return ''
            elif n < 20:
                return units[n]
            elif n < 100:
                return tens[n // 10] + ('-' + units[n % 10] if n % 10 else '')
            else:
                return units[n // 100] + ' hundred' + (' ' + convert_chunk(n % 100) if n % 100 else '')

        # Split the number into chunks of thousands so that it can be converted to words in groups of three digits.
        chunks = []
        scale_idx = 0
        while num > 0:
            chunk = num % 1000
            if chunk > 0:
                chunks.append(convert_chunk(chunk) + (f' {scales[scale_idx]}' if scales[scale_idx] else ''))
            num //= 1000
            scale_idx += 1

        return ' '.join(reversed(chunks)).strip()

# Create GUI with Tkinter.
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nate's Number Converter") #sets title of the window.
        self.geometry("400x300") #sets the size of the window.
        self.text_to_number = TextToNumber()

        # Get the path to the icon file, handles both normal and bundled versions.
        icon_path = self.resource_path("LogoDraftv2.ico") #uses .ico file for the icon.
        self.iconbitmap(icon_path)

        # Create the GUI components.
        self.create_widgets()

# Function to get the path to the resource file, works for both development and frozen executable.
    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, works for both development and frozen executable. """
        try:
            # PyInstaller creates a temporary folder and stores the path in _MEIPASS.
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

#Created the widgets with the text to number and number to text conversion within our GUI.
    def create_widgets(self):
        # Text to Number Conversion labels and buttons.
        self.label1 = tk.Label(self, text="Enter number in text (Example: Five):")
        self.label1.pack(pady=10)

        self.text_input = tk.Entry(self, width=30)
        self.text_input.pack(pady=10)

        self.convert_text_button = tk.Button(self, text="Convert to Number", command=self.convert_text_to_number)
        self.convert_text_button.pack(pady=10)

        self.result_label = tk.Label(self, text="Converted Result Will Appear Here.")
        self.result_label.pack(pady=10)

        # Number to Text Conversion labels and buttons.
        self.label2 = tk.Label(self, text="Enter number to convert to text (Example: 5):")
        self.label2.pack(pady=10)

        self.number_input = tk.Entry(self, width=30)
        self.number_input.pack(pady=10)

        self.convert_number_button = tk.Button(self, text="Convert to Text", command=self.convert_number_to_text)
        self.convert_number_button.pack(pady=10)

#functions to parse the data or display an error message if the data is invalid.
    def convert_text_to_number(self):
        text = self.text_input.get().strip()
        try:
            number = self.text_to_number.parse(text)
            self.result_label.config(text=f"Number: {number}")
        except Exception as e:
            messagebox.showerror("Error! [01]", f"Could not parse '{text}'. Please enter a valid number in text format. Such as [Five]")

    def convert_number_to_text(self):
        try:
            number = int(self.number_input.get().strip())
            text = self.text_to_number.number_to_text(number)
            self.result_label.config(text=f"Text: {text}")
        except ValueError:
            messagebox.showerror("Error! [02]", "Invalid number. Please enter a valid number such as [5].")

# Run the application using the mainloop - if using terminal I can run the program using the command: py NumConverterGUI.py
#Or if trying to compile it all together I can use the command: pyinstaller --onefile --windowed --icon=LogoDraftv2.ico --name="NatesNumberConverter" --add-data "LogoDraftv2.ico;." NumConverterGUI.py
#this will create a .exe file that can be run on any windows machine and it will use the logo i made, customize the exe's name and include the logo in the files for safe keeping!
if __name__ == "__main__":
    app = Application()
    app.mainloop()

import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    """
    A simple calculator application built using Python's Tkinter library.
    It mimics the basic layout and functionality of a standard calculator,
    using the eval() function for expression evaluation.
    """
    def __init__(self, master):
        self.master = master
        master.title("Calculator App")
        master.config(bg="#E5E7EB") # Light gray background

        # Current expression and input value
        self.current_input = ""
        self.expression = ""

        # --- Display Setup ---

        self.secondary_display = tk.Label(master, text="", anchor='e', font=('Inter', 14), 
                                          bg="#E5E7EB", fg="#6B7280", padx=10, pady=5)
        self.secondary_display.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.entry = tk.Entry(master, width=20, font=('Inter', 36, 'bold'), 
                              bd=0, relief=tk.FLAT, justify='right', 
                              bg="#E5E7EB", fg="#1F2937", insertbackground="#1F2937")
        self.entry.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=(5, 10))
        self.entry.insert(0, "0")
        self.entry.config(state='readonly')

        # --- Button Layout Configuration ---

        buttons = [
            ('AC', 2, 0, 'control'), ('±', 2, 1, 'control'), ('%', 2, 2, 'control'),
            ('÷', 2, 3, 'operator'),
            ('7', 3, 0, 'number'), ('8', 3, 1, 'number'), ('9', 3, 2, 'number'), ('×', 3, 3, 'operator'),
            ('4', 4, 0, 'number'), ('5', 4, 1, 'number'), ('6', 4, 2, 'number'), ('-', 4, 3, 'operator'),
            ('1', 5, 0, 'number'), ('2', 5, 1, 'number'), ('3', 5, 2, 'number'), ('+', 5, 3, 'operator'),
            ('0', 6, 0, 'number'), ('.', 6, 2, 'number'), ('=', 6, 3, 'equals')
        ]
        
        self.styles = {
            'number': {'bg': '#E5E7EB', 'fg': '#512DA8', 'activebackground': '#D1D5DB'}, # Light number, Deep Violet text
            'operator': {'bg': '#FF4081', 'fg': 'white', 'activebackground': '#EC4899'},  # Pink operator
            'control': {'bg': '#512DA8', 'fg': 'white', 'activebackground': '#8E24AA'},   # Deep Violet Control
            'equals': {'bg': '#FF4081', 'fg': 'white', 'activebackground': '#EC4899'}     # Pink equals
        }
        
        for (text, row, col, type) in buttons:
            self.create_button(text, row, col, type)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        spacer = tk.Frame(master, bg="#E5E7EB")
        spacer.grid(row=6, column=1, sticky="nsew")


    def create_button(self, text, row, col, type):
        style = self.styles[type]
        button = tk.Button(self.master, text=text, font=('Inter', 20), bd=0, relief=tk.FLAT, 
                           command=lambda t=text: self.click_button(t), 
                           padx=15, pady=15, width=4, 
                           **style)
        if text == '0':
            button.grid(row=row, column=col, columnspan=2, sticky="ew", padx=5, pady=5)
        elif text == '.':
            button.grid(row=row, column=2, sticky="ew", padx=5, pady=5)
        else:
            button.grid(row=row, column=col, sticky="ew", padx=5, pady=5)


    def update_display(self):
        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.current_input)
        self.entry.config(state='readonly')
        
        display_exp = self.expression.replace('/', '÷').replace('*', '×')
        
        if display_exp == self.current_input:
            self.secondary_display.config(text="")
        else:
            self.secondary_display.config(text=display_exp)


    def click_button(self, text):
        
        # --- Handle Clear (AC) ---
        if text == 'AC':
            self.current_input = "0"
            self.expression = ""
            self.update_display()
            return

        if self.current_input == "Error":
            self.current_input = "0"
            self.expression = ""
        
        # --- Handle Equals (=) ---
        if text == '=':
            try:
                safe_expression = self.expression.replace('÷', '/').replace('×', '*')
                
                if '%' in safe_expression:
                    safe_expression = safe_expression.replace('%', '/100')

                result = eval(safe_expression)
                self.current_input = str(round(result, 10))
                self.expression = self.current_input
                self.secondary_display.config(text=safe_expression.replace('/', '÷').replace('*', '×') + " =")

            except (SyntaxError, ZeroDivisionError, TypeError):
                self.current_input = "Error"
                self.expression = ""
            
            self.update_display()
            return
            
        # --- Handle Operators (+, -, ×, ÷) ---
        if text in ('+', '-', '×', '÷'):
            operator = text.replace('×', '*').replace('÷', '/')
            
            if self.expression and self.expression[-1] in ('+', '-', '*', '/'):
                self.expression = self.expression[:-1] + operator
            else:
                self.expression += operator
                
            self.current_input = "0"
            self.update_display()
            return
            
        # --- Handle Number/Decimal Input ---
        if text.isdigit() or text == '.':
            if self.current_input == "0" and text != '.':
                self.current_input = text
                if self.expression and self.expression[-1].isdigit():
                    self.expression = self.expression[:-1] + text
                else:
                    self.expression += text
            elif text == '.' and '.' in self.current_input:
                return
            else:
                self.current_input += text
                self.expression += text
        
        # --- Handle Sign Change (±) ---
        if text == '±':
            if self.current_input == "0":
                return
            
            last_op_index = max(self.expression.rfind('+'), self.expression.rfind('-'), 
                               self.expression.rfind('*'), self.expression.rfind('/'))
            
            if last_op_index == -1:
                start_index = 0
            else:
                start_index = last_op_index + 1
                
            old_num_str = self.expression[start_index:]
            
            if old_num_str:
                new_num = str(-float(old_num_str))
                self.expression = self.expression[:start_index] + new_num
                self.current_input = new_num
            
        # --- Handle Percentage (%) ---
        if text == '%':
            if self.current_input == "0" or not self.current_input:
                return
            
            percentage_value = str(float(self.current_input) / 100)
            
            last_op_index = max(self.expression.rfind('+'), self.expression.rfind('-'), 
                               self.expression.rfind('*'), self.expression.rfind('/'))
            
            if last_op_index == -1:
                self.expression = percentage_value
            else:
                self.expression = self.expression[:last_op_index + 1] + percentage_value
            self.current_input = percentage_value
        self.update_display()


# --- Main Application Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
    for i in range(2, 7):
        root.grid_rowconfigure(i, weight=1)

    app = CalculatorApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import filedialog
import re

def convert_to_assembly(java_code):

    # Regular expression pattern to match arithmetic operations
    arithmetic_pattern = r'([a-zA-Z0-9_]+)\s*([+\-*\/])\s*([a-zA-Z0-9_]+)\s*;'

    # Regular expression pattern to match if statements
    if_statement_pattern = r'if\s*\(\s*([a-zA-Z0-9_]+)\s*(==|!=|<|<=|>|>=)\s*([a-zA-Z0-9_]+)\s*\)'

    # Generate the MIPS Assembly code from the Java code
    assembly_code = ""

    for line in java_code.splitlines():
        # Check for arithmetic statements
        matches = re.search(arithmetic_pattern, line)
        if matches:
            left_operand = matches.group(1)
            operator = matches.group(2)
            right_operand = matches.group(3)
            if operator == '+':
                instruction = 'add'
            elif operator == '-':
                instruction = 'sub'
            elif operator == '*':
                instruction = 'mul'
            else:
                instruction = 'div'
            assembly_code += f".text:\n"
            assembly_code += f".main:\n"
            assembly_code += f"   lw $t0 {left_operand}\n"
            assembly_code += f"   lw $t1 {right_operand}\n"
            assembly_code += f"   {instruction} $t2, $t0, $t1\n"
            assembly_code += f"   sw $t2\n"
            assembly_code += f"   li $v0, 4\n"
            assembly_code += f"   la $a0, $t2\n"
            assembly_code += f"   syscall\n"
            assembly_code += f".data:\n"
            assembly_code += f".ascizz\n"
            assembly_code += f"   {left_operand}: .word {left_operand}\n"
            assembly_code += f"   {right_operand}: .word {right_operand} "

            return assembly_code
        else:
            # Check for if statements
            matches = re.search(if_statement_pattern, line)
            if matches:
                left_operand = matches.group(1)
                operator = matches.group(2)
                right_operand = matches.group(3)
                if operator == '==':
                    branch = 'beq'
                elif operator == '!=':
                    branch = 'bne'
                elif operator == '<':
                    branch = 'blt'
                elif operator == '<=':
                    branch = 'ble'
                elif operator == '>':
                    branch = 'bgt'
                elif operator == '>=':
                    branch = 'bge'

                assembly_code += f".text:\n"
                assembly_code += f".main:\n"
                assembly_code += f" lw $t0, {left_operand}\n"
                assembly_code += f" lw $t1, {right_operand}\n"
                assembly_code += f" {branch} $t0, $t1, true_label\n"
                assembly_code += " j false_label\n"
                assembly_code += "true_label:\n"
                assembly_code += "  li $t2, 1\n"
                assembly_code += "  j end_label\n"
                assembly_code += "false_label:\n"
                assembly_code += "  li $t2, 0\n"
                assembly_code += "end_label:\n"
                assembly_code += f" sw $t2, {left_operand}\n"

                return assembly_code

    # Add your code here to convert Java code to assembly code
    while_loop_pattern = r'while\s*\(\s*([a-zA-Z0-9_]+)\s*<\s*(\d+)\s*\)'

    # Regular expression pattern to match print statements in Java
    print_statement_pattern = r'System\.out\.println\(\s*([a-zA-Z0-9_]+)\s*\)'


    # Generate the MIPS Assembly code from the Java code
    matches = re.search(while_loop_pattern, java_code)
    if matches:
        loop_variable = matches.group(1)
        end_value = matches.group(2)
        mips_code = f"""
        .text:
        .main:
            addi $t0, $zero, 0                
            addi $t1, $zero, {end_value}       
        loop_{loop_variable}:                     
            bge $t0, $t1, exit_{loop_variable}   
            move $a0, $t0
            li $v0, 1
            syscall
            addi $t0, $t0, 1                  
            j loop_{loop_variable}              
        exit_{loop_variable}:                     
            """

        return mips_code
    #here tokenizing the for loop loop

    for_loop_pattern = r'for\s*\(\s*int\s+([a-zA-Z0-9_]+)\s*\=s*(\d+)\s*;\s*([a-zA-Z0-9_]+)\s*<\s*(\d+)\s*;\s*([a-zA-Z0-9_]+)\s*\+\+\s*\)'
    for_loop_body_pattern = r'\{[\s\S]*?\}'
    print_statement_pattern = r'System\.out\.println\(\s*([a-zA-Z0-9_]+)\s*\)'


    matches = re.search(for_loop_pattern, java_code)
    if matches:
        loop_variable = matches.group(1)
        start_value = matches.group(2)
        end_value = matches.group(4)
        loop_increment = matches.group(5)
        mips_code = f"""
        .text:
        .main:
            addi $t0, $zero, {start_value}     
            addi $t1, $zero, {end_value}       
        loop_{loop_variable}:                     
            bge $t0, $t1, exit_{loop_variable}   
            addi $t0, $t0, 1
            j loop_{loop_variable}              
        exit_{loop_variable}:                     
            """
        # Replace any print statements in the loop body with corresponding MIPS Assembly code
        loop_body = re.search(for_loop_body_pattern, java_code).group(0)
        print_statements = re.findall(print_statement_pattern, loop_body)
        for var_name in print_statements:
            mips_code = mips_code.replace(f'System.out.println({var_name})',
                                          f'li $v0, 1\nmove $a0, {var_name}\nsyscall')
        return mips_code
    else:
        return "Invalid for loop syntax"


    return "Assembly code generated from Java code"

# Function to handle the "Convert" button click event
def convert_click():
    java_code = java_textbox.get("1.0", "end-1c")
    assembly_code = convert_to_assembly(java_code)
    assembly_textbox.delete("1.0", "end")
    assembly_textbox.insert("1.0", assembly_code)

def save_click():
    assembly_code = assembly_textbox.get("1.0", "end-1c")
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        with open(filename, 'w') as file:
            file.write(assembly_code)
# Create a new GUI window
window = tk.Tk()
window.title("Your Java Compiler")

# Create a label for the Java code textbox
java_label = tk.Label(window, text="write Your Java Code Here")
java_label.pack()

# Create a textbox for users to input Java code
java_textbox = tk.Text(window, height=15, width=120)
java_textbox.pack()

# Create a label for the Assembly code textbox
assembly_label = tk.Label(window, text="Assembly Code: output")
assembly_label.pack()

# Create a textbox to display the generated assembly code
assembly_textbox = tk.Text(window, height=15, width=100, foreground="blue")
assembly_textbox.pack()


# Create a "Convert" button to convert the Java code to assembly code
convert_button = tk.Button(window, text="Compile", command=convert_click, background="green", width=60)
convert_button.pack()


# Create a "Save" button to save the generated assembly code to a file
save_button = tk.Button(window, text="Save", command=save_click, width=40, background="grey")
save_button.pack()


# Start the GUI event loop
window.mainloop()


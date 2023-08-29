
from tkinter import *
# font module must be called explicitly cuz it is not defined in __all__ in __init__.py 
from tkinter import font
from tkmacosx import Button as macButton
import re


class patterns : 
    
    # patterns so when should screen_entry be deleted automatically
    patterns_dict = {"pattern" : r"\W?\d+\W?\d*=\W?\d+"}

    @staticmethod
    def add_pattern(name , pattern : str) :
        patterns.patterns_dict[name] = pattern
    
    @staticmethod
    def del_pattern(name) : 
        if name in patterns.patterns_dict:
            del patterns.patterns_dict[name]
            
            
            
            
            
            
            

class gui: 
    window = Tk()
    window.title("Calculator")
    custom_font = font.Font(family="Helvetica" , size = 30 )
    
    #output screen
    screen_entry = None
    
    number_buttons_dict = {}
    other_buttons = {"AC" : (1,0,"white") , "+/-":(1,1,"white") , "%":(1,2,"white") , "/":(1,3,"orange") , "*":(2,3,"orange") , "-":(3,3,"orange") , "+":(4,3,"orange") , "0":(5,0 ,"gray") , ".":(5,2,"gray") , "=":(5,3,"orange")}

    
    number_inputs = []
    number_buttons_dict = {}
    
    
    @staticmethod
    def create_output_screen() :
        screen_entry = Entry(gui.window , font = gui.custom_font)
        screen_entry.grid(row=0 , column=0 ,columnspan=4)
        screen_entry.insert(0,0)
        gui.screen_entry = screen_entry
        
        
    
    #buttons from 1_9
    @staticmethod
    def create_number_buttons():
        counter = 0 
        row_index = 4
        for i in range(1,10 ) : 
            number_button = macButton(gui.window , text = f"{i}" , pady = 20, borderwidth=0,bg = "gray",command = lambda x = i: clickOperations._button_click(x))
            number_button.grid(row = row_index , column = counter)
            gui.number_buttons_dict[f"button{i}"] = number_button
            counter+=1
            if counter==3 : 
                counter=0
                row_index-=1
                
      
    @staticmethod
    def create_other_buttons() :
        for button_symbol , screen_position in gui.other_buttons.items() : 
            row , column , color  = screen_position
            if button_symbol!="0" and button_symbol!="=":
                button = macButton(gui.window , text = button_symbol , pady=20 , bg=color , command = lambda symbol = button_symbol: clickOperations._button_click(symbol))
                button.grid(row = row , column = column)
            elif button_symbol=="0" : 
                button = macButton(gui.window , text = button_symbol , padx = 50 ,pady=20 , bg=color , command = lambda symbol = button_symbol : clickOperations._button_click(symbol))
                button.grid(row = row , column = column , columnspan = 2)
            else :
                button = macButton(gui.window , text = button_symbol , pady=20 , bg=color , command = lambda symbol = button_symbol: clickOperations._equal_click())
                button.grid(row = row , column = column)
                
    @staticmethod
    def _screen_display_result(evaluate_expression_result) :
        gui.screen_entry.insert(END,str(evaluate_expression_result) )
        gui.number_inputs.clear()

            
    @staticmethod 
    def start_main_loop() :
        gui.window.mainloop()
            
            
class clickOperations  :
    
    @staticmethod
    def _button_click(button):
        if button=="AC" or re.search(patterns.patterns_dict["pattern"] , gui.screen_entry.get()):
            gui.screen_entry.delete(0,END)
        else :
            if gui.screen_entry.get()=="0" :
                gui.screen_entry.delete(0,END)
            gui.screen_entry.insert(END,button)
    
    @staticmethod
    def _equal_click() : 
        expression = gui.screen_entry.get()
        gui.screen_entry.insert(END,"=")
        result = eval(expression)
        gui.screen_entry.insert(END,result)


gui.create_output_screen()
gui.create_number_buttons()
gui.create_other_buttons()
gui.start_main_loop()

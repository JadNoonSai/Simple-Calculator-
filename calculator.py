
from tkinter import Button,Tk,Entry,END
# font module must be called explicitly cuz it is not defined in __all__ in __init__.py 
from tkinter import font
from tkmacosx import Button as macButton
import re


class patterns : 
    
    # patterns so when should screen_entry be deleted automatically
    patterns_dict = {"pattern" : r"\W?\d+\W?\d*=\W?\d+"}

    @classmethod
    def add_pattern(cls,name , pattern : str) :
        cls.patterns_dict[name] = pattern
    
    @classmethod
    def del_pattern(cls,name) : 
        if name in cls.patterns_dict:
            del cls.patterns_dict[name]
            
            
            
            
            
            
            

class Gui: 
    window = Tk()
    window.title("Calculator")
    custom_font = font.Font(family="Helvetica" , size = 30 )
    
    #output screen
    screen_entry = None
    
    number_buttons_dict = {}
    other_buttons = {"AC" : (1,0,"white") , "+/-":(1,1,"white") , "%":(1,2,"white") , "/":(1,3,"orange") , "*":(2,3,"orange") , "-":(3,3,"orange") , "+":(4,3,"orange") , "0":(5,0 ,"gray") , ".":(5,2,"gray") , "=":(5,3,"orange")}

    
    number_inputs = []
    number_buttons_dict = {}
    
    
    @classmethod
    def create_output_screen(cls) :
        screen_entry = Entry(cls.window , font = cls.custom_font)
        screen_entry.grid(row=0 , column=0 ,columnspan=4)
        screen_entry.insert(0,0)
        cls.screen_entry = screen_entry
        
        
    
    #buttons from 1_9
    @classmethod
    def create_number_buttons(cls):
        counter = 0 
        row_index = 4
        for i in range(1,10 ) : 
            number_button = macButton(cls.window , text = f"{i}" , pady = 20, borderwidth=0,bg = "gray",command = lambda x = i: ClickOperations._button_click(x))
            number_button.grid(row = row_index , column = counter)
            cls.number_buttons_dict[f"button{i}"] = number_button
            counter+=1
            if counter==3 : 
                counter=0
                row_index-=1
                
      
    @classmethod
    def create_other_buttons(cls) :
        for button_symbol , screen_position in cls.other_buttons.items() : 
            row , column , color  = screen_position
            if button_symbol!="0" and button_symbol!="=":
                button = macButton(cls.window , text = button_symbol , pady=20 , bg=color , command = lambda symbol = button_symbol: ClickOperations._button_click(symbol))
                button.grid(row = row , column = column)
            elif button_symbol=="0" : 
                button = macButton(cls.window , text = button_symbol , padx = 50 ,pady=20 , bg=color , command = lambda symbol = button_symbol : ClickOperations._button_click(symbol))
                button.grid(row = row , column = column , columnspan = 2)
            else :
                button = macButton(cls.window , text = button_symbol , pady=20 , bg=color , command = lambda symbol = button_symbol: ClickOperations._equal_click())
                button.grid(row = row , column = column)
                
    @classmethod
    def _screen_display_result(cls,evaluate_expression_result) :
        cls.screen_entry.insert(END,str(evaluate_expression_result) )
        cls.number_inputs.clear()

            
    @classmethod
    def start_main_loop(cls) :
        cls.window.mainloop()
            
            
class ClickOperations  :
    
    @staticmethod
    def _button_click(button):
        if button=="AC" :
            Gui.screen_entry.delete(0,END)
        else :
            if Gui.screen_entry.get()=="0" or re.search(patterns.patterns_dict["pattern"] , Gui.screen_entry.get()) or Gui.screen_entry.get().endswith("Error"):
                Gui.screen_entry.delete(0,END)
            if button=="+/-" :
                 Gui.screen_entry.insert(0,"-")
            else : Gui.screen_entry.insert(END,button)
    
    @staticmethod
    def _equal_click() : 
        expression = Gui.screen_entry.get()
        Gui.screen_entry.insert(END,"=")
        try : result = eval(expression)
        except ZeroDivisionError : Gui.screen_entry.insert(END,"Error")
        Gui.screen_entry.insert(END,result)


Gui.create_output_screen()
Gui.create_number_buttons()
Gui.create_other_buttons()
Gui.start_main_loop()

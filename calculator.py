
from tkinter import Button,Tk,Entry,END
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
            number_button = macButton(gui.window , text = f"{i}" , pady = 20, borderwidth=0,bg = "gray",command = lambda x = i: clickOperations._number_click(x))
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
            if button_symbol!="0":
                button = macButton(gui.window , text = button_symbol , pady=20 , bg=color , command = lambda symbol = button_symbol: clickOperations._number_click(symbol))
                button.grid(row = row , column = column)
            else : 
                button = macButton(gui.window , text = button_symbol , padx = 50 ,pady=20 , bg=color , command = lambda symbol = button_symbol : clickOperations._number_click(symbol))
                button.grid(row = row , column = column , columnspan = 2)
    
    @staticmethod
    def _screen_display_result(evaluate_expression_result) :
        gui.screen_entry.insert(END,str(evaluate_expression_result) )
        gui.number_inputs.clear()

            
    @staticmethod 
    def start_main_loop() :
        gui.window.mainloop()
            
            





#operations to perform when clicking on a number
class clickOperations: 
    @staticmethod
    def _number_click(num) :
        if num=="AC" : 
            gui.screen_entry.delete(0,END)
            gui.number_inputs.clear()   
        else : 
            if gui.screen_entry.get()=="0" or re.search(patterns.patterns_dict["pattern"] , gui.screen_entry.get()) or gui.screen_entry.get().endswith("Error") : 
                gui.screen_entry.delete(0,END)
            gui.screen_entry.insert(END , num)
            gui.number_inputs.append(str(num))
            clickOperations._perform_operation()
            
         
        
    @staticmethod
    def _perform_operation() : 
        # when we calculate "a+b="
        if "+" in gui.number_inputs or "-" in gui.number_inputs or "/"in gui.number_inputs or "*" in gui.number_inputs or "%" in gui.number_inputs :
            if "=" in gui.number_inputs:
                result = clickOperations._evaluate_expression(gui.number_inputs)
                gui._screen_display_result(result)
                
        # when we flip sign , example : press 5 , then press +/- , the other way around isnt supported
        elif len(gui.number_inputs)>1 and gui.number_inputs[-1]=="+/-":
            gui.screen_entry.delete(0,END)
            string ="".join(gui.number_inputs[:-1])
            result = -(eval(string))
            gui.screen_entry.insert(0,str(result))
            gui.number_inputs.clear()
            gui.number_inputs.append(str(result))  
        
        #when we calculate "a="
        elif len(gui.number_inputs)>1 and gui.number_inputs[-1]=="=" :
            result = clickOperations._evaluate_expression(gui.number_inputs)
            gui._screen_display_result(result)
        
        #when we click "=" alone"
        elif len(gui.number_inputs)==1 and gui.number_inputs[0]=="=" : 
            gui.screen_entry.delete(0,END)
            gui.number_inputs.clear()
            
            
    
    @staticmethod
    def _evaluate_expression(number_inputs):
        string ="".join(number_inputs)
        try : result = eval(string[:-1])
        except ZeroDivisionError as ZDE:
            return "Error"
        else: 
            return result 
    





gui.create_output_screen()
gui.create_number_buttons()
gui.create_other_buttons()
gui.start_main_loop()

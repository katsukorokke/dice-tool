from dice import Dice

dice = Dice(6)

roll_command = "r"
end_command = "e"

while(True):
    user_input = input(f"サイコロを振るなら'{roll_command}'、終了するなら'{end_command}'を入力 >>")
    
    if user_input == roll_command:
        print(f"出た目: {dice.roll()}")
    elif user_input == end_command:
        print("終了")
        break
        
        

            
         
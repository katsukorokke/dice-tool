from dice import Dice

dice_list = [Dice(6)]

roll_command = "r"
end_command = "e"

add_command = "u"
remove_command = "d"

def input_int(message: str, message_on_not_int: str) -> int:
    while (True):
        user_input = input(message)
        try:
            return int(user_input) 
        except TypeError:
            print(message_on_not_int)
            
def input_int_list(message: str, message_on_not_int: str) -> list[int]:
    while (True):
        user_input = input(message)
        try:
            return list(map(lambda x: int(x), user_input.split(",")))
        except TypeError, ValueError:
            print(message_on_not_int)
            
def display_dice_list():
    print("サイコロリスト")
    for i, dice in enumerate(dice_list):
        print(f"{i}: {dice}")

while(True):
    user_input = input(f"サイコロを振るなら'{roll_command}'、終了するなら'{end_command}'、サイコロを増やすなら'{add_command}'、減らすなら'{remove_command}'を入力 >>")
    
    if user_input == roll_command:
        print(f"出た目: {",".join(list(map(lambda dice: f"{dice.roll()}", dice_list)))}")
    elif user_input == end_command:
        print("終了")
    elif user_input == add_command:
        dices = input_int_list("サイコロをいくつ追加しますか？個数分の面数をコンマ区切りで入力 >>", "数値を入力してください") 
        
        for dice_face in dices:
            dice = Dice(dice_face)
            dice_list.append(dice)
            
            print(f"{dice}が追加されました")
        
    elif user_input == remove_command:
        display_dice_list()
        dice_indexes = input_int_list(f"どのサイコロを削除しますか？半角数値で入力してください。コンマ区切りで複数削除。 >>", "数値を入力してください")
    
        for index in range(len(dice_indexes)):
            if (0 <= dice_indexes[index] < len(dice_list)):
                dice_list_index = dice_indexes[index]
                
                print(f"{index}: {dice_list[dice_list_index]} が削除されました")
                dice_list.pop(dice_list_index)
                
                for other_index in range(index, len(dice_indexes)):
                    if other_index > index:
                        dice_indexes[other_index] -= 1
                
                
        
        

            
         
from dataclasses import dataclass
from dice import Dice

class DiceList:
    @dataclass
    class DiceListRecord:
        dice_index: int
        dice: str
    
    
    def __init__(self) -> None:
        self._dice_list: list[Dice] = []
        
    
    def add_dice(self, dice_faces: list[int]) -> list[DiceListRecord]:
        if len(dice_faces) == 0: return []
        records = []
        
        for dice_face in dice_faces:
            dice = Dice(dice_face)
            self._dice_list.append(dice)
            
            record = DiceList.DiceListRecord(len(self._dice_list) - 1, str(dice))
            records.append(record)
            
        return records
    
    def remove_dice(self, dice_indexes: list[int]) -> list[DiceListRecord]:
        if len(dice_indexes) == 0: return []
        
        records = []
        
        current_index = -1
        
        for dice_index in sorted(dice_indexes, reverse=True):
            if dice_index < 0: continue
            
            if current_index == dice_index:
                continue
            else:

                current_index = dice_index
            
            if len(self._dice_list) < dice_index: return records
            
            removed_dice = self._dice_list.pop(dice_index)
            
            record = DiceList.DiceListRecord(dice_index, str(removed_dice))
            records.append(record)
            
            
        return records
    
    def get_dice_list(self):
        return [DiceList.DiceListRecord(i, str(dice)) for [i, dice] in enumerate(self._dice_list)]
            
    
    def roll(self):
        return [dice.roll() for dice in self._dice_list]      

dice_list = DiceList()

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

def print_section_sep():
    print("==========================================================")
    
def print_records(records: list[DiceList.DiceListRecord]):
    if not records: print("特にありません")
    for record in records: print(f"{record.dice_index}: {record.dice}")

def print_dice_list(list: DiceList):
    for record in list.get_dice_list(): print(f"{record.dice_index}: {record.dice}")

while(True):
    user_input = input(f"サイコロを振るなら'{roll_command}'、終了するなら'{end_command}'、サイコロを増やすなら'{add_command}'、減らすなら'{remove_command}'を入力 >>")
    
    print_section_sep()
    
    if user_input == roll_command:
        print(f"出た目: {",".join(map(str, dice_list.roll()))}")
    elif user_input == end_command:
        print("終了")
        break
    elif user_input == add_command:
        dices = input_int_list("サイコロをいくつ追加しますか？個数分の面数をコンマ区切りで入力 >>", "数値を入力してください") 
        records = dice_list.add_dice(dices)
        
        print_section_sep()
        
        print("追加されたダイス")
        print_records(records)
        
    elif user_input == remove_command:
        print_dice_list(dice_list)
        
        print_section_sep()
        
        dice_indexes = input_int_list(f"どのサイコロを削除しますか？半角数値で入力してください。コンマ区切りで複数削除。 >>", "数値を入力してください")
        
        records = dice_list.remove_dice(dice_indexes)
        
        print_section_sep()    
        
        print("削除されたダイス")
        print_records(records)
        
    else:
        print("何もしません")
        
    print_section_sep()
    
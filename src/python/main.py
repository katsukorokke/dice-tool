from dataclasses import dataclass
from dice import Dice

class DiceTool:
    @dataclass
    class DiceListRecord:
        dice_index: int
        dice: str
    
    
    def __init__(self) -> None:
        self._dice_list: list[Dice] = []
    
    def add_dices(self, dice_faces: list[int]) -> list[DiceListRecord]:
        if not dice_faces: return []
        records = []
        
        for dice_face in dice_faces:
            if dice_face == 0: continue
            
            dice = Dice(dice_face)
            self._dice_list.append(dice)
            
            record = DiceTool.DiceListRecord(len(self._dice_list) - 1, str(dice))
            records.append(record)
            
        return records
    
    def remove_dices(self, dice_indexes: list[int]) -> list[DiceListRecord]:
        if not dice_indexes or not self._dice_list: return []
        
        edge = len(self._dice_list) - 1
        records = []

        for dice_index in sorted(list(set(dice_indexes)), reverse=True): 
            if dice_index < 0 or edge < dice_index: continue
            
            removed_dice = self._dice_list.pop(dice_index)
            
            record = DiceTool.DiceListRecord(dice_index, str(removed_dice))
            records.append(record)
            
        return records
    
    def get_dice_list(self):
        return [DiceTool.DiceListRecord(i, str(dice)) for [i, dice] in enumerate(self._dice_list)]         
    
    def roll_all(self):
        return [dice.roll() for dice in self._dice_list]     

    def clear_dices(self):
        records = self.get_dice_list()
        
        self._dice_list.clear()
        
        return records

    def set_dices(self, dice_faces: list[int])-> list[DiceListRecord]:
        self.clear_dices()
        return self.add_dices(dice_faces)
        
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
    
def print_records(records: list[DiceTool.DiceListRecord]):
    if not records: print("特にありません")
    for record in records: print(f"{record.dice_index}: {record.dice}")

def print_dice_list(list: DiceTool):
    for record in list.get_dice_list(): print(f"{record.dice_index}: {record.dice}")

class DiceToolCUI:
    ROLL = "r"
    SHOW = "s"
    
    ADD = "u"
    REMOVE = "d"

    END = "e"
    HELP = "h"
    
    def __init__(self, tool: DiceTool) -> None:
        self.tool = tool
    
    def roll_dices(self):
        print(f"出た目: {",".join(map(str, self.tool.roll_all()))}")
    
    def add_dices(self):
        list = input_int_list("複数追加可能。面数をコンマ区切りで入力 >>", "無効な形式です")
        
        records = self.tool.add_dices(list)
        
        print("追加されたサイコロ")
        print_records(records)
        
    def remove_dices(self):
        print("サイコロ一覧")
        print_dice_list(self.tool)
        
        list = input_int_list("複数削除可能。サイコロ位置をコンマ区切りで入力 >>", "無効な形式です")
        records = self.tool.remove_dices(list)
        
        print("削除されたサイコロ")
        print_records(records)
        
    def show_dice(self):
        print("サイコロ一覧")
        print_dice_list(self.tool)
    
    def help(self):
        print(f"'{DiceToolCUI.ROLL}': すべてのサイコロを振ります")
        print(f"'{DiceToolCUI.SHOW}': サイコロ一覧を表示します")
        print(f"'{DiceToolCUI.ADD}': サイコロを追加します")
        print(f"'{DiceToolCUI.REMOVE}': サイコロを削除します")
        print(f"'{DiceToolCUI.HELP}': ヘルプを表示します")
        print(f"'{DiceToolCUI.END}': 終了します")
    
    def input_loop(self) -> bool:
        user_input = input(f"操作を入力 >>")
        
        match user_input:
            case DiceToolCUI.ROLL:
                self.roll_dices()
            case DiceToolCUI.SHOW:
                self.show_dice()
            case DiceToolCUI.ADD:
                self.add_dices()
            case DiceToolCUI.REMOVE:
                self.remove_dices()
            case DiceToolCUI.HELP:
                self.help()
            case DiceToolCUI.END:
                return False
             
        return True 
     
    def start(self):
        loop = True
        
        while(loop):
           loop = self.input_loop()      
    
dice_list = DiceTool()
interface = DiceToolCUI(dice_list)

interface.start()


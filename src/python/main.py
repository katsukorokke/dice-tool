from dataclasses import dataclass
from dice import Dice
import json
from pathlib import Path

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
    
    def get_dices_data(self):
        return [dice.face for dice in self._dice_list]
    
    def click_roll(self, count, face):
        dice = Dice(face)
        
        return [dice.roll() for _ in range(count)]
             
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

def is_int(number: str):
    try:
        int(number)
    except TypeError:
        return False
    
    return True
    
class JsonStorage:
    def __init__(self, directory: Path):
        self.current_directory = directory
    
    def save(self, name, data):
        path = self.current_directory / f"{name}.json"
        path.touch(exist_ok=True)
                
        with path.open("w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def load(self, name):
        path = self.current_directory / f"{name}.json"
        
        if not path.is_file(): return None
                    
        with path.open("r", encoding="UTF-8") as f:
            data = json.load(f)
        
        return data 
    
    def get_all_file(self):
        return self.current_directory.iterdir()

class DiceToolCUI:
    ROLL = "r"
    SHOW = "s"
    
    ADD = "u"
    REMOVE = "d"

    END = "e"
    HELP = "h"
    
    SAVE = "k"
    LOAD = "c"
    
    PRESET = "p"
    
    def __init__(self, tool: DiceTool, presets: JsonStorage) -> None:
        self.tool = tool
        self.presets = presets
    
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
        print(f"'{DiceToolCUI.SAVE}': 現在のサイコロの並びを保存します")
        print(f"'{DiceToolCUI.LOAD}': 保存したサイコロの並びを読み込みます")
        print(f"'{DiceToolCUI.PRESET}': 保存したサイコロの並びを取得します")
        print(f"'{DiceToolCUI.HELP}': ヘルプを表示します")
        print(f"'<数値1>d<数値2>': <数値1>つの<数値2>面ダイスを振ります" )
        print(f"'{DiceToolCUI.END}': 終了します")
    
    def save(self):
        while (True):
            name = input(f"新しいプリセット名を入力。'{DiceToolCUI.END}'でキャンセル >>")
            if (name == DiceToolCUI.END): break
            
            self.presets.save(name, self.tool.get_dices_data())
            print(f"プリセット名: {name}としてセーブしました。")
            break
            
    
    def load(self):
        preset_list = self.preset()
        
        while (True):
            id = input(f"ロードするプリセット番号を入力。'{DiceToolCUI.END}'でキャンセル >>")
            if (id == DiceToolCUI.END): break
            if not is_int(id) or int(id) >= len(preset_list):
                print("番号が無効です")
                break
            
            name = preset_list[int(id)]
            
            data = self.presets.load(name)
            
            if data is None:
                break
            
            self.tool.set_dices(data)
            
            print(f"プリセット名: {name}をロードしました")
            break
        
    def preset(self):
        preset_list = []
        
        for [i, preset] in enumerate(self.presets.get_all_file()):
            name = preset.name[:-5]
            print(f"{i}: {name}")
            preset_list.append(name)
            
        return preset_list
        
                    
    def input_loop(self) -> bool:
        user_input = input(f"操作を入力 >>")
        
        [count, face] = user_input.split("d")
        
        if is_int(count) and is_int(face):
            print(f"出た目 :{",".join(map(str, self.tool.click_roll(int(count), int(face))))}")
            return True
            
        
        match user_input:
            case DiceToolCUI.ROLL: self.roll_dices()
            case DiceToolCUI.SHOW: self.show_dice()
            case DiceToolCUI.ADD: self.add_dices()
            case DiceToolCUI.REMOVE: self.remove_dices()
            case DiceToolCUI.HELP: self.help()
            case DiceToolCUI.SAVE: self.save()
            case DiceToolCUI.LOAD: self.load()
            case DiceToolCUI.PRESET: self.preset()
            case DiceToolCUI.END: return False
             
        return True 
     
    def start(self):
        loop = True
        
        while(loop):
           loop = self.input_loop()      

CURRENT_DIRECTORY = Path(__file__).resolve().parent

storage = JsonStorage(CURRENT_DIRECTORY / "presets")    

dice_list = DiceTool()
interface = DiceToolCUI(dice_list, storage)

interface.start()


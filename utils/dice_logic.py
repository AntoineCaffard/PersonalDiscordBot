import random as rd
import re

class DiceRoller:

    @staticmethod
    def parse(dice_str : str) :

        match = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", dice_str.strip())

        if not match:
            raise ValueError(f"Format invalide : {dice_str}")
        
        num_dice = int(match.group(1))
        num_faces = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        
        if num_dice <= 0 or num_faces <= 0 or num_dice > 200:
            raise ValueError("Nombre de dés et de faces doit être >= 1 et nombre de dés <= 200")
        
        return num_dice, num_faces, modifier
    
    @staticmethod
    def roll(num_dice : int, num_faces: int):

        result = [rd.randint(1, num_faces) for _ in range(num_dice)]
        return result


    @staticmethod
    def applyModifier(values_iterable, modifier):

        return [max(1, values + modifier) for values in values_iterable]
    
    @staticmethod
    def apply_sum_modifier(values_iterable, modifier):

        return sum(values_iterable) + modifier

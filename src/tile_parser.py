import re
from typing import List, Dict, Set
from enum import Enum

class TileType(Enum):
    """麻將牌的花色"""
    MAN = 'm'  # 萬子
    PIN = 'p'  # 筒子
    SOU = 's'  # 索子
    HONOR = 'z'  # 字牌

class Tile:
    """代表一張麻將牌"""
    def __init__(self, number: int, tile_type: TileType):
        self.number = number  # 1-9 for man/pin/sou, 1-7 for honor
        self.tile_type = tile_type
    
    def __repr__(self):
        return f"{self.number}{self.tile_type.value}"
    
    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.number == other.number and self.tile_type == other.tile_type
    
    def __hash__(self):
        return hash((self.number, self.tile_type))

class TileParser:
    """牌型解析器 - 將字符串解析為牌對象"""
    
    def __init__(self):
        self.tile_types = {
            'm': TileType.MAN,
            'p': TileType.PIN,
            's': TileType.SOU,
            'z': TileType.HONOR
        }
    
    def parse(self, hand_str: str) -> List[Tile]:
        """
        解析手牌字符串為牌列表
        
        Args:
            hand_str: 如 "123m456p789s1122z"
        
        Returns:
            Tile 對象列表
        
        Raises:
            ValueError: 如果格式無效
        """
        hand_str = hand_str.strip().lower()
        
        if not hand_str:
            raise ValueError("手牌不能為空")
        
        tiles = []
        current_numbers = []
        
        for char in hand_str:
            if char.isdigit():
                current_numbers.append(int(char))
            elif char in self.tile_types:
                if not current_numbers:
                    raise ValueError(f"無效格式：{char} 前沒有數字")
                
                tile_type = self.tile_types[char]
                
                for num in current_numbers:
                    if tile_type == TileType.HONOR:
                        if num < 1 or num > 7:
                            raise ValueError(f"字牌數字必須在1-7之間，得到 {num}")
                    else:
                        if num < 1 or num > 9:
                            raise ValueError(f"數牌數字必須在1-9之間，得到 {num}")
                    tiles.append(Tile(num, tile_type))
                
                current_numbers = []
            else:
                raise ValueError(f"無效字符：{char}")
        
        if current_numbers:
            raise ValueError(f"末尾有未匹配的數字：{current_numbers}")
        
        return tiles
    
    def to_string(self, tiles: List[Tile]) -> str:
        """
        將牌列表轉換為字符串格式
        
        Args:
            tiles: Tile 對象列表
        
        Returns:
            格式化的字符串，如 "123m456p"
        """
        result = {}
        for tile in tiles:
            tile_type = tile.tile_type.value
            if tile_type not in result:
                result[tile_type] = []
            result[tile_type].append(tile.number)
        
        output = ""
        for tile_type in ['m', 'p', 's', 'z']:
            if tile_type in result:
                numbers = sorted(result[tile_type])
                output += ''.join(str(n) for n in numbers) + tile_type
        
        return output
    
    def normalize(self, tiles: List[Tile]) -> List[Tile]:
        """
        標準化牌列表（排序）
        
        Args:
            tiles: 牌列表
        
        Returns:
            排序後的牌列表
        """
        type_order = {'m': 0, 'p': 1, 's': 2, 'z': 3}
        return sorted(tiles, key=lambda t: (type_order[t.tile_type.value], t.number))
    
    def count_tiles_by_type(self, tiles: List[Tile]) -> Dict[str, List[int]]:
        """
        按花色統計牌
        
        Args:
            tiles: 牌列表
        
        Returns:
            {'m': [1,2,3,...], 'p': [...], ...}
        """
        result = {'m': [], 'p': [], 's': [], 'z': []}
        for tile in tiles:
            tile_type = tile.tile_type.value
            result[tile_type].append(tile.number)
        
        for key in result:
            result[key].sort()
        
        return result

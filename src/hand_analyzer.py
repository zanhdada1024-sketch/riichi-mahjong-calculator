from typing import List, Tuple, Optional
from .tile_parser import Tile, TileType
from collections import Counter

class HandAnalyzer:
    """手牌分析器 - 分析手牌結構和勝利條件"""
    
    def is_winning_hand(self, tiles: List[Tile]) -> bool:
        """
        判斷是否是和牌 - 使用改進的標準麻將和牌判定
        
        Args:
            tiles: 14張牌
        
        Returns:
            是否為有效和牌
        """
        if len(tiles) != 14:
            return False
        
        # 計算牌的計數
        tile_counter = Counter((t.tile_type.value, t.number) for t in tiles)
        
        # 嘗試每一種牌作為對子
        for (tile_type, number), count in tile_counter.items():
            if count >= 2:
                # 移除對子
                remaining = tile_counter.copy()
                remaining[(tile_type, number)] -= 2
                if remaining[(tile_type, number)] == 0:
                    del remaining[(tile_type, number)]
                
                # 檢查剩餘12張牌是否能組成4個面子
                if self._can_form_melds_from_counter(remaining):
                    return True
        
        return False
    
    def _can_form_melds_from_counter(self, tile_counter: Counter) -> bool:
        """
        使用計數器檢查牌是否能組成面子
        
        Args:
            tile_counter: 牌的計數字典
        
        Returns:
            是否能組成面子
        """
        if sum(tile_counter.values()) == 0:
            return True
        
        # 複製計數器以便修改
        remaining = tile_counter.copy()
        
        # 找第一個非零的牌
        first_tile = None
        for tile_key in sorted(remaining.keys()):
            if remaining[tile_key] > 0:
                first_tile = tile_key
                break
        
        if first_tile is None:
            return True
        
        tile_type, number = first_tile
        
        # 嘗試形成刻子 (triplet: 3張相同的牌)
        if remaining[(tile_type, number)] >= 3:
            remaining[(tile_type, number)] -= 3
            if self._can_form_melds_from_counter(remaining):
                return True
            remaining[(tile_type, number)] += 3
        
        # 嘗試形成順子 (sequence: n, n+1, n+2)
        # 順子只適用於數牌（不是字牌）
        if tile_type in ['m', 'p', 's'] and number <= 7:
            if remaining[(tile_type, number + 1)] > 0 and remaining[(tile_type, number + 2)] > 0:
                remaining[(tile_type, number)] -= 1
                remaining[(tile_type, number + 1)] -= 1
                remaining[(tile_type, number + 2)] -= 1
                
                if self._can_form_melds_from_counter(remaining):
                    return True
                
                remaining[(tile_type, number)] += 1
                remaining[(tile_type, number + 1)] += 1
                remaining[(tile_type, number + 2)] += 1
        
        return False
    
    def _group_by_type(self, tiles: List[Tile]) -> dict:
        """
        按花色分組
        """
        result = {}
        for tile in tiles:
            tile_type = tile.tile_type.value
            if tile_type not in result:
                result[tile_type] = []
            result[tile_type].append(tile.number)
        
        for key in result:
            result[key].sort()
        
        return result
    
    def _can_form_melds(self, tiles: List[Tile]) -> bool:
        """
        檢查12張牌是否可以組成4個面子
        """
        if len(tiles) == 0:
            return True
        
        if len(tiles) % 3 != 0:
            return False
        
        tiles_by_type = self._group_by_type(tiles)
        
        # 遞迴嘗試形成面子
        return self._try_form_melds(tiles_by_type)
    
    def _try_form_melds(self, tiles_by_type: dict) -> bool:
        """
        遞迴地嘗試形成面子
        """
        # 檢查是否所有都已處理
        total_tiles = sum(len(v) for v in tiles_by_type.values())
        if total_tiles == 0:
            return True
        
        # 找第一個非空花色
        for tile_type in ['m', 'p', 's', 'z']:
            if tile_type in tiles_by_type and len(tiles_by_type[tile_type]) > 0:
                # 嘗試形成刻子
                if tiles_by_type[tile_type].count(tiles_by_type[tile_type][0]) >= 3:
                    first_num = tiles_by_type[tile_type][0]
                    # 移除3張相同的牌
                    for _ in range(3):
                        tiles_by_type[tile_type].remove(first_num)
                    
                    if self._try_form_melds(tiles_by_type):
                        return True
                    
                    # 恢復
                    for _ in range(3):
                        tiles_by_type[tile_type].append(first_num)
                    tiles_by_type[tile_type].sort()
                
                # 嘗試形成順子（只適用於數牌）
                if tile_type in ['m', 'p', 's']:
                    first_num = tiles_by_type[tile_type][0]
                    if first_num <= 7 and first_num + 1 in tiles_by_type[tile_type] and first_num + 2 in tiles_by_type[tile_type]:
                        # 移除順子
                        tiles_by_type[tile_type].remove(first_num)
                        tiles_by_type[tile_type].remove(first_num + 1)
                        tiles_by_type[tile_type].remove(first_num + 2)
                        
                        if self._try_form_melds(tiles_by_type):
                            return True
                        
                        # 恢復
                        tiles_by_type[tile_type].extend([first_num, first_num + 1, first_num + 2])
                        tiles_by_type[tile_type].sort()
                
                return False
        
        return False
    
    def analyze_hand_structure(self, tiles: List[Tile]) -> dict:
        """
        分析手牌結構
        
        Returns:
            包含手牌信息的字典
        """
        tiles_by_type = self._group_by_type(tiles)
        
        return {
            'tiles_by_type': tiles_by_type,
            'tile_count': len(tiles),
            'has_terminal': self._has_terminal(tiles),
            'has_honor': self._has_honor(tiles),
            'color_count': self._count_colors(tiles)
        }
    
    def _has_terminal(self, tiles: List[Tile]) -> bool:
        """
        檢查是否有么九牌
        """
        for tile in tiles:
            if tile.tile_type != TileType.HONOR:
                if tile.number == 1 or tile.number == 9:
                    return True
        return False
    
    def _has_honor(self, tiles: List[Tile]) -> bool:
        """
        檢查是否有字牌
        """
        for tile in tiles:
            if tile.tile_type == TileType.HONOR:
                return True
        return False
    
    def _count_colors(self, tiles: List[Tile]) -> int:
        """
        計算花色數量
        """
        colors = set()
        for tile in tiles:
            if tile.tile_type != TileType.HONOR:
                colors.add(tile.tile_type.value)
        return len(colors)

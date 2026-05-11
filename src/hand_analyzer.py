from typing import List, Tuple, Optional
from tile_parser import Tile, TileType
from collections import Counter

class HandAnalyzer:
    """手牌分析器 - 分析手牌結構和勝利條件"""
    
    def is_winning_hand(self, tiles: List[Tile]) -> bool:
        """
        判斷是否是和牌
        
        Args:
            tiles: 14張牌
        
        Returns:
            是否為有效和牌
        """
        if len(tiles) != 14:
            return False
        
        # 檢查是否滿足基本和牌條件
        # 1. 有1對
        # 2. 剩餘12張可組成4個面子
        
        # 按花色分組
        tiles_by_type = self._group_by_type(tiles)
        
        # 嘗試所有可能的對子
        for pair_tile in set(tiles):
            remaining = tiles.copy()
            if remaining.count(pair_tile) >= 2:
                remaining.remove(pair_tile)
                remaining.remove(pair_tile)
                
                if self._can_form_melds(remaining):
                    return True
        
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
                
                # 嘗試形成順子
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

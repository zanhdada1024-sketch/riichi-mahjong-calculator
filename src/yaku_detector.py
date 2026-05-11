from typing import List, Tuple
from tile_parser import Tile, TileType
from collections import Counter

class YakuDetector:
    """役種判定器 - 識別和牌的役種"""
    
    def __init__(self):
        # 定義所有役種
        self.yaku_list = {
            'riichi': {'han': 1, 'name': '立直'},
            'menzen_tsumo': {'han': 1, 'name': '門前清模和'},
            'pinfu': {'han': 1, 'name': '平胡'},
            'tanyao': {'han': 1, 'name': '斷么九'},
            'iipeiko': {'han': 1, 'name': '一盃口'},
            'sanshoku_doujun': {'han': 2, 'name': '三色同順'},
            'ittsu': {'han': 2, 'name': '一氣通貫'},
            'sanshoku_doukou': {'han': 2, 'name': '三色同刻'},
            'sankantsu': {'han': 2, 'name': '三槓子'},
            'sanankou': {'han': 2, 'name': '三暗刻'},
            'shousangen': {'han': 2, 'name': '小三元'},
            'honroutou': {'han': 2, 'name': '混老頭'},
            'honchantaghan': {'han': 3, 'name': '混全帶么九'},
            'honisou': {'han': 3, 'name': '混一色'},
            'chiisou': {'han': 5, 'name': '清一色'},
            'kokushi': {'han': 13, 'name': '國士無双'},
            'daisangen': {'han': 13, 'name': '大三元'},
            'daisushi': {'han': 13, 'name': '大四喜'},
            'chinroutou': {'han': 13, 'name': '清老頭'},
            'tsuisou': {'han': 13, 'name': '字一色'},
            'ryuisou': {'han': 13, 'name': '綠一色'},
            'suankou': {'han': 13, 'name': '四暗刻'},
            'chuuren_poutou': {'han': 13, 'name': '九蓮寶燈'},
        }
    
    def detect_yaku(self, tiles: List[Tile], is_tsumo: bool = False) -> List[Tuple[str, int, int]]:
        """
        檢測手牌中的役種
        
        Args:
            tiles: 14張牌
            is_tsumo: 是否是自摸
        
        Returns:
            [(役名, 番數, 符數), ...]
        """
        detected = []
        tiles_by_type = self._group_by_type(tiles)
        
        # 檢測各種役種
        if self._is_tanyao(tiles):
            detected.append(('斷么九', 1, 30))
        
        if self._is_pinfu(tiles):
            detected.append(('平胡', 1, 30))
        
        if self._is_honroutou(tiles):
            detected.append(('混老頭', 2, 30))
        
        if self._is_honisou(tiles):
            detected.append(('混一色', 3, 30))
        
        if self._is_chiisou(tiles):
            detected.append(('清一色', 5, 30))
        
        if self._is_kokushi(tiles):
            detected.append(('國士無双', 13, 30))
        
        if self._is_tsuisou(tiles):
            detected.append(('字一色', 13, 30))
        
        if not detected:
            detected.append(('通常役', 1, 30))
        
        return detected
    
    def _group_by_type(self, tiles: List[Tile]) -> dict:
        """按花色分組"""
        result = {}
        for tile in tiles:
            tile_type = tile.tile_type.value
            if tile_type not in result:
                result[tile_type] = []
            result[tile_type].append(tile.number)
        
        for key in result:
            result[key].sort()
        
        return result
    
    def _is_tanyao(self, tiles: List[Tile]) -> bool:
        """斷么九 - 所有牌都是2-8"""
        for tile in tiles:
            if tile.tile_type == TileType.HONOR:
                return False
            if tile.number == 1 or tile.number == 9:
                return False
        return True
    
    def _is_pinfu(self, tiles: List[Tile]) -> bool:
        """平胡 - 無刻子，無么九對"""
        # 簡化版本，實際需要複雜的組合檢查
        has_honor = any(t.tile_type == TileType.HONOR for t in tiles)
        has_terminal = any(t.number in [1, 9] for t in tiles if t.tile_type != TileType.HONOR)
        
        return not has_honor and not has_terminal
    
    def _is_honroutou(self, tiles: List[Tile]) -> bool:
        """混老頭 - 全部是么九牌和字牌"""
        tiles_by_type = self._group_by_type(tiles)
        
        # 檢查所有牌
        for tile in tiles:
            if tile.tile_type == TileType.HONOR:
                continue
            if tile.number != 1 and tile.number != 9:
                return False
        
        # 必須有字牌
        return any(t.tile_type == TileType.HONOR for t in tiles)
    
    def _is_honisou(self, tiles: List[Tile]) -> bool:
        """混一色 - 一種數牌花色 + 字牌"""
        tiles_by_type = self._group_by_type(tiles)
        
        # 計算數牌花色數
        colors = []
        for tile_type in ['m', 'p', 's']:
            if tile_type in tiles_by_type and len(tiles_by_type[tile_type]) > 0:
                colors.append(tile_type)
        
        # 必須只有一種數牌花色，且有字牌
        return len(colors) == 1 and 'z' in tiles_by_type
    
    def _is_chiisou(self, tiles: List[Tile]) -> bool:
        """清一色 - 只有一種花色的數牌"""
        tiles_by_type = self._group_by_type(tiles)
        
        # 計算數牌花色數
        colors = []
        for tile_type in ['m', 'p', 's']:
            if tile_type in tiles_by_type and len(tiles_by_type[tile_type]) > 0:
                colors.append(tile_type)
        
        # 不能有字牌
        return len(colors) == 1 and 'z' not in tiles_by_type
    
    def _is_kokushi(self, tiles: List[Tile]) -> bool:
        """國士無双 - 13種么九牌各一張，加一對"""
        kokushi_tiles = []
        # 萬子：1, 9
        for i in [1, 9]:
            kokushi_tiles.append(('m', i))
        # 筒子：1, 9
        for i in [1, 9]:
            kokushi_tiles.append(('p', i))
        # 索子：1, 9
        for i in [1, 9]:
            kokushi_tiles.append(('s', i))
        # 字牌：1-7
        for i in range(1, 8):
            kokushi_tiles.append(('z', i))
        
        # 檢查是否包含所有13種么九牌
        tile_set = set((t.tile_type.value, t.number) for t in tiles)
        kokushi_set = set(kokushi_tiles)
        
        return len(tile_set & kokushi_set) == 13
    
    def _is_tsuisou(self, tiles: List[Tile]) -> bool:
        """字一色 - 所有牌都是字牌"""
        for tile in tiles:
            if tile.tile_type != TileType.HONOR:
                return False
        return True

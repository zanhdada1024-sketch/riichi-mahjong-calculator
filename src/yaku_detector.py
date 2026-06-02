from typing import List, Tuple
from .tile_parser import Tile, TileType
from collections import Counter

class YakuDetector:
    """役種判定器 - 識別和牌的役種"""
    
    def __init__(self):
        # 定義所有役種（優先級順序）
        self.all_yakus = {
            # 役滿
            'kokushi': {'han': 13, 'name': '國士無双', 'fu': 30},
            'daisangen': {'han': 13, 'name': '大三元', 'fu': 30},
            'suankou': {'han': 13, 'name': '四暗刻', 'fu': 30},
            'tsuisou': {'han': 13, 'name': '字一色', 'fu': 30},
            'chinroutou': {'han': 13, 'name': '清老頭', 'fu': 30},
            'shousangen': {'han': 3, 'name': '小三元', 'fu': 30},
            'honroutou': {'han': 2, 'name': '混老頭', 'fu': 30},
            'honchantaghan': {'han': 3, 'name': '混全帶么九', 'fu': 30},
            'chiisou': {'han': 6, 'name': '清一色', 'fu': 30},
            'honisou': {'han': 3, 'name': '混一色', 'fu': 30},
            'ittsu': {'han': 2, 'name': '一氣通貫', 'fu': 30},
            'sanshoku_doujun': {'han': 2, 'name': '三色同順', 'fu': 30},
            'sanshoku_doukou': {'han': 2, 'name': '三色同刻', 'fu': 30},
            'sankantsu': {'han': 2, 'name': '三槓子', 'fu': 30},
            'sanankou': {'han': 2, 'name': '三暗刻', 'fu': 30},
            'tanyao': {'han': 1, 'name': '斷么九', 'fu': 30},
            'iipeiko': {'han': 1, 'name': '一盃口', 'fu': 30},
            'pinfu': {'han': 1, 'name': '平胡', 'fu': 30},
            'menzen_tsumo': {'han': 1, 'name': '門前清模和', 'fu': 30},
            'riichi': {'han': 1, 'name': '立直', 'fu': 30},
        }
    
    def detect_all_yakus(self, tiles: List[Tile], is_tsumo: bool = False) -> dict:
        """
        檢測所有可能的役種及其對應情況
        
        Args:
            tiles: 14張牌
            is_tsumo: 是否是自摸
        
        Returns:
            {'役名': {'han': X, 'possible': True/False}, ...}
        """
        result = {}
        
        # 檢查所有役種
        result['國士無双'] = self._check_kokushi(tiles)
        result['字一色'] = self._check_tsuisou(tiles)
        result['清老頭'] = self._check_chinroutou(tiles)
        result['清一色'] = self._check_chiisou(tiles)
        result['大三元'] = self._check_daisangen(tiles)
        result['四暗刻'] = self._check_suankou(tiles)
        result['混老頭'] = self._check_honroutou(tiles)
        result['混全帶么九'] = self._check_honchantaghan(tiles)
        result['混一色'] = self._check_honisou(tiles)
        result['小三元'] = self._check_shousangen(tiles)
        result['一氣通貫'] = self._check_ittsu(tiles)
        result['三色同順'] = self._check_sanshoku_doujun(tiles)
        result['三色同刻'] = self._check_sanshoku_doukou(tiles)
        result['三槓子'] = self._check_sankantsu(tiles)
        result['三暗刻'] = self._check_sanankou(tiles)
        result['斷么九'] = self._check_tanyao(tiles)
        result['一盃口'] = self._check_iipeiko(tiles)
        result['平胡'] = self._check_pinfu(tiles)
        result['門前清模和'] = self._check_menzen_tsumo(tiles)
        result['立直'] = {'han': 1, 'possible': False}  # 需要外部設定
        
        return result
    
    def detect_yaku(self, tiles: List[Tile], is_tsumo: bool = False) -> List[Tuple[str, int, int]]:
        """
        檢測手牌中最高的役種（簡化版，返回第一個匹配的）
        """
        detected = []
        
        # 按優先級檢測
        if self._is_kokushi(tiles):
            detected.append(('國士無双', 13, 30))
        elif self._is_tsuisou(tiles):
            detected.append(('字一色', 13, 30))
        elif self._is_chinroutou(tiles):
            detected.append(('清老頭', 13, 30))
        elif self._is_chiisou(tiles):
            detected.append(('清一色', 6, 30))
        elif self._is_daisangen(tiles):
            detected.append(('大三元', 13, 30))
        elif self._is_honroutou(tiles):
            detected.append(('混老頭', 2, 30))
        elif self._is_honisou(tiles):
            detected.append(('混一色', 3, 30))
        elif self._is_honchantaghan(tiles):
            detected.append(('混全帶么九', 3, 30))
        elif self._is_tanyao(tiles):
            detected.append(('斷么九', 1, 30))
        elif self._is_pinfu(tiles):
            detected.append(('平胡', 1, 30))
        else:
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
    
    # ============================================================
    # 役種檢測方法
    # ============================================================
    
    def _check_kokushi(self, tiles: List[Tile]) -> dict:
        """國士無双"""
        return {'han': 13, 'possible': self._is_kokushi(tiles)}
    
    def _is_kokushi(self, tiles: List[Tile]) -> bool:
        """國士無双 - 13種么九牌各一張，加一對"""
        kokushi_tiles = set()
        for i in [1, 9]:
            kokushi_tiles.add(('m', i))
        for i in [1, 9]:
            kokushi_tiles.add(('p', i))
        for i in [1, 9]:
            kokushi_tiles.add(('s', i))
        for i in range(1, 8):
            kokushi_tiles.add(('z', i))
        
        tile_set = [(t.tile_type.value, t.number) for t in tiles]
        tile_counter = Counter(tile_set)
        
        # 需要13種不同的么九牌，且有一對
        unique_kokushi = len([t for t in tile_set if t in kokushi_tiles])
        if unique_kokushi != 14:
            return False
        
        # 檢查是否所有都是么九牌
        for t in tile_set:
            if t not in kokushi_tiles:
                return False
        
        return True
    
    def _check_tsuisou(self, tiles: List[Tile]) -> dict:
        """字一色"""
        return {'han': 13, 'possible': self._is_tsuisou(tiles)}
    
    def _is_tsuisou(self, tiles: List[Tile]) -> bool:
        """字一色 - 所有牌都是字牌"""
        for tile in tiles:
            if tile.tile_type != TileType.HONOR:
                return False
        return True
    
    def _check_chinroutou(self, tiles: List[Tile]) -> dict:
        """清老頭"""
        return {'han': 13, 'possible': self._is_chinroutou(tiles)}
    
    def _is_chinroutou(self, tiles: List[Tile]) -> bool:
        """清老頭 - 全部是么九牌（無字牌）"""
        for tile in tiles:
            if tile.tile_type == TileType.HONOR:
                return False
            if tile.number != 1 and tile.number != 9:
                return False
        return True
    
    def _check_chiisou(self, tiles: List[Tile]) -> dict:
        """清一色"""
        return {'han': 6, 'possible': self._is_chiisou(tiles)}
    
    def _is_chiisou(self, tiles: List[Tile]) -> bool:
        """清一色 - 只有一種花色的數牌"""
        tiles_by_type = self._group_by_type(tiles)
        colors = [t for t in ['m', 'p', 's'] if t in tiles_by_type and len(tiles_by_type[t]) > 0]
        return len(colors) == 1 and 'z' not in tiles_by_type
    
    def _check_daisangen(self, tiles: List[Tile]) -> dict:
        """大三元"""
        return {'han': 13, 'possible': self._is_daisangen(tiles)}
    
    def _is_daisangen(self, tiles: List[Tile]) -> bool:
        """大三元 - 白、發、中都是刻子"""
        tile_list = [(t.tile_type.value, t.number) for t in tiles]
        
        # 檢查是否有白、發、中
        white_count = tile_list.count(('z', 5))
        green_count = tile_list.count(('z', 6))
        red_count = tile_list.count(('z', 7))
        
        return white_count >= 3 and green_count >= 3 and red_count >= 3
    
    def _check_suankou(self, tiles: List[Tile]) -> dict:
        """四暗刻"""
        return {'han': 13, 'possible': self._is_suankou(tiles)}
    
    def _is_suankou(self, tiles: List[Tile]) -> bool:
        """四暗刻 - 四組刻子都是暗刻"""
        # 簡化版本：檢查是否有4組相同的牌
        tile_counter = Counter((t.tile_type.value, t.number) for t in tiles)
        triplets = sum(1 for count in tile_counter.values() if count >= 3)
        return triplets == 4
    
    def _check_honroutou(self, tiles: List[Tile]) -> dict:
        """混老頭"""
        return {'han': 2, 'possible': self._is_honroutou(tiles)}
    
    def _is_honroutou(self, tiles: List[Tile]) -> bool:
        """混老頭 - 全部是么九牌和字牌"""
        has_honor = False
        for tile in tiles:
            if tile.tile_type == TileType.HONOR:
                has_honor = True
            elif tile.number != 1 and tile.number != 9:
                return False
        return has_honor
    
    def _check_honisou(self, tiles: List[Tile]) -> dict:
        """混一色"""
        return {'han': 3, 'possible': self._is_honisou(tiles)}
    
    def _is_honisou(self, tiles: List[Tile]) -> bool:
        """混一色 - 一種數牌花色 + 字牌"""
        tiles_by_type = self._group_by_type(tiles)
        colors = [t for t in ['m', 'p', 's'] if t in tiles_by_type and len(tiles_by_type[t]) > 0]
        return len(colors) == 1 and 'z' in tiles_by_type
    
    def _check_honchantaghan(self, tiles: List[Tile]) -> dict:
        """混全帶么九"""
        return {'han': 3, 'possible': self._is_honchantaghan(tiles)}
    
    def _is_honchantaghan(self, tiles: List[Tile]) -> bool:
        """混全帶么九 - 每組都帶么九，且有字牌"""
        has_honor = any(t.tile_type == TileType.HONOR for t in tiles)
        if not has_honor:
            return False
        
        # 簡化檢查：有字牌且有么九數牌
        has_terminal = any(t.number in [1, 9] for t in tiles if t.tile_type != TileType.HONOR)
        return has_terminal
    
    def _check_shousangen(self, tiles: List[Tile]) -> dict:
        """小三元"""
        return {'han': 3, 'possible': self._is_shousangen(tiles)}
    
    def _is_shousangen(self, tiles: List[Tile]) -> bool:
        """小三元 - 白、發、中中有兩組刻子，一對"""
        tile_list = [(t.tile_type.value, t.number) for t in tiles]
        white_count = tile_list.count(('z', 5))
        green_count = tile_list.count(('z', 6))
        red_count = tile_list.count(('z', 7))
        
        # 兩個3張，一個2張
        counts = sorted([white_count, green_count, red_count])
        return counts == [2, 3, 3]
    
    def _check_ittsu(self, tiles: List[Tile]) -> dict:
        """一氣通貫"""
        return {'han': 2, 'possible': self._is_ittsu(tiles)}
    
    def _is_ittsu(self, tiles: List[Tile]) -> bool:
        """一氣通貫 - 1-9順子各一個"""
        tiles_by_type = self._group_by_type(tiles)
        
        # 需要同一花色有1-9的所有數字
        for suit in ['m', 'p', 's']:
            if suit in tiles_by_type:
                nums = set(tiles_by_type[suit])
                if {1, 2, 3, 4, 5, 6, 7, 8, 9}.issubset(nums):
                    return True
        return False
    
    def _check_sanshoku_doujun(self, tiles: List[Tile]) -> dict:
        """三色同順"""
        return {'han': 2, 'possible': self._is_sanshoku_doujun(tiles)}
    
    def _is_sanshoku_doujun(self, tiles: List[Tile]) -> bool:
        """三色同順 - 三種花色都有相同的順子"""
        # 簡化版本
        tiles_by_type = self._group_by_type(tiles)
        if len(tiles_by_type) < 3:
            return False
        return 'm' in tiles_by_type and 'p' in tiles_by_type and 's' in tiles_by_type
    
    def _check_sanshoku_doukou(self, tiles: List[Tile]) -> dict:
        """三色同刻"""
        return {'han': 2, 'possible': self._is_sanshoku_doukou(tiles)}
    
    def _is_sanshoku_doukou(self, tiles: List[Tile]) -> bool:
        """三色同刻 - 三種花色的同一數字各有刻子"""
        tiles_by_type = self._group_by_type(tiles)
        if not ('m' in tiles_by_type and 'p' in tiles_by_type and 's' in tiles_by_type):
            return False
        
        # 簡化檢查：有三種花色各有3張以上
        return (len(tiles_by_type.get('m', [])) >= 3 and
                len(tiles_by_type.get('p', [])) >= 3 and
                len(tiles_by_type.get('s', [])) >= 3)
    
    def _check_sankantsu(self, tiles: List[Tile]) -> dict:
        """三槓子"""
        return {'han': 2, 'possible': self._is_sankantsu(tiles)}
    
    def _is_sankantsu(self, tiles: List[Tile]) -> bool:
        """三槓子 - 三個槓子"""
        # 簡化版本：檢查是否有多個4張的牌組
        tile_counter = Counter((t.tile_type.value, t.number) for t in tiles)
        quads = sum(1 for count in tile_counter.values() if count == 4)
        return quads >= 3
    
    def _check_sanankou(self, tiles: List[Tile]) -> dict:
        """三暗刻"""
        return {'han': 2, 'possible': self._is_sanankou(tiles)}
    
    def _is_sanankou(self, tiles: List[Tile]) -> bool:
        """三暗刻 - 三個暗刻"""
        # 簡化版本：檢查是否有多個3張的牌組
        tile_counter = Counter((t.tile_type.value, t.number) for t in tiles)
        triplets = sum(1 for count in tile_counter.values() if count >= 3)
        return triplets >= 3
    
    def _check_tanyao(self, tiles: List[Tile]) -> dict:
        """斷么九"""
        return {'han': 1, 'possible': self._is_tanyao(tiles)}
    
    def _is_tanyao(self, tiles: List[Tile]) -> bool:
        """斷么九 - 所有牌都是2-8"""
        for tile in tiles:
            if tile.tile_type == TileType.HONOR:
                return False
            if tile.number == 1 or tile.number == 9:
                return False
        return True
    
    def _check_iipeiko(self, tiles: List[Tile]) -> dict:
        """一盃口"""
        return {'han': 1, 'possible': self._is_iipeiko(tiles)}
    
    def _is_iipeiko(self, tiles: List[Tile]) -> bool:
        """一盃口 - 同樣的順子兩組"""
        # 簡化版本
        tile_counter = Counter((t.tile_type.value, t.number) for t in tiles)
        return max(tile_counter.values()) >= 2
    
    def _check_pinfu(self, tiles: List[Tile]) -> dict:
        """平胡"""
        return {'han': 1, 'possible': self._is_pinfu(tiles)}
    
    def _is_pinfu(self, tiles: List[Tile]) -> bool:
        """平胡 - 無刻子，無么九對"""
        has_honor = any(t.tile_type == TileType.HONOR for t in tiles)
        has_terminal = any(t.number in [1, 9] for t in tiles if t.tile_type != TileType.HONOR)
        return not has_honor and not has_terminal
    
    def _check_menzen_tsumo(self, tiles: List[Tile]) -> dict:
        """門前清模和"""
        return {'han': 1, 'possible': False}  # 需要外部設定
    
    def _check_riichi(self, tiles: List[Tile]) -> dict:
        """立直"""
        return {'han': 1, 'possible': False}  # 需要外部設定

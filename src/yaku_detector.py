from typing import List, Tuple
from .tile_parser import Tile, TileType
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
    
    def detect_all_yakus(self, tiles: List[Tile], is_tsumo: bool = False) -> dict:
        """
        檢測所有可能的役種（用於顯示）
        
        Args:
            tiles: 14張牌
            is_tsumo: 是否是自摸
        
        Returns:
            {'役名': {'possible': True/False, 'han': 翻數}, ...}
        """
        result = {}
        
        # 檢測每個役種
        for key, yaku_info in self.yaku_list.items():
            yaku_name = yaku_info['name']
            han = yaku_info['han']
            
            if key == 'tanyao':
                result[yaku_name] = {'possible': self._is_tanyao(tiles), 'han': han}
            elif key == 'pinfu':
                result[yaku_name] = {'possible': self._is_pinfu(tiles), 'han': han}
            elif key == 'honroutou':
                result[yaku_name] = {'possible': self._is_honroutou(tiles), 'han': han}
            elif key == 'honisou':
                result[yaku_name] = {'possible': self._is_honisou(tiles), 'han': han}
            elif key == 'chiisou':
                result[yaku_name] = {'possible': self._is_chiisou(tiles), 'han': han}
            elif key == 'kokushi':
                result[yaku_name] = {'possible': self._is_kokushi(tiles), 'han': han}
            elif key == 'tsuisou':
                result[yaku_name] = {'possible': self._is_tsuisou(tiles), 'han': han}
            elif key == 'menzen_tsumo':
                result[yaku_name] = {'possible': is_tsumo, 'han': han}
            elif key == 'chinroutou':
                result[yaku_name] = {'possible': self._is_chinroutou(tiles), 'han': han}
            elif key == 'chuuren_poutou':
                result[yaku_name] = {'possible': self._is_chuuren_poutou(tiles), 'han': han}
            elif key == 'daisangen':
                result[yaku_name] = {'possible': self._is_daisangen(tiles), 'han': han}
            elif key == 'daisushi':
                result[yaku_name] = {'possible': self._is_daisushi(tiles), 'han': han}
            elif key == 'ryuisou':
                result[yaku_name] = {'possible': self._is_ryuisou(tiles), 'han': han}
            elif key == 'suankou':
                result[yaku_name] = {'possible': self._is_suankou(tiles), 'han': han}
            else:
                result[yaku_name] = {'possible': False, 'han': han}
        
        return result
    
    def detect_yaku(self, tiles: List[Tile], is_tsumo: bool = False) -> List[Tuple[str, int, int]]:
        """
        檢測手牌中的所有成立役種（計算番數用）
        
        Args:
            tiles: 14張牌
            is_tsumo: 是否是自摸
        
        Returns:
            [(役名, 番數, 符數), ...]
        """
        detected = []
        
        # 先檢測特殊役種（役滿優先）
        if self._is_kokushi(tiles):
            detected.append(('國士無双', 13, 30))
            return detected
        
        if self._is_chuuren_poutou(tiles):
            detected.append(('九蓮寶燈', 13, 30))
            return detected
        
        if self._is_daisushi(tiles):
            detected.append(('大四喜', 13, 30))
            return detected
        
        if self._is_daisangen(tiles):
            detected.append(('大三元', 13, 30))
            return detected
        
        if self._is_tsuisou(tiles):
            detected.append(('字一色', 13, 30))
            return detected
        
        if self._is_ryuisou(tiles):
            detected.append(('綠一色', 13, 30))
            return detected
        
        if self._is_chinroutou(tiles):
            detected.append(('清老頭', 13, 30))
            return detected
        
        if self._is_suankou(tiles):
            detected.append(('四暗刻', 13, 30))
            return detected
        
        # 檢測一般役種（可複數成立）
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
        
        # 如果是自摸且沒有其他役，加上門清自摸
        if is_tsumo and not detected:
            detected.append(('門前清模和', 1, 30))
        
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
        has_honor = any(t.tile_type == TileType.HONOR for t in tiles)
        has_terminal = any(t.number in [1, 9] for t in tiles if t.tile_type != TileType.HONOR)
        
        return not has_honor and not has_terminal
    
    def _is_honroutou(self, tiles: List[Tile]) -> bool:
        """混老頭 - 全部是么九牌和字牌"""
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
        kokushi_tiles = [
            ('m', 1), ('m', 9),
            ('p', 1), ('p', 9),
            ('s', 1), ('s', 9),
            ('z', 1), ('z', 2), ('z', 3), ('z', 4), ('z', 5), ('z', 6), ('z', 7)
        ]
        
        tile_counter = Counter((t.tile_type.value, t.number) for t in tiles)
        kokushi_counter = Counter(kokushi_tiles)
        
        # 檢查是否包含所有13種么九牌
        for tile_type, num in kokushi_tiles:
            if tile_counter[(tile_type, num)] == 0:
                return False
        
        # 檢查是否剛好有一對某種么九牌
        has_pair = False
        for tile_type, num in kokushi_tiles:
            if tile_counter[(tile_type, num)] == 2:
                if has_pair:
                    return False
                has_pair = True
        
        return has_pair
    
    def _is_tsuisou(self, tiles: List[Tile]) -> bool:
        """字一色 - 所有牌都是字牌"""
        for tile in tiles:
            if tile.tile_type != TileType.HONOR:
                return False
        return True
    
    def _is_chinroutou(self, tiles: List[Tile]) -> bool:
        """清老頭 - 所有牌都是1,9和字牌"""
        for tile in tiles:
            if tile.tile_type == TileType.HONOR:
                continue
            if tile.number != 1 and tile.number != 9:
                return False
        
        # 必須有字牌
        return any(t.tile_type == TileType.HONOR for t in tiles)
    
    def _is_chuuren_poutou(self, tiles: List[Tile]) -> bool:
        """九蓮寶燈 - 清牌1112345678999+1"""
        tiles_by_type = self._group_by_type(tiles)
        
        # 必須是清牌（一種花色）
        colors = [t for t in ['m', 'p', 's'] if t in tiles_by_type and len(tiles_by_type[t]) > 0]
        if len(colors) != 1 or 'z' in tiles_by_type:
            return False
        
        color = colors[0]
        required = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9]
        hand = sorted(tiles_by_type[color])
        
        # 檢查是否包含所需的牌
        from collections import Counter
        required_counter = Counter(required)
        hand_counter = Counter(hand)
        
        return required_counter == hand_counter
    
    def _is_daisangen(self, tiles: List[Tile]) -> bool:
        """大三元 - 三個龍的三刻"""
        counter = Counter((t.tile_type.value, t.number) for t in tiles)
        
        # 需要5,6,7字牌各3張
        return (counter[('z', 5)] >= 3 and counter[('z', 6)] >= 3 and counter[('z', 7)] >= 3)
    
    def _is_daisushi(self, tiles: List[Tile]) -> bool:
        """大四喜 - 四個風的四刻"""
        counter = Counter((t.tile_type.value, t.number) for t in tiles)
        
        # 需要1,2,3,4字牌各3張
        return (counter[('z', 1)] >= 3 and counter[('z', 2)] >= 3 and 
                counter[('z', 3)] >= 3 and counter[('z', 4)] >= 3)
    
    def _is_ryuisou(self, tiles: List[Tile]) -> bool:
        """綠一色 - 只有2,3,4,6,8索和6字"""
        allowed = {('s', 2), ('s', 3), ('s', 4), ('s', 6), ('s', 8), ('z', 6)}
        
        for tile in tiles:
            if (tile.tile_type.value, tile.number) not in allowed:
                return False
        
        # 必須有6字（發）
        return any(t.tile_type == TileType.HONOR and t.number == 6 for t in tiles)
    
    def _is_suankou(self, tiles: List[Tile]) -> bool:
        """四暗刻 - 四個刻子"""
        counter = Counter((t.tile_type.value, t.number) for t in tiles)
        
        # 計算有多少個刻子
        triplets = 0
        pair = 0
        
        for count in counter.values():
            if count >= 3:
                triplets += count // 3
            if count % 3 == 2:
                pair += 1
        
        return triplets >= 4 and pair >= 1

from typing import Tuple

class PointsCalculator:
    """點數計算器 - 根據番符計算點數"""
    
    def __init__(self):
        # 點數對照表：(番, 符) -> (親自摸, 親榮和, 子自摸(親), 子自摸(子), 子榮和)
        self.points_table = self._init_points_table()
    
    def _init_points_table(self) -> dict:
        """初始化點數對照表"""
        table = {}
        
        # 1番
        table[(1, 30)] = {'parent_tsumo': 500, 'parent_ron': 1000, 'child_parent_tsumo': 300, 'child_child_tsumo': 100, 'child_ron': 1000}
        table[(1, 40)] = {'parent_tsumo': 700, 'parent_ron': 1300, 'child_parent_tsumo': 400, 'child_child_tsumo': 200, 'child_ron': 1300}
        table[(1, 50)] = {'parent_tsumo': 800, 'parent_ron': 1600, 'child_parent_tsumo': 400, 'child_child_tsumo': 200, 'child_ron': 1600}
        table[(1, 60)] = {'parent_tsumo': 1000, 'parent_ron': 2000, 'child_parent_tsumo': 500, 'child_child_tsumo': 300, 'child_ron': 2000}
        table[(1, 70)] = {'parent_tsumo': 1200, 'parent_ron': 2300, 'child_parent_tsumo': 600, 'child_child_tsumo': 300, 'child_ron': 2300}
        table[(1, 80)] = {'parent_tsumo': 1300, 'parent_ron': 2600, 'child_parent_tsumo': 700, 'child_child_tsumo': 300, 'child_ron': 2600}
        table[(1, 90)] = {'parent_tsumo': 1500, 'parent_ron': 2900, 'child_parent_tsumo': 800, 'child_child_tsumo': 400, 'child_ron': 2900}
        table[(1, 100)] = {'parent_tsumo': 1600, 'parent_ron': 3200, 'child_parent_tsumo': 800, 'child_child_tsumo': 400, 'child_ron': 3200}
        
        # 2番
        table[(2, 30)] = {'parent_tsumo': 1000, 'parent_ron': 2000, 'child_parent_tsumo': 500, 'child_child_tsumo': 300, 'child_ron': 2000}
        table[(2, 40)] = {'parent_tsumo': 1300, 'parent_ron': 2600, 'child_parent_tsumo': 700, 'child_child_tsumo': 400, 'child_ron': 2600}
        table[(2, 50)] = {'parent_tsumo': 1600, 'parent_ron': 3200, 'child_parent_tsumo': 800, 'child_child_tsumo': 400, 'child_ron': 3200}
        table[(2, 60)] = {'parent_tsumo': 2000, 'parent_ron': 3900, 'child_parent_tsumo': 1000, 'child_child_tsumo': 500, 'child_ron': 3900}
        table[(2, 70)] = {'parent_tsumo': 2300, 'parent_ron': 4500, 'child_parent_tsumo': 1200, 'child_child_tsumo': 600, 'child_ron': 4500}
        
        # 3番
        table[(3, 30)] = {'parent_tsumo': 2000, 'parent_ron': 3900, 'child_parent_tsumo': 1000, 'child_child_tsumo': 500, 'child_ron': 3900}
        table[(3, 40)] = {'parent_tsumo': 2600, 'parent_ron': 5200, 'child_parent_tsumo': 1300, 'child_child_tsumo': 700, 'child_ron': 5200}
        table[(3, 50)] = {'parent_tsumo': 3200, 'parent_ron': 6400, 'child_parent_tsumo': 1600, 'child_child_tsumo': 800, 'child_ron': 6400}
        table[(3, 60)] = {'parent_tsumo': 3900, 'parent_ron': 7700, 'child_parent_tsumo': 2000, 'child_child_tsumo': 1000, 'child_ron': 7700}
        
        # 4番
        table[(4, 30)] = {'parent_tsumo': 3900, 'parent_ron': 7700, 'child_parent_tsumo': 2000, 'child_child_tsumo': 1000, 'child_ron': 7700}
        table[(4, 40)] = {'parent_tsumo': 5200, 'parent_ron': 8000, 'child_parent_tsumo': 2600, 'child_child_tsumo': 1300, 'child_ron': 8000}
        
        # 滿貫 (5番 或 4番60符以上)
        table[(5, 0)] = {'parent_tsumo': 8000, 'parent_ron': 16000, 'child_parent_tsumo': 4000, 'child_child_tsumo': 2000, 'child_ron': 8000}
        table[(6, 0)] = {'parent_tsumo': 12000, 'parent_ron': 24000, 'child_parent_tsumo': 6000, 'child_child_tsumo': 3000, 'child_ron': 12000}
        table[(8, 0)] = {'parent_tsumo': 16000, 'parent_ron': 32000, 'child_parent_tsumo': 8000, 'child_child_tsumo': 4000, 'child_ron': 16000}
        table[(11, 0)] = {'parent_tsumo': 24000, 'parent_ron': 48000, 'child_parent_tsumo': 12000, 'child_child_tsumo': 6000, 'child_ron': 24000}
        table[(13, 0)] = {'parent_tsumo': 32000, 'parent_ron': 64000, 'child_parent_tsumo': 16000, 'child_child_tsumo': 8000, 'child_ron': 32000}
        
        return table
    
    def get_points(self, han: int, fu: int) -> dict:
        """
        根據番符查表獲取點數
        
        Args:
            han: 番數
            fu: 符數
        
        Returns:
            點數字典
        """
        # 判斷是否滿貫
        if han >= 5:
            mangan_key = (5, 0)
        elif han >= 4 and fu >= 40:
            mangan_key = (5, 0)
        elif han >= 3 and fu >= 70:
            mangan_key = (5, 0)
        else:
            mangan_key = None
        
        # 判斷是否跳滿
        if han >= 6:
            mangan_key = (6, 0)
        
        # 判斷是否倍滿
        if han >= 8:
            mangan_key = (8, 0)
        
        # 判斷是否三倍滿
        if han >= 11:
            mangan_key = (11, 0)
        
        # 判斷是否役滿
        if han >= 13:
            mangan_key = (13, 0)
        
        if mangan_key and mangan_key in self.points_table:
            return self.points_table[mangan_key]
        
        # 查表
        key = (han, fu)
        if key in self.points_table:
            return self.points_table[key]
        
        # 默認返回基礎點數
        return {'parent_tsumo': 1000, 'parent_ron': 2000, 'child_parent_tsumo': 500, 'child_child_tsumo': 300, 'child_ron': 2000}
    
    def calculate_parent_tsumo_payment(self, han: int, fu: int) -> int:
        """計算親自摸時，子家的支付額"""
        points = self.get_points(han, fu)
        return points.get('parent_tsumo', 1000)
    
    def calculate_parent_ron_payment(self, han: int, fu: int) -> int:
        """計算親榮和時的支付額"""
        points = self.get_points(han, fu)
        return points.get('parent_ron', 2000)
    
    def calculate_child_tsumo_parent_payment(self, han: int, fu: int) -> int:
        """計算子自摸時，親家的支付額"""
        points = self.get_points(han, fu)
        return points.get('child_parent_tsumo', 500)
    
    def calculate_child_tsumo_child_payment(self, han: int, fu: int) -> int:
        """計算子自摸時，子家的支付額"""
        points = self.get_points(han, fu)
        return points.get('child_child_tsumo', 300)
    
    def calculate_child_ron_payment(self, han: int, fu: int) -> int:
        """計算子榮和時的支付額"""
        points = self.get_points(han, fu)
        return points.get('child_ron', 2000)

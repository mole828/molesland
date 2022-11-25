'''
抽卡数据分析
uid {
    summary {

    }
    pool name {
        rar
    }
}
'''
from collections import defaultdict
analysts = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

from . import Gacha

def analystOne (gacha: Gacha):
    for char in gacha.chars:
        for pool in [
            analysts[''][''], 
            analysts[''][gacha.pool],
            analysts[gacha.uid][''],
            analysts[gacha.uid][gacha.pool],
        ]:
            pool[char.rarity]+=1





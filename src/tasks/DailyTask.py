import re

from ok import Logger, find_boxes_by_name, find_boxes_within_boundary
from src.tasks.BaseGfTask import BaseGfTask

logger = Logger.get_logger(__name__)


class DailyTask(BaseGfTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "一键日常"
        self.description = "收菜"
        self.default_config.update({
            '公共区': True,
            '购买免费礼包': True,
            '自动刷体力': True,
            '竞技场': True,
            '兵棋推演': True,
            '班组': True,
            '尘烟': True,
            '领任务': True,
            '大月卡': True,
            '邮件': True,
        })

    def run(self):
        # return self.choose_chenyan()
        self.ensure_main(recheck_time=2, time_out=90)
        if self.config.get('公共区'):
            self.gongongqu()
        if self.config.get('购买免费礼包'):
            self.shopping()
        if self.config.get('自动刷体力'):
            self.battle()
        if self.config.get('竞技场'):
            self.arena()
        if self.config.get('兵棋推演'):
            self.bingqi()
        if self.config.get('班组'):
            self.guild()

        if self.config.get('领任务'):
            self.claim_quest()
        if self.config.get('大月卡'):
            self.xunlu()
        if self.config.get('邮件'):
            self.mail()

    def claim_quest(self):
        self.info_set('current_task', 'claim_quest')
        self.wait_click_ocr(match=['委托'], box='bottom_right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['一键领取'], box='bottom_right', time_out=4,
                            raise_if_not_found=False, after_sleep=1)
        if self.wait_click_ocr(match=['领取全部', '无可领取报酬'], box='bottom_left', time_out=3, after_sleep=0.5):
            self.wait_pop_up()
        self.ensure_main()

    def mail(self):
        self.info_set('current_task', 'mail')
        self.click(0.07, 0.63)
        self.wait_click_ocr(match=['领取全部'], box='bottom_left', time_out=4, after_sleep=2, raise_if_not_found=False)

        self.ensure_main()

    def xunlu(self):
        self.info_set('current_task', 'xunlu')
        self.wait_click_ocr(match=['巡录'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['沿途行动'], box='top_right', time_out=4,
                            raise_if_not_found=True, after_sleep=1)
        self.wait_click_ocr(match=['一键领取'], box='bottom_right', time_out=4,
                            raise_if_not_found=False, after_sleep=1)

        self.ensure_main()

    def gongongqu(self):
        self.info_set('current_task', 'public area')
        self.wait_click_ocr(match=['公共区'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['调度室'], box='left', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['调度收益'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['取出'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['资源生产'], box='left', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['收取'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['点击空白处关闭'], box='bottom', after_sleep=0.5, raise_if_not_found=False)
        self.back()
        self.sleep(1)
        if self.wait_click_ocr(match=['一键领取'], box='bottom', after_sleep=1, time_out=5):
            self.wait_click_ocr(match=['再次派遣'], box='bottom', after_sleep=1, raise_if_not_found=False)
        self.back()
        self.ensure_main()

    def shopping(self):
        self.info_set('current_task', 'shopping')
        self.wait_click_ocr(match=['商城'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['品质甄选'], box='left', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['常驻礼包'], box='right', after_sleep=0.5, raise_if_not_found=True)
        if self.wait_click_ocr(match=['免费'], box='left', after_sleep=0.5, raise_if_not_found=False, time_out=4):
            self.log_info('found free item to buy')
            self.wait_click_ocr(match=['确认'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
            self.wait_click_ocr(match=['点击空白处关闭'], box='bottom', after_sleep=0.5, raise_if_not_found=False)
        self.ensure_main()

    def arena(self):
        self.info_set('current_task', 'arena')
        self.wait_click_ocr(match=['战役推进'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['模拟作战'], box='top_right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['实兵演习'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr_with_pop_up("进攻", box='bottom_right')
        count = self.challenge_arena_opponent()
        self.back()
        self.sleep(1)
        if count > 0:
            self.click_relative(0.34, 0.89, after_sleep=0.5)
            if not self.wait_ocr(match=['演习补给'], box='top', time_out=4):
                self.wait_pop_up(time_out=4)
        self.ensure_main()

    def bingqi(self):
        self.info_set('current_task', 'bingqi')
        self.wait_click_ocr(match=['战役推进'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['模拟作战'], box='top_right', after_sleep=0.5, raise_if_not_found=True)
        self.swipe_relative(0.8, 0.6, 0.5, 0.6, duration=1)
        self.sleep(0.5)
        self.wait_click_ocr(match=['兵棋推演'], box='bottom_right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_ocr(match='防御阵容', box='right', time_out=30, post_action=lambda: self.click_relative(0.5, 0.5))
        while self.find_top_right_count():
            self.info_incr('bingqi')
            self.wait_click_ocr(match=['匹配'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
            self.auto_battle()
            self.wait_ocr(match=['匹配'], box='bottom', raise_if_not_found=True, time_out=30)
        self.ensure_main()

    def guild(self):
        self.info_set('current_task', 'guild')
        self.wait_click_ocr(match=['班组'], box='bottom_right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['要务'], box='bottom_right', after_sleep=0.5, raise_if_not_found=True)
        result = self.wait_ocr(match=['开始作战', '每日要务已完成'], box='bottom_right',
                               raise_if_not_found=True, log=True)
        if result[0].name == '开始作战':
            self.click(result)
            self.auto_battle()
            self.wait_ocr(match=['开始作战', '每日要务已完成'], box='bottom_right', raise_if_not_found=True)
        else:
            self.log_info('每日要务已完成')
        self.back()
        self.sleep(1)
        self.chenyan()

        self.wait_click_ocr(match=['补给'], box='bottom_right', after_sleep=0.5)
        if result := self.wait_ocr(match=['领取全部'], box='bottom_right', time_out=4,
                                   raise_if_not_found=False):
            self.click_box(result)
            self.wait_pop_up()
        self.back()
        self.sleep(1)
        self.ensure_main()

    def chenyan(self):
        if not self.config.get('尘烟'):
            return
        end = self.ocr(match=re.compile('后结束'), box='bottom_right')
        if end:
            self.click(end, after_sleep=1)
        result = self.ocr(0.89, 0.01, 0.99, 0.1, match=re.compile(r"^\d+/\d+$"), box='top_right')
        if not result:
            raise Exception('找不到尘烟票')
        while True:
            tickets = int(result[0].name.split('/')[0])
            self.log_info(f'chenyan tickets {tickets}')
            self.info_set('chenyan tickets', tickets)
            if tickets == 0:
                break
            self.wait_click_ocr(match='攻坚战', box='top_right', after_sleep=0.5, raise_if_not_found=True)
            self.wait_click_ocr(match='开始作战', box='bottom_right', after_sleep=0.5, raise_if_not_found=True)
            self.choose_chenyan()
            self.sleep(2)
        self.back(after_sleep=2)

    def choose_chenyan(self):
        existing = self.ocr(box='bottom_right', match=re.compile(r"^\d+$"))
        if len(existing) < 4:
            for exist in existing:
                self.click_box(exist, after_sleep=0.1)
            chars = self.ocr(box='bottom_left', match=re.compile(r"^\d+$"))
            chars = sorted(chars, key=lambda obj: int(obj.name), reverse=True)
            for i in range(4):
                self.click_box(chars[i], after_sleep=0.01)
        self.wait_click_ocr(match='助战', box='bottom_right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match='火力', box='top_right', after_sleep=2, raise_if_not_found=True)
        priority = ['可露凯', '玛绮朵', '琼玖', '托洛洛']
        chars = self.ocr(0.18, 0.27, 0.82, 0.79, match=re.compile(r'^\D*$'))
        sorted_chars = sort_characters_by_priority(chars, priority)
        for char in sorted_chars:
            self.click(char, after_sleep=1)
            join = self.ocr(match='入队', box='bottom_right')
            if join:
                self.click_box(join, after_sleep=1)
                break
        self.wait_click_ocr(match='确定', box='bottom_right')
        self.auto_battle('开始作战', 'bottom_right')

    def wait_click_ocr_with_pop_up(self, match, box=None):
        if self.wait_until(lambda: self.do_wait_pop_up(match, box), time_out=10, raise_if_not_found=True):
            self.sleep(0.5)
            return True

    def do_wait_pop_up(self, match, box):
        boxes = self.ocr()
        if pop_up := find_boxes_by_name(boxes, '点击空白处关闭'):
            self.click(pop_up)
            return False
        elif click := find_boxes_by_name(boxes, match):
            if click := find_boxes_within_boundary(click, self.get_box_by_name(box)):
                self.click(click)
                return True

    def challenge_arena_opponent(self):
        challenged = 0
        waited_pop_up = False
        while True:
            remaining_count = int(self.ocr(0.89, 0.01, 0.99, 0.1)[0].name.split('/')[0])
            if remaining_count <= 1:
                self.log_info(f'challenge arena complete {remaining_count}')
                break
            boxes = self.ocr(0, 0.55, 0.94, 0.62, match=re.compile(r"^[1-9]\d*$"))
            if len(boxes) != 5:
                if not waited_pop_up:
                    waited_pop_up = True
                    self.wait_pop_up(time_out=15) and self.wait_pop_up(time_out=15) and self.wait_pop_up(time_out=15)
                    continue
                else:
                    raise Exception("找不到五个演习对手")
            self.log_info(f'arena opponents {boxes}')
            for box in boxes:
                if int(box.name) < 5000:
                    search_success = box.copy()
                    search_success.width = self.width_of_screen(0.17)
                    search_success.height = self.height_of_screen(0.15)
                    search_success.y -= search_success.height
                    if not self.ocr(match=re.compile('挑战'), box=search_success, log=True):
                        self.log_info(f'challenge opponent {box.name}')
                        self.click(box)
                        self.wait_click_ocr(match=['进攻'], box='bottom_right', after_sleep=0.5,
                                            raise_if_not_found=True)
                        self.auto_battle()
                        self.wait_ocr(match='刷新', box='bottom_right', raise_if_not_found=True,
                                      time_out=30)
                        challenged += 1
                        continue
            if self.ocr(match=['刷新消耗'], box='bottom_right'):
                self.log_info(f'no refresh count remains')
                return challenged
            self.wait_click_ocr(match='刷新', box='bottom_right', after_sleep=2, raise_if_not_found=True)
        return challenged

    def battle(self):
        self.info_set('current_task', 'battle')
        self.wait_click_ocr(match=['战役推进'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['补给作战'], box='top', after_sleep=0.5, raise_if_not_found=True)
        self.swipe_relative(0.8, 0.6, 0.5, 0.6, duration=1)
        self.sleep(1)
        self.wait_click_ocr(match=['标准同调'], box='right', after_sleep=0.5, raise_if_not_found=True)
        remaining = self.fast_combat()
        self.back()
        if remaining >= 10:
            self.wait_click_ocr(match=['军备解析'], box='left', after_sleep=0.5, raise_if_not_found=True,
                                post_action=lambda: self.back(after_sleep=2))
            while remaining >= 10:
                remaining = self.fast_combat()
        self.ensure_main()


def sort_characters_by_priority(chars, priority):
    """
    Sorts a list of character objects based on their 'charname' attribute,
    according to a priority list.

    Characters whose 'charname' attribute appears in the priority list are
    placed at the front, sorted by their order within the priority list.
    Characters not in the priority list retain their original order.

    Args:
        chars: A list of character objects, where each object has a 'charname' attribute (string).
        priority: A list of character names (strings) representing the priority order.

    Returns:
        A new list of character objects, sorted according to the priority.  The
        original `chars` list is not modified.
    """

    priority_map = {name: index for index, name in enumerate(priority)}

    def sort_key(char):
        """
        Helper function to determine the sort key for each character object.
        Returns a tuple: (priority_index, original_index)
        - priority_index: The index of the character's name in the priority list, or len(priority) if not found.
                          Characters in the priority list will have smaller priority_index values.
        - original_index: The original index of the character object in the `chars` list. This preserves the original order
                          for characters with the same priority.
        """
        charname = char.name
        if charname in priority_map:
            return (priority_map[charname], chars.index(char))
        else:
            return (len(priority), chars.index(char))  # Assign lowest priority and keep original order

    return sorted(chars, key=sort_key)

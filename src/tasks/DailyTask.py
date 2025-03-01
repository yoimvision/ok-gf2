import re
import time

from ok import Logger
from src.tasks.BaseLsTask import BaseGfTask

logger = Logger.get_logger(__name__)


class DailyTask(BaseGfTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "一键日常"
        self.description = "收菜"
        self.default_config.update({
            '吃料理': False,
            '刷鸡': True,
            '免费召唤': True,
            '收菜': True,
            '公会': True,
            '经验金币本': True,
            '单人突袭': True,
            '组队突袭': True,
            '巨石阵召唤一次': True,
            '免费礼包': True,
            '活动挂机5分钟': True,
            '聊天': True,
            '领邮件': True,
            '商店购物': True,
            '买料理': True,
            '买礼物': True,
            '活动领奖': True,
            '领任务': True,
            '竞技场': True,
        })

        self.config_description = {
            '领体力': "不满四个Buff则吃4个每样1个",
            '刷鸡': "村庄刷鸡肉, 要小技能可以打死鸡的角色, 如鲁亚, 蓝恩, 男主",
            '收菜': "快速探查和收菜",
            '公会': "公会奖励和投资",
            '经验金币本': "只刷日常的, 不会用票",
            '单人突袭': "打一次, 然后扫荡两次, 只刷日常的, 不会用票",
            '组队突袭': "只刷日常的, 不会用票",
            '巨石阵召唤一次': "做日常任务",
            '聊天': "好感度, 从上到下聊六次",
            '活动领奖': "兔女郎抽奖",
            '领任务': "领取日常,周常,史诗任务奖励",
            '竞技场': "只刷下防的近战, 直到票刷完",
        }

    def run(self):
        self.ensure_main(recheck_time=2, time_out=90)
        # self.gongongqu()
        # self.shopping()
        self.battle()
        # if self.config.get('刷鸡'):
        #     self.farm_chicken()
        # if self.config.get('经验金币本'):
        #     self.exp_and_gold()
        # if self.config.get('免费召唤'):
        #     self.free_summon()
        # if self.config.get('公会'):
        #     self.guild()
        # if self.config.get('收菜'):
        #     self.collect()
        # if self.config.get('吃料理'):
        #     self.eat()
        # if self.config.get('单人突袭'):
        #     self.farm_dragon()
        # if self.config.get('组队突袭'):
        #     self.farm_dragon_team()
        # if self.config.get('巨石阵召唤一次'):
        #     self.use_stone_henge()
        # if self.config.get('活动挂机5分钟'):
        #     self.farm_activity()
        # if self.config.get('聊天'):
        #     self.chat()
        # if self.config.get('领邮件'):
        #     self.claim_mail()
        # if self.config.get('商店购物'):
        #     self.shop()
        # if self.config.get('活动领奖'):
        #     self.claim_activity()
        # if self.config.get('领任务'):
        #     self.claim_quest()
        # if self.config.get('竞技场'):
        #     self.do_arena()
        #     self.ensure_main()
        # self.log_info('一键日常完成', notify=True, tray=True)

    def gongongqu(self):
        self.log_info('public area')
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
        self.log_info('shopping')
        self.wait_click_ocr(match=['商城'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['品质甄选'], box='left', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['常驻礼包'], box='right', after_sleep=0.5, raise_if_not_found=True)
        if self.wait_click_ocr(match=['免费'], box='left', after_sleep=0.5, raise_if_not_found=False, time_out=5):
            self.log_info('found free item to buy')
            self.wait_click_ocr(match=['确认'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
            self.wait_click_ocr(match=['点击空白处关闭'], box='bottom', after_sleep=0.5, raise_if_not_found=False)
        self.ensure_main()

    def battle(self):
        self.log_info('battle')
        self.wait_click_ocr(match=['战役推进'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['补给作战'], box='top', after_sleep=0.5, raise_if_not_found=True)
        self.swipe_relative(0.8, 0.6, 0.5, 0.6, duration=1)
        self.sleep(1)
        self.wait_click_ocr(match=['标准同调'], box='right', after_sleep=0.5, raise_if_not_found=True)
        self.wait_click_ocr(match=['自律'], box='bottom', after_sleep=0.5, raise_if_not_found=True)
        self.ensure_main()



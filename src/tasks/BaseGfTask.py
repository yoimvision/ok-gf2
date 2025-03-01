import re
import sys
import time

from ok import BaseTask
from ok import Logger

logger = Logger.get_logger(__name__)


class BaseGfTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # from ok import og
        # self.log_debug(f'{og.config.get("auth").get("app_id")}')
        # if og.config.get("auth").get("app_id") != 'ok-ls':
        #     sys.exit(1)

    def ensure_main(self, recheck_time=1, time_out=30, esc=True):
        if not self.wait_until(lambda: self.is_main(recheck_time=recheck_time, esc=esc), time_out=time_out):
            raise Exception("请从游戏主页进入")

    def is_main(self, recheck_time=0, esc=True):
        boxes = self.ocr(match=['整备室','公共区','招募'], box='right')
        if len(boxes) == 3:
            if recheck_time:
                self.sleep(recheck_time)
                return self.is_main(recheck_time=0, esc=False)
            else:
                return True
        # if not self.do_handle_alert()[0]:
        if box:=self.ocr(box="bottom", match=["点击开始", "点击空白处关闭"],
                           log=True):
            self.click(box)
            return False
        if esc:
            self.back()
            self.sleep(1)
            # self.do_handle_alert()
        self.next_frame()


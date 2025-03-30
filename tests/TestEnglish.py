# Test case
import unittest

from config import config
from ok.gui.common.config import Language
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.DailyTask import DailyTask


class TestBattleBaseSerialization(TaskTestCase):
    task_class = DailyTask
    lang = Language.ENGLISH
    config = config

    def test_paiqian(self):
        # Create a BattleReport object
        self.set_image('tests/images/english_date_regex.png')
        dates = self.task.find_activities()
        self.assertEqual(len(dates), 1)


if __name__ == '__main__':
    unittest.main()

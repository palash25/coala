import unittest
import os

from coala_utils.ContextManagers import make_temp
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ShowAppliedPatchesAction import \
    ShowAppliedPatchesAction
from coalib.settings.Section import Section
from coala_utils.ContextManagers import (
    make_temp, retrieve_stdout, simulate_console_inputs)
from coalib.io.FileFactory import FileFactory


class ShowAppliedPatchesActionTest(unittest.TestCase):

    def setUp(self):
        factory_test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'FileFactoryTestFiles'))
        self.testfile_path = os.path.join(factory_test_path, 'test.txt')

    def test_apply(self):
        uut = ShowAppliedPatchesAction()

        with make_temp() as f_a, make_temp() as f_b, make_temp() as f_c:

            file_dict = {
                f_a: ['1\n', '2\n', '3\n'],
                f_b: ['1\n', '2\n', '3\n'],
                f_c: ['1\n', '2\n', '3\n']
            }
            expected_file_dict = {
                f_a: ['1\n', '3_changed\n'],
                f_b: ['1\n', '2\n', '3_changed\n'],
                f_c: ['1\n', '2\n', '3\n']
            }

            file_diff_dict = {}
            file_dict = {self.testfile_path:
                         FileFactory(self.testfile_path)}
            diff = Diff(file_dict[self.testfile_path])
            diff.delete_line(2)
            diff.change_line(3, '3\n', '3_changed\n')
            result = Result('origin', 'msg', diffs={f_a: diff},
                            applied_actions={'ApplyPatchAction': [Result(
                            'origin', 'message',
                            diffs={self.testfile_path: diff}),
                            file_dict, file_diff_dict, Section('')]})

            self.assertTrue(uut.apply(result,
                                      file_dict,
                                      file_diff_dict))

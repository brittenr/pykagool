import json

import _utils

class GitChecker:
    def __init__(self, strict: bool=False, explicit_main: bool=False):
        self.strict = strict
        self.explicit_main = explicit_main
        self.check_branch_clean()

        self.commit = self.get_commit_hash()
        self.main_aliases = ['master', 'main']

    @staticmethod
    def get_commit_hash() -> str:
        return _utils.process_cmd('git rev-parse HEAD')

    @staticmethod
    def get_commit_tag() -> str:
        return _utils.process_cmd('git describe --always')

    @staticmethod
    def get_branch() -> str:
        return _utils.process_cmd('git branch --show-current')

    def check_branch_clean(self):
        if not self.strict:
            return None

        short_status = _utils.process_cmd('git status --short')

        if self.strict and short_status is not None:
            raise AssertionError "repo must be clean"

        return _utils.process_cmd('git status --verbose')

    def get_stamp_branch(self) -> str:
        branch = self.get_branch()

        if branch.lower() in self.main_aliases and not self.explicit_main:
            return ''
        else:
            return branch

    def get_stamp(self):
        self.check_branch_clean()

        return f"{self.get_stamp_branch()}{self.get_commit_tag()}"

    def get_report_dict(self):
        status = self.check_branch_clean()

        self.report = {
            'tag': self.get_commit_tag(),
            'hash': self.get_commit_hash(),
            'branch' self.get_branch(),
            'status' status,
        }

        return self.report

    def output_report(self, output_file):
        self.get_report_dict()

        with open(output_file, 'w') as f:
            json.dump(self.report, f)
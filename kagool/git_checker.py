import json
import _utils


class GitChecker:
    def __init__(self, strict: bool = False, explicit_main: bool = False):
        self.strict = strict
        self.explicit_main = explicit_main
        self.check_branch_clean()

        self.main_aliases = ["master", "main"]
        self.commit = self.get_commit_hash()
        self.report = self.get_report_dict()

    @staticmethod
    def get_commit_hash() -> str:
        """
        :return: full commit hash
        """
        return _utils.process_cmd("git rev-parse HEAD")

    @staticmethod
    def get_commit_tag() -> str:
        """
        :return: git tag if there is one or short commit hash
        """
        return _utils.process_cmd("git describe --always")

    @staticmethod
    def get_branch() -> str:
        """
        :return: current git branch
        """
        return _utils.process_cmd("git branch --show-current")

    def check_branch_clean(self) -> str:
        """
        check if git status returns any uncommitted file/changes in repo

        return: where there are changes: if strict then throw an error else return details on changes
        """
        if not self.strict:
            return None

        short_status = _utils.process_cmd("git status --short")

        if self.strict and short_status is not None:
            raise AssertionError("repo must be clean")

        return _utils.process_cmd("git status --verbose")

    def get_stamp_branch(self) -> str:
        """
        :return: branch name, exlcuding master or main if not explicit_main
        """
        branch = self.get_branch()

        if branch.lower() in self.main_aliases and not self.explicit_main:
            return ""
        else:
            return branch

    def get_stamp(self) -> str:
        """
        :return: stamp branch and tag
        """
        self.check_branch_clean()

        return f"{self.get_stamp_branch()}{self.get_commit_tag()}"

    def get_report_dict(self) -> str:
        """
        :return: dict of details on commit status
        """
        status = self.check_branch_clean()

        self.report = {
            "tag": self.get_commit_tag(),
            "hash": self.get_commit_hash(),
            "branch": self.get_branch(),
            "status": status,
        }

        return self.report

    def output_report(self, output_file) -> None:
        """
        output json represnetation of report dict

        :param output_file: file path to output file
        """
        self.get_report_dict()

        with open(output_file, "w") as f:
            json.dump(self.report, f)

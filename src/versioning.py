import subprocess


class GitControl:
    """
    https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script
    """

    def __init__(self, strict: bool=True, verbose: bool = False):
        self.verbose = verbose
        self.label = self.repo_current_label()
        self.full_hash = self.repo_current_hash()
        self.branch = self.repo_current_branch()
        self.stamp = self.label + self.branch
        self.print_description = self.description()

        if self.verbose:
            print(self)

    def __repr__(self):
        return "GitControl() " + self.stamp

    def __str__(self):
        return self.description()

    def description(self):
        return """Current Repo State:\n > Branch:\t{b}\n > Label:\t{l}\n > Hash:\t{h}""".format(
            b=self.branch, l=self.label, h=self.full_hash)

    @staticmethod
    def repo_current_label():
        try:
            label = subprocess.check_output(
                ['git', 'describe', '--always']).decode().strip()
        # Not copying .git folder into docker container
        except subprocess.CalledProcessError:
            label = "0000000"

        return label

    @staticmethod
    def repo_current_hash():
        try:
            hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD']).decode().strip()
        # Not copying .git folder into docker container
        except subprocess.CalledProcessError:
            hash = "0000000"

        return hash

    @staticmethod
    def repo_current_branch():
        try:
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
        # Not copying .git folder into docker container
        except subprocess.CalledProcessError:
            branch = "0000000"

        return branch

    # TODO
    # def assert_no_uncommitted
    # def write_json
    # def write_yaml

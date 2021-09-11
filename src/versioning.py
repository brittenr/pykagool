class gitControl():
    """
    https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script
    """

    def __init__(strict: bool=True, verbose: bool = False):
        self.label = self.repo_current_label()
        self.full_hash = self.repo_current_hash()
        self.branch = repo_current_branch()
        self.stamp = self.label + self.branch

    @staticmethod
    def repo_current_label():
        try:
            commit = subprocess.check_output(
                ['git', 'describe', '--always']).decode().strip()
        # Not copying .git folder into docker container
        except subprocess.CalledProcessError:
            commit = "0000000"

        if verbose:
            print(' > Git Hash: {}'.format(commit))

        return commit

    @staticmethod
    def repo_current_hash():
        try:
            commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD']).decode().strip()
        # Not copying .git folder into docker container
        except subprocess.CalledProcessError:
            commit = "0000000"

        if verbose:
            print(' > Git Hash: {}'.format(commit))

        return commit

    @staticmethod
    def repo_current_branch():
        try:
            commit = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
        # Not copying .git folder into docker container
        except subprocess.CalledProcessError:
            commit = "0000000"

    # TODO
    # def assert_no_uncommitted
    # def write_json
    # def write_yaml

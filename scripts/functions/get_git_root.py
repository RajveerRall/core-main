import git


def get_git_root(path: str) -> str:
    """
    Get the root directory of the Git repository that contains the specified path.

    :param path: A string representing the path to a file or directory within the Git repository.
    :type path: str
    :return: A string representing the root directory of the Git repository.
    :rtype: str
    :raises git.exc.InvalidGitRepositoryError: If the specified path is not within a Git repository.
    """
    git_repo = git.Repo(path.replace('\\', '/'), search_parent_directories=True)
    return git_repo.git.rev_parse('--show-toplevel')

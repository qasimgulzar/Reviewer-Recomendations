import logging
import os
from heapq import nlargest
from operator import itemgetter

import git
from github import Github

g = Github(os.getenv('GITHUB_USER_ACCESS_TOKEN', 'github-user-access-token'))

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

if __name__ == '__main__':
    l_repo = git.Repo('/Users/qasimgulzar/IdeaProjects/philu/edx-platform')
    repo = g.get_repo('philanthropy-u/edx-platform')

    commits = dict()
    excluded_emails = []
    for pull in repo.get_pulls():
        for file in pull.get_files():
            for commit, lines in l_repo.blame('HEAD', file.filename):
                log.debug('{author} has contributed {total_lines} lines in {filename}'.format(filename=file.filename,
                                                                                              author=commit.author,
                                                                                              total_lines=len(lines)))

                count = commits.get(commit.author.email, 0) + len(lines)
                commits[commit.author.email] = count

        log.debug('------------------------------------------')

    commits = commits.items()
    commits = filter(lambda x: 'arbisoft' in x[0] and x[0] not in excluded_emails, commits)
    commits = nlargest(5, commits, key=itemgetter(1))

    log.info(commits)

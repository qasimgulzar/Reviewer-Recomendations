import logging
from heapq import nlargest
from operator import itemgetter

from github import Github
import git

g = Github("git-hub-access-token")

log = logging

if __name__ == '__main__':
    l_repo = git.Repo('/Users/qasimgulzar/IdeaProjects/philu/edx-platform')
    repo = g.get_repo('philanthropy-u/edx-platform')

    commits = dict()
    excluded_emails = ['ahsan.haq@arbisoft.com', 'zia.fazal@arbisoft.com', 'waheed.ahmed@arbisoft.com']
    for pull in repo.get_pulls():
        for file in pull.get_files():
            for commit in l_repo.iter_commits(paths=file.filename):
                log.info('{filename} - {author}'.format(filename=file.filename, author=commit.author))

                count = commits.get(commit.author.email, 0) + 1
                commits[commit.author.email] = count

        log.info('------------------------------------------')

    commits = commits.items()
    commits = filter(lambda x: 'arbisoft' in x[0] and x[0] not in excluded_emails, commits)
    commits = nlargest(5, commits, key=itemgetter(1))

    log.info(commits)

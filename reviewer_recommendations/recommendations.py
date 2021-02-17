import logging
import os
from heapq import nlargest
from operator import itemgetter

import git
from github import Github

log = logging.getLogger(__name__)


class ReviewerRecommendation(object):
    def __init__(self, *args, **kwargs):
        self.github_auth_token = kwargs.get('github_user_access_token', None)
        self.workspace_dir = kwargs.get('workspace_dir', None)
        self.git_repo_name = kwargs.get('git_repo_name', None)

        self.github_client = Github(self.github_auth_token)

    def get_blames(self, repo_path, file):
        repo = git.Repo(repo_path)
        return repo.blame('HEAD', file.filename)

    def get_pulls(self, repo_name='philanthropy-u/edx-platform', *args, **kwargs):
        repo = self.github_client.get_repo(repo_name)
        return repo.get_pulls(**kwargs)

    def get_files(self, pull):
        return pull.get_files()

    def recommendations_by_contribution(self, pull, repo_path='~/IdeaProjects/philu/edx-platform'):
        contributions = dict()
        for file in self.get_files(pull):

            if not os.path.exists(os.path.join(repo_path, file.filename)):
                continue

            for commit, lines in self.get_blames(repo_path, file):
                count = contributions.get(commit.author.email, 0) + len(lines)
                contributions[commit.author.email] = count

                log.debug('{author} has contributed {total_lines} lines in {filename}'.format(filename=file.filename,
                                                                                              author=commit.author,
                                                                                              total_lines=len(lines)))
        return contributions.items()

    def filter_recomentations_by_email_must_contains(self, contributions, term='arbisoft'):
        contributions = filter(lambda x: term in x[0], contributions)
        return contributions

    def filter_recomentations_excluded_emails(self, contributions, excluded_emails=[]):
        contributions = filter(lambda x: x[0] not in excluded_emails, contributions)
        return contributions

    def get_top_n_recommentations(self, contributions, n=5):
        return nlargest(n, contributions, key=itemgetter(1))

    def get_recommendations(self, pull, term='arbisoft', excluded_emails=[], n=5,
                            repo_path='~/IdeaProjects/philu/edx-platform'):
        recommendations = self.recommendations_by_contribution(pull, repo_path)
        recommendations = self.filter_recomentations_by_email_must_contains(recommendations, term)
        recommendations = self.filter_recomentations_excluded_emails(recommendations, excluded_emails)
        recommendations = self.get_top_n_recommentations(recommendations, n)
        return recommendations

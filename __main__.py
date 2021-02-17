import logging
import os

from reviewer_recommendations.recommendations import ReviewerRecommendation

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

if __name__ == '__main__':

    recommend = ReviewerRecommendation(
        github_user_access_token=os.getenv('GITHUB_USER_ACCESS_TOKEN', 'github-user-access-token'),
    )

    for pull in recommend.get_pulls():

        recommendations = recommend.get_recommendations(pull, term='arbisoft', excluded_emails=[], n=5)

        log.debug('------------------------------------------')

        log.info(recommendations)

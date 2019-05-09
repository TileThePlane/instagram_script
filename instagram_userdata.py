'''
https://www.upwork.com/ab/proposals/1126192042930085889
Script to gather follower and following data of targeted instagramers.
Given dataspec:
		user_data['AccountName'] = raw_user_data['username']
		user_data['PostNumber'] = raw_user_data['edge_owner_to_timeline_media']['count']
		user_data['FollowersNumber'] = raw_user_data['edge_followed_by']['count']
		user_data['FollowingNumber'] = raw_user_data['edge_follow']['count']
		user_data['ProfileBiography'] = raw_user_data['biography']
		user_data['Verification'] = raw_user_data['is_verified']

Output json format
{
    account_name: {
        'AccountName': profile.username,
        'PostNumber': profile.mediacount,
        'FollowersNumber': profile.followers,
        'FollowingNUmber': profile.followees,
        'ProfileBiography': profile.biography,
        'Verification': profile.is_verified
        followers: [
            {
                'AccountName': profile.username,
                'PostNumber': profile.mediacount,
                'FollowersNumber': profile.followers,
                'FollowingNUmber': profile.followees,
                'ProfileBiography': profile.biography,
                'Verification': profile.is_verified
            }
        ]
        following: [
            {
                'AccountName': profile.username,
                'PostNumber': profile.mediacount,
                'FollowersNumber': profile.followers,
                'FollowingNUmber': profile.followees,
                'ProfileBiography': profile.biography,
                'Verification': profile.is_verified
            }
        ]
    }
}
'''
__author__ = 'Kyle Vonderwerth'
__email__ = 'kylesv@live.com'
__owner__ = 'Jennifer Wang'

import instaloader
from collections import defaultdict
from json import dump

ACCOUNT_NAMES = ['colesprouse', 'sabinasocol', 'realbarbarapalvin','jessalizzi','linguamarina','brendonburchard','millionaire_mentor']
INSTANCE_USER_NAME = ''
INSTANCE_PASSWORD = ''

def get_profile_data(profile):
    return {
        'AccountName': profile.username,
        'PostNumber': profile.mediacount,
        'FollowersNumber': profile.followers,
        'FollowingNUmber': profile.followees,
        'ProfileBiography': profile.biography,
        'Verification': profile.is_verified
    }

if __name__ == '__main__':
    # Get instance
    L = instaloader.Instaloader()
    user_data = defaultdict(dict)

    # Login or load session
    L.login(INSTANCE_USER_NAME, INSTANCE_PASSWORD)

    for account_name in ACCOUNT_NAMES:
        # Obtain profile metadata
        seed_profile = instaloader.Profile.from_username(L.context, account_name)
        user_data[seed_profile.username].update(get_profile_data(seed_profile))
        user_data[seed_profile.username].update({
            'followers': [],
            'following': []
        })

        for followee in seed_profile.get_followees():
            user_data[seed_profile.username]['following'].append(
                get_profile_data(instaloader.Profile.from_username(L.context, followee.username))
            )

        for follower in seed_profile.get_followers():
            user_data[seed_profile.username]['followers'].append(
                get_profile_data(instaloader.Profile.from_username(L.context, follower.username))
            )

        with open('data.json', 'w') as outfile:
            dump(user_data,outfile)

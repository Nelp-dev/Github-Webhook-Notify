import json
import urllib3
import webhooks


urllib3.disable_warnings()
USER_AGENT = {'user-agent': 'cjh5414'}
http = urllib3.PoolManager(headers=USER_AGENT)

MEMBERS = ['cjh5414', 'sim4858', 'NESOY']


def get_opened_PR_dict_list():
    PULLS_URL = 'https://api.github.com/repos/Nelp-dev/Nelp/pulls'
    response = http.request('GET', PULLS_URL)
    PR_info_list = json.loads(response.data.decode('utf-8'))

    opened_PR_dict_list = []
    for PR_info in PR_info_list:
        PR_dict = {}

        PR_dict['user'] = PR_info['user']['login']

        PR_url = PR_info['url']
        PR_dict['number'] = PR_url.split('/')[-1]

        opened_PR_dict_list.append(PR_dict)
    
    return opened_PR_dict_list


def get_members_who_did_not_approve(PR_owner, PR_number):
    REVIEWS_URL = 'https://api.github.com/repos/Nelp-dev/Nelp/pulls/' + PR_number + '/reviews'
    response = http.request('GET', REVIEWS_URL)
    review_info_list = json.loads(response.data.decode('utf-8'))

    members = MEMBERS[:]
    members.remove(PR_owner)
    for review_info in review_info_list:
        if review_info['state'] == 'APPROVED':
            approving_user = review_info['user']['login']
            if approving_user in members:
                members.remove(approving_user)
    
    return members


PR_URL = 'https://github.com/Nelp-dev/Nelp/pull/'

def get_message_to_request_merge(user, PR_number):
    return user + '님 머지하세요\n' + PR_URL + PR_number + '\n\n'

def get_message_to_request_approving(user, PR_number):
    return user + '님 리뷰하세요\n' + PR_URL + PR_number + '\n\n'


def notify_to_line(message):
    webhooks.notify_to_line('\n' + message)


def main():
    opened_PR_dict_list = get_opened_PR_dict_list()
    if len(opened_PR_dict_list) == 0:
        return
    else:
        notify_message = ''
        for PR_dict in opened_PR_dict_list:
            members = get_members_who_did_not_approve(PR_dict['user'], PR_dict['number'])
            if len(members) == 0:
                notify_message += get_message_to_request_merge(PR_dict['user'], PR_dict['number'])
            else:
                for member in members:
                    notify_message += get_message_to_request_approving(member, PR_dict['number'])
        
        notify_to_line(notify_message)
    

if __name__ == '__main__':
    main()

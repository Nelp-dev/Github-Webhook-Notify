from flask import Flask, request, jsonify
import urllib3

LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
LINE_HEADERS = {
    'Authorization' : 'Bearer ' + 'gakjPa74Fw2tlPavkCfeBaFmVPqiSWWjoUBlqKCiJoQ'
}

application = Flask(__name__)


def notify_to_line(message):
    try:
        http = urllib3.PoolManager()
        response = http.request(
            'POST',
            LINE_NOTIFY_URL,
            headers=LINE_HEADERS,
            fields={'message': message}
        )
        print('Response HTTP Status Code: {status_code}'.format(
        status_code=response.status))
    except urllib3.exceptions.NewConnectionError:
        print('Connection failed.')


def open_pull_request():
    json_dict = request.get_json()
    message = 'Open Pull Request ' + '#' + str(json_dict['number']) + '\n'
    message += (json_dict['pull_request']['user']['login'] + '\n')
    message += (json_dict['pull_request']['title'] + '\n')
    message += (json_dict['pull_request']['html_url'] + '\n')
    notify_to_line(message)


@application.route('/postreceive', methods=['POST'])
def hello_world():
    if request.headers['X-GitHub-Event'] == 'pull_request' and request.get_json()['action'] == 'opened':
        open_pull_request()
        return 'success'
    else:
        return 'hello'

if __name__ == "__main__":
    application.run(host='0.0.0.0')

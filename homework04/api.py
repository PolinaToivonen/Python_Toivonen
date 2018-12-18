import requests
import time
from config import VK_CONFIG


def get(url: str, params={}, timeout=1, max_retries=5, backoff_factor=0.3) -> dict:
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            req = requests.get(url, params=params, timeout=timeout)
            return req
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            value = backoff_factor * (2 ** i)
            time.sleep(value)


def get_friends(user_id: int, fields="") -> dict:
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': VK_CONFIG['domain'],
        'access_token': VK_CONFIG['access_token'],
        'user_id': user_id,
        'fields': fields,
        'v': VK_CONFIG['version']
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}".format(
        **query_params)
    response = get(query, query_params)
    json_file = response.json()
    fail = json_file.get('error')
    if fail:
        raise Exception(json_file['error']['error_msg'])
    return json_file['response']['items']


def messages_get_history(user_id: int, offset=0, count=200) -> list:
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    query_params = {
        'domain': VK_CONFIG['domain'],
        'access_token': VK_CONFIG['access_token'],
        'user_id': user_id,
        'offset': offset,
        'messages_count': min(count, 200),
        'v': VK_CONFIG['version']
    }

    messages = []
    while count > 0:
        query = "{domain}/messages.getHistory?" \
            "access_token={access_token}&user_id={user_id}&offset={offset}&count={messages_count}&v={v}"\
            .format(**query_params)
        response = get(query)
        if response:
            json_file = response.json()
            if json_file.get('error') is not None:
                print(json_file['error']['error_msg'])
            else:
                messages.extend(json_file['response']["items"])
        count -= min(count, 200)
        query_params['offset'] += 200
        query_params['messages_count'] = min(count, 200)
        time.sleep(0.4)
    return messages

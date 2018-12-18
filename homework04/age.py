import datetime
from statistics import median
from typing import Optional

from api import get_friends
from config import VK_CONFIG


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    dates = []
    ages = []
    data = get_friends(user_id, 'bdate')
    for i in data:
        if i.get('bdate'):
            dates.append(i['bdate'])
    y_dates = []
    for elem in dates:
        if len(elem) in range(8, 11):
            y_dates.append(elem)
    dates = y_dates

    for elem in dates:
        a = list(map(int, elem.split('.')))
        data = datetime.date(a[2], a[1], a[0])
        age = (datetime.date.today() - data) / 365.25
        ages.append(age.days)

    if len(ages) > 0:
        return median(ages)
    else:
        return None


if __name__ == '__main__':
    user_id = VK_CONFIG['user_id']
    print('Age:', age_predict(user_id))

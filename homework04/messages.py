from api import messages_get_history
from api import get_friends
from api_models import Message
from config import VK_CONFIG, PLOTLY_CONFIG

plotly.tools.set_credentials_file(
    username=PLOTLY_CONFIG['username'],
    api_key=PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[List[datetime.date], List[int]]:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    dates = []
    cnt = Counter()
    for message in messages:
        message['date'] = datetime.utcfromtimestamp(message['date']).strftime("%Y-%m-%d")
        dates.append(message['date'])
    for val in dates:
        cnt[val] += 1
    return list(cnt.keys()), list(cnt.values())


def plotly_messages_freq(dates: List[datetime.date], freq: List[int]) -> None:
    """ Построение графика с помощью Plot.ly
    :param dates:
    :param dates: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [go.Scatter(x=dates, y=freq)]
    py.plot(data)


if __name__ == '__main__':
    messages = messages_get_history(172030641, offset=0, count=200)
    x, y = count_dates_from_messages(messages)
    plotly_messages_freq(x, y)
    

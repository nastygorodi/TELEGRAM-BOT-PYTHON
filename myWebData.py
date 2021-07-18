import numpy
import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import pandas as pd


def make_myTasks(tasks):
    names = []
    urls = []
    tags = []
    ratings = []

    for task in tqdm(tasks):
        name = task['name']
        task_id = task['contestId']
        task_index = task['index']
        url = f'https://codeforces.com/problemset/problem/{task_id}/{task_index}'
        tag = task['tags']
        if 'rating' in task.keys():
            rating = task['rating']
            ratings.append(rating)
        else:
            ratings.append('')

        names.append(name)
        urls.append(url)
        tags.append(tag)

    myTasks = pd.DataFrame(
        {
            'name': names,
            'url': urls,
            'tags': tags,
            'rating': ratings,
        }
    )
    myTasks.drop_duplicates(subset=['url'], inplace=True)

    myTasks.to_csv('myTasks.csv', encoding='utf-8', index=False)
    myTasks = pd.read_csv('myTasks.csv')
    return myTasks


def choose_rating(myTasks, min_, max_):
    search_index = myTasks.apply(
        lambda row: min_ < row['rating'] < max_,
        axis=1,
    )
    if myTasks[search_index].shape[0] == 0:
        return numpy.eye(17)
    return myTasks[search_index].sample(1)


class SampleTask:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    @staticmethod
    def from_csv(csv_path: str):
        return SampleTask(pd.read_csv(csv_path))

    def __call__(self, tags='', min_rating=None, max_rating=None):
        CF_api = 'https://codeforces.com/api/'
        url_problems = f'{CF_api}problemset.problems'
        if (len(tags) > 0):
            url_problems = f'{CF_api}problemset.problems?tags={tags}'
        response = requests.get(url_problems, params={'lang': 'ru'})

        tasks = response.json()['result']['problems']
        myTasks = make_myTasks(tasks)
        if myTasks.shape[0] == 0:
            return numpy.eye(17)
        if min_rating is not None and max_rating is not None:
            return choose_rating(myTasks, min_rating, max_rating)

        return myTasks.sample(1)


def get_limit_time(soup):
    text_time_limit  = ''
    for text in soup.find_all('div', 'time-limit'):
        text_time_limit += text.text
        text_time_limit += '\n'
    index_time = 0
    for i in range(len(text_time_limit)):
        if text_time_limit[i].isdigit():
            index_time = i
            break
    text_time_limit = text_time_limit[ : index_time] + ': ' + text_time_limit[index_time : ]
    return text_time_limit


def get_limit_memory(soup):
    text_memory_limit  = ''
    for text in soup.find_all('div', 'memory-limit'):
        text_memory_limit += text.text
        text_memory_limit += '\n'
    index_memory = 0
    for i in range(len(text_memory_limit)):
        if text_memory_limit[i].isdigit():
            index_memory = i
            break
    text_memory_limit = text_memory_limit[ : index_memory] + ': ' + text_memory_limit[index_memory : ]
    return text_memory_limit


myReplace = {'$': '', '\le': ' ≤ ', '\ge': ' ≥ ', '\oplus': '⊕', '\otimes': '⊗', '\times': '×', '\cdot': '·',
             '\pm': '±', '\cap': '∩', '\cup': '∪', '\sum': 'Σ', '\prod': 'П', '\mathrm' : '', '\neq' : '≠',
             '\ne' : '≠', '\ldots' : '...', '\quad' : '  ', '\sqrt' : '√', '\dots' : '...', '\in' : '∈',
             '\notin' : '∉', '\{' : '{', '\}' : '}', '\,' : ''}


def GetTask(task):
    url = task.iloc[0]['url']
    response = requests.get(url, params = {'lang' : 'ru'})
    soup = BeautifulSoup(response.content, 'html.parser')

    text = ''
    text = text + soup.find_all('div', 'problem-statement')[0].find_all('div', 'title')[0].text + '\n\n'
    text = text + get_limit_time(soup) + '\n\n' + get_limit_memory(soup) + '\n\n'

    for line in soup.find_all('p'):
        line_text = line.text
        for key in myReplace:
            line_text = line_text.replace(key, myReplace[key])
        text += line_text
        text += '\n'

    return text

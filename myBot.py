import telebot
import requests
import keyboa
from keyboa import Keyboa
from tqdm.notebook import tqdm
import myWebData

with open('myToken.txt') as file:
    TOKEN = file.read()
myBot = telebot.TeleBot(TOKEN)

CF_api = 'https://codeforces.com/api/'
url_problems = f'{CF_api}problemset.problems'
response = requests.get(url_problems, params = {'lang' : 'ru'})
tasks = response.json()['result']['problems']


tasks_ids = [
    {"2-sat": "2-sat"}, {"бинарный поиск": "binary search"}, {"битмаски": "bitmasks"},
    {"перебор": "brute force"}, {"китайская теорема об остатках": "chinese remainder theorem"}, {"комбинаторика": "combinatorics"},
    {"конструктив": "constructive algorithms"}, {"структуры данных": "data structures"}, {"поиск в глубину и т.п.": "dfs ans similar"},
    {"разделяй и властвуй": "divide and conquer"}, {"динамика": "dp"}, {"снм": "dsu"},
    {"разбор выражений": "expression parsing"}, {"фурье": "fft"}, {"потоки": "flows"},
    {"игры": "games"}, {"геометрия": "geometry"}, {"паросочетания": "graph matchings"},
    {"графы": "graphs"}, {"жадные алгоритмы": "greedy"}, {"хэши": "hashing"},
    {"реализация": "implementation"}, {"интерактив": "interactive"}, {"математика": "math"},
    {"матрицы": "matrices"}, {"meet-in-the-middle": "meet-in-the-middle"}, {"теория чисел": "number theory"},
    {"теория вероятностей": "probabilities"}, {"расписания": "schedules"}, {"кратчайшие пути": "shortest paths"},
    {"сортировки": "sortings"}, {"строковые суфф. структуры": "string suffix structures"}, {"строки": "strings"},
    {"тернарный поиск": "ternary search"}, {"деревья": "trees"}, {"два указателя": "two pointers"},
    ]


@myBot.callback_query_handler(func=lambda call: True)
def callback_tag(call):
    global tags_
    tags_ = call.data

def sent_task(message):
    str = message.text
    min_ = int (str[0 : str.find('-')])
    max_ = int (str[str.find('-') + 1 : ])
    myTasks = myWebData.make_myTasks(tasks)
    myTasks.to_csv('myTasks.csv', encoding='utf-8', index=False)
    request = myWebData.SampleTask.from_csv('myTasks.csv')
    userTask = request(tags_, min_, max_)
    if userTask.shape[1] == 17:
        myBot.send_message(message.from_user.id, "Задачи с такими параметрами не существует, попробуй еще =)")
        return
    task = myWebData.GetTask(userTask)
    myBot.send_message(message.from_user.id, task)


@myBot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        myBot.send_message(message.from_user.id, "Для получения задачи нажми /get_task")
    elif message.text == "/get_task":
        kb_tasks = Keyboa(items=tasks_ids, items_in_row=3).keyboard
        myBot.send_message(message.from_user.id, reply_markup=kb_tasks, text="~ Выбери тему ~")
        myBot.send_message(message.from_user.id, "Напиши диапазон сложности задачи через тире \nНапример: 0-2000")
        myBot.register_next_step_handler(message, sent_task)
    else:
        myBot.send_message(message.from_user.id, "Привет =) \nнапиши /help")

myBot.polling(none_stop=True, interval=0)

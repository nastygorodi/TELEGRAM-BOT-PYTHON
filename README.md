# TELEGRAM-BOT-PYTHON

## Описание

Бот работает с API сайта https://codeforces.com . Пользователь может получать рандомную задачу с выбранными темой и уровнем сложности.

## Инструменты разработки

Язык программирования -- ```Python```

## Технологии и методы

```CodeForces API```

```pyTelegramBotAPI```

```BeautifulSoup```

## Реализация

Бот находится в режиме ожидания сообщения от пользователя.
При получении команды ```/get_task``` бот делает API-запрос к сайту для получения всех задач из архива. 

Далее присходит отбор задач из архива под параметры, заданные пользователем, из подходящих выбирается случайная.

Потом с помощью get-запроса бот получает html-страничку с нужной задачей. 

Затем, используя ```BeautifulSoup```, бот получает текст задачи, который и отправляется пользователю.

## Для запуска кода

Необходимо установить все пакеты из файла ```requirements.txt```

Положить токен телеграм-бота в файл ```myToken.txt```


## Использование бота

Найти бота по тегу ```@cf_tasks_bot```

Написать команду ```\help```


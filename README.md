# TelegramBot
Telegram bot ot for GoToCamp

## Бот и его возможности:  
Бот умеет взаимодействовать с учениками и преподавателями(администраторами).  

***Режим ученика***:  
> * ***Автоматически***:  
    1. Уведомление о наступающих событиях: “Сейчас обед”;  
    2. Уведомление о получении новой ачивки: “Вася Пупкин получил достижение: Неспящий”;  
    3. Расписание на день по утрам и его обновления в течение дня: список время - событие, место;
    4. Срочные сообщения: “Всем срочно на внеплановый второй обед!”;
> * ***По запросу***:  
    1. Список ачивок пользователя;  
    2. Полное расписание на день;  
    3. Информация о текущем событии - “что и где сейчас идет?”;  
    4. Номера телефонов вожатых и преподавателей;  
    5. Команда “Где живет?” - говорит, где живет участник;  
    
***Режим администратора***:  
> * ***Автоматически***:  
    1. Уведомление о наступающих событиях: “Сейчас обед”;  
    2. Уведомление о получении новой ачивки: “Вася Пупкин получил достижение: Неспящий”;  
    3. Расписание на день по утрам и его обновления в течение дня: список время - событие, место;
    4. Срочные сообщения: “Всем срочно на внеплановый второй обед!”;  
> * ***По запросу***:  
    1. Добавление расписания на день(Рекомендуется добавлять новое расписание вечером, когда все мероприятия закончатся);  
    2. Добавление ачивки;  
    3. Отправка срочного сообщения.***


## Инструкция по настройке и установке: 
Чтобы бот корректно работал, надо запустить файлы bot.py и scheduler.py. На сервере должны быть установлены следующие библиотеки для python: pytelegrambotapi, schedule.
Вы можете сделать это следующими операциями: python -m pip install schedule и python -m pip install pytelegrambotapi. Также нужно заполнить файл room_allocation.txt следующими данными: в каждой следующей строке необходимо ввести Фамилию(из Телеграма), Имя(из Телеграма), Alias(без @; если нет, то поставить -), корпус в котором живёт ученик и комната через пробел.  

***Пример***:  
Almaz Samatov samatov 1 101  
Dilshat Salikhov dil 1 301  

Также нужно заполнить файл info.txt данными о номерах телефонов вожатых и преподавателей.  
  
***Предпологаемый формат***: Имя Фамилия, Номер. Жёсткого формата в этом случае нет. Заполняйте как хотите.  

***Изначальный пароль администратора***: qwerty  

Чтобы бот работал без падений, рекомендуется перенести его на вебхуки. Инструкция о том, как это сделать, можно найти тут: https://groosha.gitbooks.io/telegram-bot-lessons/content/chapter4.html

## Использование:  

***Режим администратора***: запрос "добавить расписание на день"  
***Формат***: [ЧЧ:ММ(начало) ЧЧ:ММ(конец) событие, место]. Должно быть столько же пробелов и запятая. Без знаков [].  

***Режим администратора***: запрос "добавить ачивку"  
***Формат***: [Имя Фамилия Ачивка]. Должно быть столько же пробелов. Без знаков [].   

***Режим администратора***: запрос "добавить расписание на день"  
***Формат***: [ЧЧ:ММ(начало) ЧЧ:ММ(конец) событие, место]. Должно быть столько же пробелов и запятая. Без знаков [].  

**Вся остальная функциональность предельно ясна и интеллектуально понятна.**

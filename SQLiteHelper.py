import sqlite3
import config


class SQLightHelperForUsers:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS users
            (USER_ID      INT          NOT NULL,
            CHAT_ID       INT          NOT NULL,
            USER_NAME     TEXT         NOT NULL,
            USER_SURNAME  TEXT         NOT NULL,
            ADMIN_OR_NOT  BOOLEAN      NOT NULL);''')
        self.cursor = self.connection.cursor()

    def select_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()

    def add_new_user(self, id_of_user, chat_id, user_name, user_surname, admin_or_not):
        with self.connection:
            if self.status_of_user(id_of_user) == 'No user found':
                params = (id_of_user, chat_id, user_name, user_surname, admin_or_not)
                self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", params)
                self.connection.commit()

    def update_user_info(self, id_of_user, admin_or_not):
        with self.connection:
            params = (id_of_user, admin_or_not)
            self.cursor.execute("UPDATE users SET ADMIN_OR_NOT = ? WHERE USER_ID=?", params)
            self.connection.commit()

    def chat_id(self, user_name, user_surname):
        with self.connection:
            params = (user_name, user_surname)
            state = self.cursor.execute('SELECT chat_id FROM users WHERE user_name = ? '
                                        'AND user_surname = ?', params).fetchone()
            if state is not None:
                return state[0]
            else:
                return 'Error'

    def user_names(self, user_id):
        with self.connection:
            params = (user_id,)
            return self.cursor.execute('SELECT user_name, user_surname FROM users WHERE user_id = ?',
                                       params).fetchone()

    def status_of_user(self, id_of_user):
        with self.connection:
            params = (id_of_user,)
            state = self.cursor.execute('SELECT admin_or_not FROM users WHERE user_id = ?', params).fetchone()
            if state is None:
                return 'No user found'
            elif state[0] == 1:
                return 'User is admin'
            else:
                return 'User is learner'

    def close(self):
        self.connection.close()


class SQLightHelperForAchievements:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS achievements
            (ID INT PRIMARY KEY     NOT NULL,
            USER_NAME     TEXT      NOT NULL,
            USER_SURNAME  TEXT     NOT NULL,
            ACHIEVEMENT   TEXT     NOT NULL);''')
        self.cursor = self.connection.cursor()

    def add_new_achievement(self, user_name, user_surname, achievement):
        with self.connection:
            params = (self.number_of_id() + 1, user_name, user_surname, achievement)
            self.cursor.execute("INSERT INTO achievements VALUES (?, ?, ?, ?)", params)
            self.connection.commit()

    def id_of_chat(self, user_name, user_surname):
        db_helper = SQLightHelperForUsers(config.db_name)
        return db_helper.chat_id(user_name, user_surname)

    def achievements(self, user_name, user_surname):
        with self.connection:
            params = (user_name, user_surname)
            return self.cursor.execute('SELECT achievement FROM achievements WHERE user_name = ? AND user_surname = ?',
                                params).fetchall()

    def number_of_id(self):
        with self.connection:
            all = self.cursor.execute('SELECT * FROM achievements').fetchall()
            return len(all)

    def close(self):
        self.connection.close()


class SQLightHelperForSchedule:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS schedule
            (START_TIME    INT      NOT NULL,
            END_TIME       INT      NOT NULL,
            EVENT          TEXT     NOT NULL,
            PLACE          TEXT     NOT NULL );''')
        self.cursor = self.connection.cursor()

    def add_new_row(self, start_time, end_time, event, place):
        with self.connection:
            params = (start_time, end_time, event, place)
            self.cursor.execute("INSERT INTO schedule VALUES (?, ?, ?, ?)", params)
            self.connection.commit()

    def delete_schedule(self):
        with self.connection:
            self.cursor.execute('DELETE from SCHEDULE')
            self.connection.commit()

    def get_schedule(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM schedule").fetchall()

    def current_event(self, current_time):
        with self.connection:
            params = (current_time, current_time)
            event = self.cursor.execute('SELECT event, place FROM schedule WHERE START_TIME <= ? AND END_TIME >= ?',
                                        params).fetchone()
            return event


    def next_event(self, current_time):
        with self.connection:
            params = (current_time,)
            event = self.cursor.execute('SELECT start_time, event, place FROM schedule WHERE START_TIME > ?',
                                        params).fetchone()
            return event


    def close(self):
        self.connection.close()


class SQLightHelperForQuestions:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS questions
            (ID INT PRIMARY KEY     NOT NULL,
            LOGIN          TEXT     NOT NULL,
            QUESTION       TEXT     NOT NULL,
            ANSWER_1       TEXT     NOT NULL,
            ANSWER_2       TEXT     NOT NULL,
            ANSWER_3       TEXT     NOT NULL,
            RIGHT_ANSWER       TEXT     NOT NULL);''')
        self.cursor = self.connection.cursor()


    def add_new_row(self, login, question, answer_1, answer_2, answer_3, right_answer):
        with self.connection:
            params = (self.number_of_id() + 1, login, question, answer_1, answer_2, answer_3, right_answer)
            self.cursor.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?, ?)", params)
            self.connection.commit()

    def get_one_question(self, login):
        with self.connection:
            params = (login,)
            question = self.cursor.execute("SELECT * FROM questions WHERE login = ?", params).fetchall()
            return question

    def delete_row(self, login, question):
        with self.connection:
            self.cursor.execute('DELETE from questions WHERE login = ? and question = ?', (login, question))
            self.connection.commit()

    def delete_all(self, login):
        with self.connection:
            self.cursor.execute('DELETE from questions WHERE login = ?', (login,))
            self.connection.commit()

    def number_of_id(self):
        with self.connection:
            all = self.cursor.execute('SELECT * FROM questions').fetchall()
            return len(all)

    def close(self):
        self.connection.close()

























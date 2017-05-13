

import sqlite3
import requests
import operator

d = ['fef']
class Engine:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.database = self.conn.cursor()
        self.skills_db = {x.lower(): 0 for x in self.get_item('skills')}

        blacklist_file = open('blacklist.txt')
        self.blacklist = [s.rstrip() for s in blacklist_file.readlines()]
        blacklist_file.close()

        self.skills = []

    def __del__(self):
        self.database.close()

    def get_item(self, column, param=None, value=None):
        if param and value:
            action = 'SELECT {0} FROM data WHERE {1}="{2}"'.format(column, param, value)
            self.database.execute(action)
            result = self.database.fetchall()
            return [i[0] for i in result]

        action = 'SELECT {0} FROM data'.format(column)
        self.database.execute(action)
        result = self.database.fetchall()
        return [x[0] for x in result]

    def parser(self, text, per_page=50):
        main_domain = 'http://api.hh.ru/'
        search_output = requests.get(main_domain + 'vacancies/', params={'text': text, 'per_page': per_page}).json()
        found = 0

        for item in search_output['items']:
            if not item['id'] in self.blacklist:
                vacancy = requests.get(main_domain + 'vacancies/' + item['id']).json()
                key_skills = vacancy['key_skills']
                if key_skills:
                    found += 1
                    self.skills += [x['name'].lower() for x in key_skills]

                else:
                    self.blacklist.append(item['id'])

        blacklist_file = open('blacklist.txt', 'a')
        blacklist_file.write('\n'.join(self.blacklist))
        blacklist_file.close()

        new_skills_file = open('new_skills.log')
        new_skills = [s.rstrip().lower() for s in new_skills_file.readlines()]
        new_skills_file.close()

        new_skills_file = open('new_skills.log', 'a')
        for i in self.skills:
            known = False
            for j in self.skills_db:
                if i in j.split(', '):
                    self.skills_db[j] += 1 / found
                    known = True

            if not known and i not in new_skills:
                new_skills_file.write(i + '\n')

        new_skills_file.close()

        skills = []
        percents = []
        for item in self.skills_db:
            if self.skills_db[item] > 0.3:
                skills.append(self.get_item('name', param='skills', value=item)[0])
                percents.append(round(self.skills_db[item], 2))

        return sorted(dict(zip(skills, percents)).items(), key=operator.itemgetter(1), reverse=True)


if __name__ == '__main__':
    parser = Parser()
    print(parser.main(input()))

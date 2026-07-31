from src.load_data_into_database import load_account_info

#get some user names
user_names: list[str] = []
with open('database/mal_usernames.txt') as file:
    while(True):
        line: str = file.readline()
        if line == '': break
        user_names.append(line[:-1])

#load to database
for user_name in user_names:
    load_account_info(user_name)
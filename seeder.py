import requests
import json
import random
import os

# Using this dataset https://www.kaggle.com/sayangoswami/reddit-memes-dataset/downloads/reddit-memes-dataset.zip/3

class User:
  def __init__(self, email, password, url, folder_path):
    self.url = url
    self.path_login = 'login'
    self.path_create_memes = 'user/memes'
    self.folder_path = folder_path
    self.user_info = {
      'user[email]': email, 
      'user[password]': password 
    }
    self.filenames = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))] 

  def login(self):
    response = requests.post(self.url + self.path_login, params = self.user_info)
    if response.status_code == 201:
      print("> User: "+ response.json()['handle'] + " has loged in")
      self.token = response.headers['Authorization']
      return True
    else:
      print("> Couldn't log in")
    return False

  def upload_meme(self, meme_path):
    file = {
      'meme[image]': open(meme_path, 'rb')
    }
    response = requests.post(
      self.url + self.path_create_memes, 
      files = file,
      headers = {'Authorization': self.token}
    )

    if response.status_code == 201:
      print("Meme seeded: " + meme_path)
    else:
      print("Couldn't seed meme: " + meme_path)

  def upload_random_memes(self, amount = 10):
    if self.token == None:
      print("Please log in first")
      return
    random_picks = random.sample(self.filenames ,amount)
    i = 0
    for meme in random_picks:
      print('> \t[' + str(i) + ']', end =" ");i+=1;
      self.upload_meme(self.folder_path + '/' + meme)


## Setup........    
url = 'http://localhost:3000/'
meme_folder = 'reddit-memes-dataset/memes'
users_info = [{'email': 'edwmapa@gmail.com', 'password': '123456'}]

for one_user in users_info:
  user = User(one_user['email'], one_user['password'], url, meme_folder)
  if user.login():
    user.upload_random_memes(5)




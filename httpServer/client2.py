import requests


Test = requests.get('http://localhost:8000/player2.txt')
print('Reply status code %s \nfilesContents:\n%s\n' % (Test.status_code, Test.text))

# Test3 = requests.get('http://localhost:8000/ans?Rock')
# print('Status code %s \nFilesContents:\n%s\n' % (Test3.status_code, Test3.text))

# print("Rock, paper, or scissors")
# Tput = input("Enter in your choice: ")

# Test2 = requests.get('http://localhost:8000/ans?' + Tput)
# print('Status code %s \nFilesContents:\n%s\n' % (Test2.status_code, Test2.text))
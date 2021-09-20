import request 

Test = request.get('http://localhost:8000/test.txt')
print('Reply status code %s \nfilesContents:\n%s\n' % (Test.status_code, Test.text))

print("Rock, paper, or scissors")
Tput = input("Enter in your choice")

Test2 = request.get('http://localhost:8000/ans.txt?' + Tput)
print('Status code %s \nFilesContents:\n%s\n' % (Test2.status_code, Test2.text))

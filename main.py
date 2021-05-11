from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import sys

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# sys.argv[1] is the title the google doc you are looking for
for file_list in drive.ListFile({'q': "title contains '%s'" % str(sys.argv[1])}):
  print('Received %s files from Files.list()' % len(file_list))
  for eachFile in file_list:
    print('title: %s, id: %s' % (eachFile['title'], eachFile['id']))
    file = drive.CreateFile({'id': eachFile['id']})
    file.GetContentFile('test.txt')
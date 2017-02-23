import os
import sys
import re
import getopt
import urllib
import json
import requests
import pprint

def print_usage():
  print(f'Usage: {sys.argv[0]} <url> [-u user] [-p pass] -f <inputfile> --numdelimiter=")"')

if (len(sys.argv) < 4):
  print_usage()
  sys.exit(2)

url = sys.argv[1]

try:
  opts, args = getopt.getopt(sys.argv[2:], 'hu:p:f:', ['help=', 'user=', 'password=', 'file=', 'numdelimiter='])
except getopt.GetoptError:
  print_usage()
  sys.exit(2)

user = None
password = None
auth = []

for opt, arg in opts:
  pass
  if opt == '-h':
    print_usage()
    sys.exit()
  elif opt in ('-f', '--file'):
    filepath = arg.strip()
  elif opt in ('-u', '--user'):
    user = arg
    auth.append(user)
  elif opt in ('-p', '--password'):
    password = arg
    auth.append(password)
  elif opt == '--numdelimiter':
    numdelimiter = arg
if (len(auth) < 2):
  auth = None
else:
  auth = (user, password)

inputfile = open(filepath, 'r', encoding='UTF-8')
line_index = 0
question = None
answer = None
prev_line = None
answers = []
for line in inputfile:
  if (line_index == 0):
    origin = line.strip().replace(u'\ufeff', '')
    line_index += 1
    # print(repr(origin))
    continue
  line_content = line.strip()
  if (question == None) and (line_content != ''):
    question = line_content
    question_count = int(re.search(f'^(\d+){numdelimiter}', line_content).group(1))
    # print(repr(question))
  elif line_content != '':
    match = re.search(f'^(\d+){numdelimiter}', line_content)
    if match:
      # print(answer)
      question = line_content
      question_count = int(match.group(1))
      answers.append({
        'value': answer,
        'origin': origin,
        'source': os.path.basename(inputfile.name)
      })
      answer = None
      # print(repr(question))
    elif (answer == None):
      if (prev_line == '\n') and (line != '\n'):
        answer = f'\n{line_content} '
      else:
        answer = line
    else:
      if (prev_line == '\n') and (line != '\n'):
        answer += f'\n{line_content} '
      else:
        answer += line
  line_index += 1
  prev_line = line

pp = pprint.PrettyPrinter(indent=2, )
pp.pprint(answers)

# count = 0 

# response = requests.post(url, auth=auth, data=data)
# if (response.status_code == 201):
#   count += 1

# print(f'Created {count} entries')

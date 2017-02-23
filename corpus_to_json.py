import os, sys, re, getopt, json, pprint, string

def print_usage():
  print(f'Usage: {sys.argv[0]} -i <inputfile> [-o <outputfile>] --numdelimiter=<delimiter>')

if (len(sys.argv) < 2):
  print_usage()
  sys.exit(2)

try:
  opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['help=', 'input=', 'output=', 'numdelimiter='])
except getopt.GetoptError:
  print_usage()
  sys.exit(2)

output_filepath = ''
numdelimiter = ''
user = None
password = None
auth = []

for opt, arg in opts:
  pass
  if opt == '-h':
    print_usage()
    sys.exit()
  elif opt in ('-i', '--input'):
    input_filepath = arg.strip()
  elif opt in ('-o', '--output'):
    output_filepath = arg.strip()
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

if input_filepath == None:
  print('Input file is required')

inputfile = open(input_filepath, 'r', encoding='utf-8-sig')
line_index = 0
question = None
answer = None
prev_line = None
answers = []
printable = set(string.printable)
for line in inputfile:
  line_content = line.strip()
  if (line_index == 0):
    origin = line_content
    line_index += 1
    continue
  if (question == None) and (line_content != ''):
    question = line_content
    match = re.search(f'^(\d+){numdelimiter}', line_content)
    if match:
      question_count = int(match.group(1))
    else:
      print(f'Unable to parse question \'{question}\' with number delimiter \'{numdelimiter}\'')
      sys.exit(2)
  elif line_content != '':
    match = re.search(f'^(\d+){numdelimiter}', line_content)
    if match:
      number = int(match.group(1))
      if number > question_count:
        question_count = number
        question = line_content
        answers.append({
          'value': answer.strip(),
          'origin': origin,
          'source': os.path.basename(inputfile.name)
        })
        answer = None
        continue
    if (answer == None):
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

if output_filepath:
  with open(output_filepath, 'w') as outputfile:
    json.dump(answers, outputfile, indent=2)
else:
  pprint.pprint(answers)

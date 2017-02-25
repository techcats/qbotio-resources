import os, sys, re, getopt, json, pprint, string

def print_usage():
  print(f'Usage: {sys.argv[0]} -i <inputfile> [-o <outputfile>] [--questions-only] [--multi-line-question] --numdelimiter=<delimiter> [debug]')

if (len(sys.argv) < 2):
  print_usage()
  sys.exit(2)

try:
  opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['help=', 'input=', 'output=', 'questions-only', 'multi-line-question', 'numdelimiter=', 'debug'])
except getopt.GetoptError:
  print_usage()
  sys.exit(2)

output_filepath = ''
numdelimiter = ''
user = None
password = None
auth = []
debug = False
questions_only = False
multi_line_question = False

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
  elif opt == '--questions-only':
    questions_only = True
  elif opt == '--multi-line-question':
    multi_line_question = True
  elif opt == '--numdelimiter':
    numdelimiter = arg
  elif opt == '--debug':
    debug = True
if (len(auth) < 2):
  auth = None
else:
  auth = (user, password)

if input_filepath == None:
  print('Input file is required')

inputfile = open(input_filepath, 'r', encoding='utf-8-sig')
filename = os.path.basename(inputfile.name)
line_index = 0
question = None
answer = None
prev_line = ''
questions = []
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
  else:
    match = re.search(f'^(\d+){numdelimiter}', line_content)
    if match:
      number = int(match.group(1))
      if number > question_count:
        if debug: print(repr(f'{question}'))
        answer = answer.strip()
        questions.append({
          'value': question,
          'origin': origin,
          'source': filename
        })
        answers.append({
          'value': answer,
          'origin': origin,
          'source': filename
        })
        if debug and not questions_only: print(repr(f'{answer}'))
        question_count = number
        question = line_content
        answer = None
        continue
    if multi_line_question and (prev_line.strip() != '') and prev_line.endswith('\n') and (prev_line.strip() in question):
      question += f' {line_content}'
    elif (answer == None):
        answer = line
    else:
        answer += line
  line_index += 1
  prev_line = line

answer = answer.strip()
questions.append({
  'value': question,
  'origin': origin,
  'source': filename
})
answers.append({
  'value': answer,
  'origin': origin,
  'source': filename
})

if debug: print(repr(f'{question}'))
if debug and not questions_only: print(repr(f'{answer}'))

if output_filepath:
  with open(output_filepath, 'w') as outputfile:
    if questions_only:
      json.dump(questions, outputfile, indent=2)
    else:
      json.dump(answers, outputfile, indent=2)
else:
  if questions_only:
    pprint.pprint(questions)
  else:
    pprint.pprint(answers)

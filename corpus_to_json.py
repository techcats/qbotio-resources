import os, sys, re, getopt, json, pprint

debug = False
questions_only = False
questions_and_answers = False
origin = ''
filename = ''
output_filepath = ''
numdelimiter = ''
user = None
password = None
auth = []
multi_line_question = False
collection = []

def print_usage():
  print(f'Usage: {sys.argv[0]} -i <inputfile> [-o <outputfile>] [--questions-only] [--questions_and_answers] [--multi-line-question] --numdelimiter=<delimiter> [debug]')

def print_debug(question, answer):
  if questions_and_answers:
    print(repr(f'{question}'))
    print(repr(f'{answer}'))
  elif questions_only: 
    print(repr(f'{question}'))
  else: 
    print(repr(f'{answer}'))

def collect(question, answer):
  if (questions_and_answers):
    collection.append({
      'question': question,
      'answer': answer,
      'origin': origin,
      'source': filename
    })
  else:
    collection.append({
      'value': question if questions_only else answer,
      'origin': origin,
      'source': filename
    })

if (len(sys.argv) < 2):
  print_usage()
  sys.exit(2)

try:
  opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['help=', 'input=', 'output=', 'questions-only', 'questions-and-answers', 'multi-line-question', 'numdelimiter=', 'debug'])
except getopt.GetoptError:
  print_usage()
  sys.exit(2)

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
  elif opt == '--questions-and-answers':
    questions_and_answers = True
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
regexp = re.compile(f'^(\d+){numdelimiter}')

for line in inputfile:
  line_content = line.strip()
  if (line_index == 0):
    origin = line_content
    line_index += 1
    continue
  if (question == None) and (line_content != ''):
    match = regexp.match(line_content)
    if match:
      question = regexp.sub('', line_content).strip()
      question_count = int(match.group(1))
    else:
      print(f'Unable to parse question \'{line_content}\' with number delimiter \'{numdelimiter}\'')
      sys.exit(2)
  else:
    match = regexp.match(line_content)
    if match:
      number = int(match.group(1))
      if number > question_count:
        answer = answer.strip()
        collect(question, answer)
        if debug: print_debug(question, answer)
        question_count = number
        question = regexp.sub('', line_content).strip()
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
collect(question, answer)

if debug: print_debug(question, answer)

if output_filepath:
  with open(output_filepath, 'w') as outputfile:
      json.dump(collection, outputfile, indent=2)
else:
    pprint.pprint(collection)

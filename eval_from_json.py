import argparse, ijson, os, re
from urllib import request, parse

parser = argparse.ArgumentParser(description='Reads a JSON list of questions/answers and evaluates the performance of Q Bot IO')
parser.add_argument('url', metavar='<URL>', type=str, help='Q Bot IO search endpoint')
parser.add_argument('-i', '-I', '--input', metavar='<File>', type=str, help='a JSON file containing questions and answers', required=True)
parser.add_argument('-o', '-O', '--output', metavar='<File>', type=str, help='File for reporting evaluation results', required=True)
parser.add_argument('-v', '--verbose', action='store_true', help='Output accuracy for each question result')
parser.add_argument('--passthrough', action='store_true', help='Omit NLTK preprocessing')
parser.add_argument('--ranks', type=int, help='Number of ranks', required=True)
args = parser.parse_args()
PATH = os.path.dirname(os.path.abspath(__file__))

inputfile = open(os.path.join(PATH,args.input), 'r', encoding='utf-8')
outputfile = open(os.path.join(PATH,args.output), 'w', encoding='utf-8')

indent = '{:2}'.format('')
indent2x = indent + indent
indent4x = indent2x + indent2x

outputfile.write('{\n')
if (args.verbose):
  outputfile.write(f'{indent}"evaluations": [\n')
TRAINING_DATA = ijson.items(inputfile, 'item')
train_count = 0
total_rankings = 0
total_accuracy = 0
misses = 0
error = 0
ESCAPE_QUOTE = re.compile(r'(")')
for i, data in enumerate(TRAINING_DATA):
  if args.verbose and (i > 0):
    outputfile.write(',\n')
  question = data['question']
  params = {'q': question}
  connection = request.urlopen(f'{args.url}?' + parse.urlencode(params) + ('&passthrough' if args.passthrough else ''))
  items = ijson.items(connection, 'item')
  rank = 0
  rank_count = 0
  rank_error = 0
  accuracy = 0
  answer_index = -1
  for j, item in enumerate(items):
    if rank == 0:
      if isinstance(data['answer'], list):
        try:
          answer_index = data['answer'].index(item['value'])
          if answer_index > -1:
            rank = j + 1
        except:
          pass
      elif item['value'] == data['answer']:
        rank = j + 1
    rank_count += 1
    if (j + 1 == args.ranks):
      break
  total_rankings += rank_count
  if rank == 0: 
    misses += 1
    rank_error = args.ranks
  else:
    accuracy = (rank_count - (rank - 1)) / rank_count
    rank_error = rank - 1
  total_accuracy += accuracy
  error += rank_error
  connection.close()
  metadata = []
  if args.verbose:
    if 'origin' in data:
      origin = data['origin']
      if answer_index > -1:
        origin = origin[answer_index]
      metadata.append('%s"origin": "%s"' % (indent4x, origin))
    if 'source' in data:
      source = data['source']
      if answer_index > -1:
        source = source[answer_index]
      metadata.append('%s"source": "%s"' % (indent4x, source))
    metadata = ',\n'.join(metadata)
    outputfile.writelines([
      f'{indent2x}{{\n',
      f'{indent4x}"question": "%s",\n' % ESCAPE_QUOTE.sub(r'\\\1', question),
      f'{indent4x}"rank": {rank},\n',
      f'{indent4x}"rank_count": {rank_count},\n',
      f'{indent4x}"rank_error": {rank_error},\n',
      f'{indent4x}"accuracy": {accuracy},\n',
      f'{metadata}\n',
      f'{indent2x}}}'
    ])
  train_count += 1
  outputfile.flush()
hit_accuracy = (train_count - misses) / train_count
rank_accuracy = total_accuracy / train_count
if args.verbose:
  outputfile.write('\n  ],\n')
error /= train_count
outputfile.writelines([
  f'{indent}"overall": {{\n',
  f'{indent2x}"train_count": {train_count},\n',
  f'{indent2x}"total_rankings": {total_rankings},\n',
  f'{indent2x}"misses": {misses},\n',
  f'{indent2x}"mean_average_error": {error},\n',
  f'{indent2x}"hit_accuracy": {hit_accuracy},\n',
  f'{indent2x}"rank_accuracy": {rank_accuracy}\n',
  f'{indent}}}\n'
])

inputfile.close()
outputfile.write('}')
outputfile.close()

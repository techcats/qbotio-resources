import argparse, ijson, os, re

parser = argparse.ArgumentParser(description='Compare between two evaluations')
parser.add_argument('file1', type=str, help='Evaluation 1')
parser.add_argument('file2', type=str, help='Evaluation 2')
parser.add_argument('--select', type=int, help='Select evaluation [1] or [2] to check performance', choices=[1, 2], required=True)
parser.add_argument('--filter-positive', action='store_true', help='Output only negative or neutral performances')
parser.add_argument('-o', '-O', '--output', metavar ='<File>', type=str, required=True, help='File for reporting comparisons')
parser.add_argument('-v', '--verbose', action='store_true', help='Output comparison for each question result')

args = parser.parse_args()

PATH = os.path.dirname(os.path.abspath(__file__))
file1 = open(os.path.join(PATH, args.file1), 'r', encoding='utf-8')
file2 = open(os.path.join(PATH, args.file2), 'r', encoding='utf-8')
outputfile = open(os.path.join(PATH, args.output), 'w', encoding='utf-8')
EVALUATIONS1 = ijson.items(file1, 'evaluations.item')
EVALUATIONS2 = ijson.items(file2, 'evaluations.item')

indent = '{:2}'.format('')
indent2x = indent + indent
indent4x = indent2x + indent2x

outputfile.write('{\n')
count = 0
try:
  if (args.verbose):
    outputfile.write(f'{indent}"comparisons": [\n')
  ESCAPE_QUOTE = re.compile(r'(")')
  while True:
    try:
      evaluation1 = next(EVALUATIONS1)
    except StopIteration:
      raise
    except:
      print(f'Please verify valid evaluations from {args.file1}')
      raise
    try:
      evaluation2 = next(EVALUATIONS2)
    except StopIteration:
      raise
    except:
      print(f'Please verify valid evaluations from {args.file2}')
      raise
    is_positive = False
    rank1 = 0
    rank2 = 0
    if args.select == 1: 
      rank1 = evaluation1['rank']
      rank2 = evaluation2['rank']
    elif args.select == 2:
      rank1 = evaluation2['rank']
      rank2 = evaluation1['rank']
    if (rank1 == 1) or (rank1 < rank2):
      is_positive = True
    if args.verbose and not (args.filter_positive and is_positive):
      if count > 0: outputfile.write(',\n')
      outputfile.writelines([
        f'{indent2x}{{\n',
        f'{indent4x}"question": "%s",\n' % ESCAPE_QUOTE.sub(r'\\\1', evaluation1['question']),
        f'{indent4x}"eval1_rank": %s,\n' % evaluation1['rank'],
        f'{indent4x}"eval2_rank": %s\n' % evaluation2['rank'],
        f'{indent2x}}}'
      ])
      count += 1
except StopIteration:
  if args.verbose:
    outputfile.write('\n  ],\n')

outputfile.writelines([
  f'{indent}"result": {{\n',
  f'{indent2x}"count": {count}\n',
  f'{indent}}}\n'
])

file1.close()
file2.close()
outputfile.write('}')
outputfile.close()
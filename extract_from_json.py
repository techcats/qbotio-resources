import argparse, ijson, os

parser = argparse.ArgumentParser(description='Create a seperate question or answer JSON')
parser.add_argument('input', type=str, help='Input JSON file')
parser.add_argument('output', type=str, help='Output JSON file')
parser.add_argument('--select', type=int, help='Select [1] or [2] for question or answer respectively', choices=[1, 2], required=True)

args = parser.parse_args()

PATH = os.path.dirname(os.path.abspath(__file__))
inputfile = open(os.path.join(PATH, args.input), 'r', encoding='utf-8')
outputfile = open(os.path.join(PATH, args.output), 'w', encoding='utf-8')
src = os.path.basename(inputfile.name)
TRAINING_DATA = ijson.items(inputfile, 'item')
valueType = 'answer'
if args.select == 1:
  valueType = 'question'


indent = '{:2}'.format('')
indent2x = indent + indent
indent4x = indent2x + indent2x

outputfile.write('[\n')
for i, data in enumerate(TRAINING_DATA):
  if i > 0:
    outputfile.writelines(',')
  source = src
  if 'source' in data: 
    source - data['source']
  tags = '[]'
  if 'tags' in data:
    tags = '["%s"]' % '","'.join(data['tags'])
  outputfile.writelines([
    f'{indent}{{\n',
    f'{indent2x}"value": "%s",\n' % data[valueType],
    f'{indent2x}"origin": "%s",\n' % data['origin'],
    f'{indent2x}"source": "{source}",\n',
    f'{indent2x}"tags": {tags}\n',
    f'{indent}}}'
  ])

inputfile.close()
outputfile.write('\n]')
outputfile.close()
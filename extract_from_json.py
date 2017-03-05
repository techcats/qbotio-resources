import argparse, ijson, os

parser = argparse.ArgumentParser(description='Create a seperate question or answer JSON')
parser.add_argument('input', type=str, help='Input JSON file')
parser.add_argument('output', type=str, help='Output JSON file')
parser.add_argument('--select', type=int, help='Select [1] or [2] for question or answer respectively', choices=[1, 2], required=True)
parser.add_argument('--key', type=str, help='If JSON is not a list, provide a dot notation key e.g. item or key.item')

args = parser.parse_args()

PATH = os.path.dirname(os.path.abspath(__file__))
inputfile = open(os.path.join(PATH, args.input), 'r', encoding='utf-8')
outputfile = open(os.path.join(PATH, args.output), 'w', encoding='utf-8')
TRAINING_DATA = ijson.items(inputfile, args.key or 'item')
valueType = 'answer'
if args.select == 1:
  valueType = 'question'


indent = '{:2}'.format('')
indent2x = indent + indent
indent4x = indent2x + indent2x

outputfile.write('[\n')
for i, data in enumerate(TRAINING_DATA):
  if i > 0:
    outputfile.writelines(',\n')
  source = origin = tags = ''
  if 'source' in data: 
    source = f'{indent2x}"source": "%s",\n' % data['source']
  if 'origin' in data:
    origin = f'{indent2x}"origin": "%s",\n' % data['origin']
  if 'tags' in data:
    tags = f'{indent2x}"tags": %s\n' % ('["%s"]' % '","'.join(data['tags']))
  outputfile.writelines([
    f'{indent}{{\n',
    f'{source}',
    f'{origin}',
    f'{tags}',
    f'{indent2x}"value": "%s"\n' % data[valueType],
    f'{indent}}}'
  ])

inputfile.close()
outputfile.write('\n]')
outputfile.close()
#!/usr/bin/env python3
def main():
	import sys
	import json
	import datetime
	import codecs

	filename=sys.argv[1]
	print ("Filename: ", filename)
	with codecs.open(filename+'.txt', 'w', 'utf-8') as w:
		with codecs.open(filename, 'r', 'utf-8') as f:
			data=json.loads(f.read())
			labels = data['results']['speaker_labels']['segments']
			speaker_start_times={}
			for label in labels:
				for item in label['items']:
					speaker_start_times[item['start_time']] =item['speaker_label']
			items = data['results']['items']
			lines=[]
			line=''
			time=0
			speaker='null'
			wasPunctuation=False
			isPunctuation=False
			i=0
			for item in items:
				i=i+1
				content = item['alternatives'][0]['content']
				isPunctuation = (item['type'] == 'punctuation' and content != '、')

				if item.get('start_time'):
					current_speaker=speaker_start_times[item['start_time']]
					latest_time=item['start_time']
				elif isPunctuation:
					line = line+content

				if isPunctuation and not wasPunctuation:
					if speaker:
						lines.append({'speaker':speaker, 'line':line, 'time':time})
					line=''
					time=latest_time
				elif current_speaker != speaker:
					if speaker:
						lines.append({'speaker':speaker, 'line':line, 'time':time})
					line=content
					speaker=current_speaker
					time=item['start_time']
				elif not isPunctuation:
					line = line + content
				
				wasPunctuation = isPunctuation
			lines.append({'speaker':speaker, 'line':line,'time':time})
			sorted_lines = sorted(lines,key=lambda k: float(k['time']))
			speaker = 'null'
			for line_data in sorted_lines:
				current_speaker = line_data.get('speaker')
				if line_data.get('line'):
					line='[' + str(datetime.timedelta(seconds=int(round(float(line_data['time']))))) + '] ' + line_data.get('speaker') + ': ' + line_data.get('line')
					if speaker != 'null' and current_speaker != speaker:
						w.write('\n')
					w.write(line + '\n')
					speaker=current_speaker

if __name__ == '__main__':
	main()

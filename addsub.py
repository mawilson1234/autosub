import argparse, subprocess, os, sys, glob

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--video_file', nargs = '?', 
	help = 'The relative path(s) to the video file. Default is all files in the current directory that end in .mov.')
parser.add_argument('-o', '--output_file', nargs = '?', default = '',
	help = 'Where to save the file(s) with the hard-coded subtitles. Default are the video file names + "-subbed" in mp4 format.')
parser.add_argument('-s', '--subtitle_file', nargs = '?', default = '', 
	help = 'Relative path to the srt file(s). Default assumes they\'re the same name as the video file(s) but with an .srt extension.')
parser.add_argument('-r', '--rename', default = False, action = 'store_true',
	help = 'Whether to automatically rename files to avoid overwriting. The default prompts for whether to overwrite for each output file that already exists.')

args = parser.parse_args()

if not args.video_file:
	args.video_file = glob.glob('*.mov')
else:	
	args.video_file = glob.glob(args.video_file)

if not args.subtitle_file:
	args.subtitle_file = [f'{file[:-4]}.srt' for file in args.video_file]
else:
	args.subtitle_file = glob.glob(args.video_file)

if not args.output_file:
	args.output_file = [f'{file[:-4]}-subbed.mp4' for file in args.video_file]
else:
	args.output_file = args.output_file.split(':')

if not len(args.video_file) == len(args.subtitle_file) == len(args.output_file):
	print('Error: number of files do not match. Exiting...')
	sys.exit(1)


for vf, sf, of in tuple(zip(args.video_file, args.subtitle_file, args.output_file)):
	if not os.path.isfile(vf) or not os.path.isfile(sf):
		print(f'Video or subtitle file not found: {vf} (video), {sf} (subtitle). Skipping...')
		continue
	
	if os.path.isfile(of) and not args.rename:
		overwrite = input(f'File "{of}" already exists. Overwrite? [y/n/rename] ').lower()
		if not overwrite in ['y', 'rename', 'r']:
			print('Skipping...')
			continue
		elif overwrite in ['r', 'rename']:
			counter = 1
			of = f'{of[:-4]}-{counter}{of[-4:]}'
			while os.path.isfile(of):
				of = f'{of[:(-5-len(str(counter - 1)))]}-{counter}{of[-4:]}'
				counter += 1
	elif os.path.isfile(of):
		counter = 1
		of = f'{of[:-4]}-{counter}{of[-4:]}'
		while os.path.isfile(of):
			of = f'{of[:(-5-len(str(counter - 1)))]}-{counter}{of[-4:]}'
			counter += 1

	print(f'Adding subtitles to {vf}...')
	subprocess.call(f'ffmpeg -hide_banner -loglevel warning -i \'{vf}\' -vf "subtitles=\'{sf}\':force_style=\'Fontsize=24,PrimaryColour=&Hffffff&,BorderStyle=3\'" -c:a copy "{of}"', cwd = os.getcwd(), shell = True)

print('Done!')
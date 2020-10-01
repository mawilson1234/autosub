import argparse, subprocess, os, sys, glob, re

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--video_file', nargs = '?', 
	help = 'The relative path(s) to the video file(s). Default is all files in the current directory that end in .mov or .mp4.')
parser.add_argument('-o', '--output_file', nargs = '?', default = '',
	help = 'Where to save the file(s) with the hard-coded subtitles. Default are the video file names + "-subbed" in mp4 format.')
parser.add_argument('-s', '--subtitle_file', nargs = '?', default = '', 
	help = 'Relative path to the srt file(s). Default assumes they\'re the same name as the video file(s) but with an .srt extension.')
parser.add_argument('-r', '--rename', default = False, action = 'store_true',
	help = 'Whether to automatically rename files to avoid overwriting. The default prompts for whether to overwrite for each output file that already exists.')
parser.add_argument('-c', '--color', default = 'ffffff',
	help = 'The color (in hex) to use for the subtitles. Default is "ffffff" (white).')
parser.add_argument('-si', '--size', default = '24',
	help = 'The font size to use for the subtitles in pt. Default is 24.')
parser.add_argument('-b', '--border_style', default = '3',
	help = 'The border style to use for the subtitles. Default is 3 (opaque box). 1 uses an outline + drop shadow.')
parser.add_argument('-af', '--additional_formatting', default = '',
	help = 'Additional formatting to use for the subtitles, specified using SubStation Alpha style fields. Default is empty.')
parser.add_argument('-se', '--soft_embed', default = False, action = 'store_true',
	help = 'Set this if you want to soft-embed the subtitles instead (in which case rendering options can be set by the video playback software).')
parser.add_argument('-vc', '--video_codec', default = 'libx264',
	help = 'Set this to change the video codec. Default is libx264. The other valid option is libx265.')
parser.add_argument('-comp', '--compression', default = '22',
	help = 'Set this to change the compression ratio for the output video. The default is 22. Lower numbers mean less compression.')

args = parser.parse_args()

if not args.video_file:
	args.video_file = glob.glob('*.mov') + glob.glob('*.mp4')
else:	
	args.video_file = glob.glob(args.video_file)

if not args.subtitle_file:
	args.subtitle_file = [f'{file[:-4]}.srt' for file in args.video_file]
else:
	args.subtitle_file = glob.glob(args.subtitle_file)

if not args.output_file:
	args.output_file = [f'{file[:-4]}-subbed.mp4' for file in args.video_file]
else:
	args.output_file = args.output_file.split(':')

if args.additional_formatting:
	args.additional_formatting = ',' + args.additional_formatting

if not len(args.video_file) == len(args.subtitle_file) == len(args.output_file):
	print('Error: number of files do not match. Exiting...')
	sys.exit(1)

if args.video_codec == 'libx264':
	codec_string = f'libx264 -crf {args.compression}'
elif args.video_codec == 'libx265':
	codec_string = f'libx265 -x265-params log-level=error:crf={args.compression}'
else:
	print('Error: addsub only supports libx264 and libx265 codecs. Choose a valid codec and rerun.')

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

	# Convert sbv to srt to add them
	if os.path.splitext(sf)[1] == '.sbv':
		from captionstransformer.sbv import Reader
		from captionstransformer.srt import Writer

		with open(sf) as r:
			reader = Reader(r)

			with open(f'{os.path.splitext(sf)[0]}.srt', 'w') as w:
				writer = Writer(w)
				writer.set_captions(reader.read())
				writer.write()
				writer.close()

	print(f'Adding subtitles to {vf}...')

	if not args.soft_embed:
		subprocess.call(f'ffmpeg -hide_banner -loglevel warning -i "{vf}" -vf "subtitles=\'{sf}\':force_style=\'Fontsize={args.size},PrimaryColour=&H{args.color}&,BorderStyle={args.border_style}{args.additional_formatting}\'" -c:v {codec_string} -c:a copy "{of}"', cwd = os.getcwd(), shell = True)
	else:
		subprocess.call(f'ffmpeg -hide_banner -loglevel warning -i "{vf}" -i "{sf}" -c:v {codec_string} -c:a copy -c:s mov_text -disposition:s:0 default "{of}"', cwd = os.getcwd(), shell = True)

	# If the subtitle started off as sbv, try to delete the temporarily needed srt file
	# This isn't hugely important, so just pass if it fails
	if os.path.splitext(sf)[1] == '.sbv':
		try:
			os.remove(f'{os.path.splitext(sf)[0]}.srt')
		except:
			pass

print('Done!')
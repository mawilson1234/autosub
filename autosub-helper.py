import subprocess, argparse, glob, sys, os

DEFAULT_SUBTITLE_FORMAT = 'srt'
DEFAULT_CONCURRENCY = 10
DEFAULT_SRC_LANGUAGE = 'en'
DEFAULT_DST_LANGUAGE = 'en'

parser = argparse.ArgumentParser()
parser.add_argument('source_path', default = '', help="Path to the video or audio file to subtitle",
                        nargs='?')
parser.add_argument('-C', '--concurrency', help="Number of concurrent API requests to make",
                        type=int, default=DEFAULT_CONCURRENCY)
parser.add_argument('-o', '--output',
                        help="Output path for subtitles (by default, subtitles are saved in \
                        the same directory and name as the source path)")
parser.add_argument('-F', '--format', help="Destination subtitle format",
                        default=DEFAULT_SUBTITLE_FORMAT)
parser.add_argument('-S', '--src-language', help="Language spoken in source file",
                        default=DEFAULT_SRC_LANGUAGE)
parser.add_argument('-D', '--dst-language', help="Desired language for the subtitles",
                        default=DEFAULT_DST_LANGUAGE)
parser.add_argument('-K', '--api-key',
                        help="The Google Translate API key to be used. \
                        (Required for subtitle translation)")
parser.add_argument('--list-formats', help="List all available subtitle formats",
                        action='store_true')
parser.add_argument('--list-languages', help="List all available source/destination languages",
                        action='store_true')

args = parser.parse_args()

if sys.platform == 'darwin':
    app_path = '/Applications/autosub/autosub'
elif sys.platform == 'win32':
    app_path = '%ProgramFiles%/autosub/autosub'
else:
    print('Only Mac and Windows are currently supported. Exiting.')
    sys.exit(1)

if not (args.list_formats or args.list_languages):
    if not args.source_path:
        args.source_path = glob.glob('*.mov') + glob.glob('*.mp4')
    else:    
        args.source_path = glob.glob(args.source_path)

    if not args.output:
        args.output = [file[:-4] + '.srt' for file in args.source_path]
    else:
        args.output = args.output.split(':')

    if not len(args.output) == len(args.source_path):
        print("Number of videos doesn't match number of specified output files. Exiting.")
        sys.exit(1)

    if not args.api_key:
        keystr = ''
    else:
        keystr = ' -K ' + str(args.api_key)

    for source, output in tuple(zip(args.source_path, args.output)):
        subprocess.call('python "' + app_path + '" "' + str(source) + '" -C ' + str(args.concurrency) + ' -o "' + str(output) + '" -F ' + str(args.format) + ' -S ' + str(args.src_language) + ' -D ' + str(args.dst_language) + str(keystr), cwd = os.getcwd(), shell = True)

elif args.list_formats:
    subprocess.Popen('python "' + app_path + '" --list-formats', cwd = os.getcwd(), shell = True).communicate()

elif args.list_languages:
    subprocess.Popen('python "' + app_path + '" --list-languages', cwd = os.getcwd(), shell = True).communicate()


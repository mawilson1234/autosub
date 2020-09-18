(In progress)

# Requirements:
## Programs:
Python >=3.6

ffmpeg

## Python packages
(install using `pip install [packagename]` from a terminal/command prompt):

google-api-python-client

requests

pysrt

progressbar2

six

# Installation:
## Windows:
Install autosub + addsub by putting the autosub root folder in `%ProgramFiles%`, and adding `%ProgramFiles%\autosub` to your `PATH`.

To find the location of your `%ProgramFiles%` folder, open a command prompt and run `echo %ProgramFiles%`. Then, put the root autosub folder in the folder that was listed.

To add `%ProgramFiles%\autosub` to your `PATH`, right click on 'This PC' on your desktop, and select 'Properties'. On the left, select 'Advanced System Settings', and then 'Environment Variables'. On the lower panel, 'System variables', scroll down and find the entry for `Path` or `PATH`. Select that entry, and click 'Edit...'. On the right, click 'New', and type `%ProgramFiles%\autosub` (note the backslash!). Then click 'OK', 'OK', and 'OK' to exit the settings windows. You're done!

## Mac:
Mac is a bit more complex: you need to place the bash files in /usr/bin/local,
take ownership of them with chmod, and make them executable.
(Detailed instructions + bash files coming.)

# Usage
## `autosub`
`autosub [source_path] [-C/--concurrency] [-o/--output] [-F/--format] [-S/--src_language] [-D/--dst-language] [-K/--api_key] [--list-formats] [--list-languages]`

- `source_path`: the (relative or absolute) path to the video file you want to generate subtitles for. The default generates subtitles for every file with a `.mov` extension in the current directory. Unix-style wildcards are supported.
- `-C/--concurrency`: the number of concurrent API requests to make.
- `-o/--output`: the name of the output subtitle file(s). The default saves them in the same directory as the video and with the same name.
- `-F/--format`: the subtitle format. Default is `.srt`.
- `-S/--src-language`: the language spoken in the source video. Default is English.
- `-D/--dst-language`: the language to translate the subtitles to. Note that you will need to provide a Google Translate API key in order to use this functionality.
- `-K/--api-key`: a Google Translate API key to use. This is only needed if you are translating the subtitles.
- `--list-formats`: show all available subtitle formats.
- `--list-languages`: show all available source/destination languages.

## `addsub`
`addsub [-v/--video_file] [-o/--output_file] [-s/--subtitle_file] [-r/--rename] [-c/--color] [-si/--size] [-b/--border_style] [-af/--additional_formatting]`

- `-v/--video_file`: the relative or absolute path(s) to the video file(s). Default is all files in the current directory than end in `.mov`.
- `-o/--output_file`: where the save the output file(s) with the hard-coded subtitles. Default are the video file names + `-subbed` in `.mp4` format.
- `-s/--subtitle_file`: the relative or absolute path(s) to the srt file(s). Default assumes that they have the same name as the video file(s) but with an `.srt` extension.
- `-r/--rename`: Whether to automatically rename files to avoid overwriting. The default prompts for whether to overwrite for each output file name that already exists.
- `-c/--color`: the color (in hex) to use for the subtitles. Default is `ffffff` (white).
- `-si/--size`: the font size to use for the subtitles in pt. Default is 24.
- `-b/--border_style`: the border style to use for the subtitles. Default is 3 (opaque box). 1 uses an outline + drop shadow.
- `-af/--additional_formatting`: Additional formatting to use for the subtitles, specified using SubStation Alpha style fields. Default is empty.
- `-sc/--soft_embed`: Set this to soft-embed the subtitles instead of hard-embedding them, so that you can choose whether to display them and the formatting in the video playback software.
- `-comp/--compression`: The compression factor to use for the output video. Default is 22. Lower numbers mean less compression.

# Output
## `autosub`
An srt file containing the recognized speech. The default will put this in the same directory as the video with the same file name but an `.srt` extension. This can be edited in any text editor to fix formatting (punctuation and capitalization) and word recognition errors.

## `addsub`
A video file with hard-embedded or soft-embedded subtitles, depending on what options you set. The default hard-embeds the subtitles, and puts the resulting video(s) in the same directory as the original video(s), with the name `[original_file_name]-subbed.mp4`.

# Note
If you are soft-embedding subtitles, you may need to select the subtitle track manually in your video player; in particular, VLC requires this, and others may as well.
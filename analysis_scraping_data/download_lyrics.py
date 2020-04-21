# Thanks to https://github.com/sgiammy/emotion-patterns-in-music-playlists

import lyricwikia
import argparse
import sys
import os
import shutil  # high level operations on files (copying and removing)

import pandas

from progress.bar import Bar # progress bar

SPACE_CHARACHTER_SUBSTITUTION = '.'
SLASH_CHARACHTER_SUBSTITUTION = '-'
LOCAL_PATH = os.path.abspath('.')

parser = argparse.ArgumentParser(
    description='Download lyrics from LyricsWikia')
parser.add_argument('-i', '--input', type=str, help='Input file dataset')
parser.add_argument('-o', '--output', type=str, help='Output directory')
parser.add_argument('-s', '--skipHeader', action='store_true',
                    help='Wether or not the file contains an header which should be skipped')
parser.add_argument('-f', '--force', action='store_true', help='Force override lyrics available')


args = parser.parse_args()

LYRICS_PATH = './lyrics_lyricwikia'

LOG_FILE = '.'.join([sys.argv[0], 'log'])
try:
    os.remove(os.path.join('.', LOG_FILE))
except OSError:
    # Log file did not exists...not too bad
    pass


def count_songs(file_path):
    with open(file_path) as f:
        count = len(f.readlines()) - 1
        if args.skipHeader:
            count -= 1
        return count


def create_output_dir():
    if os.path.exists(LYRICS_PATH) and os.path.isdir(LYRICS_PATH):
        #shutil.rmtree(path)
        return
    os.makedirs(LYRICS_PATH)

def lyric_entries_generator(path):
    dataFrame = pandas.read_csv(path)
    for idx, row in dataFrame.iterrows(): 
        yield row



def download_lyric(song):
    try:
        filename = str(song['Index'])
        #filename = '_'.join([song['Index'], song['Emotion'], song['Artist'], song['Song']])
        #filename = filename.replace('/', SLASH_CHARACHTER_SUBSTITUTION)  # The '/' should never appear
        #filename = filename.replace(' ', SPACE_CHARACHTER_SUBSTITUTION) 
        
        if(not args.force and os.path.isfile(LOCAL_PATH + '/' + filename)):
            print('exists')
            return False
        
        with open(os.path.join(LYRICS_PATH, filename), 'w') as sfile:
            lyric = lyricwikia.get_lyrics(song['Artist'], song['Song'])
            sfile.write(lyric)
            sfile.close()
            return True
    except lyricwikia.LyricsNotFound:
        err('Could not download {}: {}, {}'.format(
            song['Index'], song['Artist'], song['Song']))
        return False


def err(msg):
    with open(os.path.join('.', LOG_FILE), 'a') as log:
        log.write(msg)
        log.write('\n')


if __name__ == '__main__':
    totalTitles = count_songs(args.input or "datasets/MoodyLyrics.csv")
    print(str(totalTitles) + ' canciones')

    # Create output directory
    create_output_dir()
    # Download songs
    count = 0
    errorCount = 0
    bar = Bar('Downloading lyrics', max = int(totalTitles))
    #for lyric in lyric_entries_generator(args.input):
    for lyric in lyric_entries_generator('datasets/MoodyLyrics.csv'):
        if not download_lyric(lyric):
            errorCount += 1
        count +=1
        bar.next()
    bar.finish()

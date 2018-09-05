#!/usr/bin/env python3

import os
import sys
import argparse

def printFailedTo(failedToDescription, error):
    sys.stderr.write('Failed to ' + failedActionDescription + ': ' + error + '\n')

def readDestinationsFile(destinationsFile):
    destinationDirectory = os.path.expandvars('$HOME')
    destinations = []
    for line in destinationsFile:
        if (line[-2] == ':'):
            destinationDirectory = os.path.expandvars(line[:-2])
        else:
            destinations.append((os.path.expandvars(line[:-1]), destinationDirectory))    # [:-1] to ignore '\n'
    return destinations

def linkFileToDirectory(filename, directory):
    filename = os.path.expandvars(filename)
    directory = os.path.expandvars(directory)
    printLinkFileToDirectoryFailedTo = lambda error: printFailedTo('link file \'{}\' to directory \'{}\''.format(filename, directory), error)

    if (not os.path.isfile(filename)):
        printLinkFileToDirectoryFailedTo('\'{}\' is not a file.'.format(filename))
        sys.exit(1)

    if (not os.path.isdir(directory)):
        if (os.path.exists(directory)):
            printLinkFileToDirectoryFailedTo('\'{}\' exists and it is not a directory.'.format(filename))
            sys.exit(1)
        else:
            print('Creating directory \'{}\'.'.format(directory))
            os.system('mkdir {}'.format(directory))

    print('Linking file \'{}\' to directory \'{}\''
            .format(filename, directory))
    os.system('ln -f {} {}'.format(filename, directory))

def linkDirectoryToDirectory(srcDirectory, dstDirectory):
    srcDirectory = os.path.expandvars(srcDirectory)
    dstDirectory = os.path.expandvars(dstDirectory)
    printLinkDirectoryToDirectoryFailedTo = lambda error: printFailedTo('link directory \'{}\' to directory \'{}\''.format(srcDirectory, dstDirectory), error)

    if (not os.path.isdir(srcDirectory)):
        printLinkDirectoryToDirectoryFailedTo('\'{}\' is not a directory.'.format(srcDirectory))
        sys.exit(1)

    print('Linking directory \'{}\' to directory \'{}\''.format(srcDirectory, dstDirectory))

    cwd = os.getcwd()
    os.chdir(srcDirectory)

    newDirectoryPath = os.path.join(dstDirectory, srcDirectory)
    if (not os.path.isdir(newDirectoryPath)):
        if (os.path.exists(newDirectoryPath)):
            printLinkDirectoryToDirectoryFailedTo('\'{}\' exists and not a directory'.format(newDirectoryPath))
            sys.exit(1)
        else:
            print('Creating directory \'{}\'.'.format(newDirectoryPath))
            os.system('mkdir {}'.format(newDirectoryPath))

    for filename in os.listdir('./'):       # we already changed directory to srcDirectory
        if (os.path.isfile(filename)):
            linkFileToDirectory(filename, newDirectoryPath)
        elif (os.path.isdir(filename)):
            linkDirectoryToDirectory(filename, newDirectoryPath)
        else:
            print('Ignoring \'{}\' as it is not a file or directory.'
                    .format(filename))

    os.chdir(cwd)

def main():
    parser = argparse.ArgumentParser(description='Link config files in repo to their domains.')
    parser.add_argument('destinations', type=str, nargs='?', default='.destinations',
            help='file with destionations, default is \'.destinations\'')
    args = parser.parse_args()

    destinationsFilePath = os.path.expandvars(args.destinations)
    if (not os.path.isfile(destinationsFilePath)):
        printFailedTo('read destinations file', '\'{}\' is not a file'.format(destinationsFilePath))
        sys.exit(1)
    with open(destinationsFilePath) as destinationsFile:
        destinations = readDestinationsFile(destinationsFile)

    for (filename, destination) in destinations:
        if (os.path.isfile(filename)):
            linkFileToDirectory(filename, destination)
        elif (os.path.isdir(filename)):
            linkDirectoryToDirectory(filename, destination)
        else:
            print('Ignoring \'{}\' as it is not a file or directory.'
                    .format(filename))

if (__name__ == '__main__'):
    main()

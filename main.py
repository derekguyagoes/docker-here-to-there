import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="which compose file to parse")
    parser.add_argument("-d", "--destination", help="where will the images end up")

    args = parser.parse_args()

    images = []
    sourceImages = []

    f = open(args.file)
    for line in f:
        if line.find("image") > -1:
            colon = line.find(":") + 1
            wholeline = str.strip(line[colon:])
            forwardslash = wholeline.find("/")
            if forwardslash > -1:
                if wholeline[:forwardslash].find(args.destination) == -1:
                    image = wholeline[forwardslash + 1:]
                    images.append(image)
                sourceImages.append(wholeline)

    f.close()

    f = open("send.sh", "w")
    f.write("#!/bin/sh\n\n")
    for image in images:
        for sourceImage in sourceImages:
            f.write('docker tag {0} {1}/{2}\n'.format(sourceImage, args.destination, image))
            f.write('docker push {0}/{1}\n\n'.format(args.destination, image))
            break
    f.close()

    f = open("send.sh", "r")
    print(f.read())


if __name__ == '__main__':
    main()

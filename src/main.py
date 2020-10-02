import argparse


def line_contains_image(line):
    return line.find("image") > -1


def writes_file(args, images, sourceImages):
    f = open("send.sh", "w")
    f.write("#!/bin/sh\n\n")
    for inx, val in enumerate(images):
        f.write('docker tag {0} {1}/{2}\n'.format(sourceImages[inx], args.destination, images[inx]))
        f.write('docker push {0}/{1}\n\n'.format(args.destination, images[inx]))

    f.close()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="which compose file to parse")
    parser.add_argument("-d", "--destination", help="where will the images end up")

    args = parser.parse_args()

    images = []
    sourceImages = []

    reads_file(args, images, sourceImages)

    writes_file(args, images, sourceImages)

    f = open("send.sh", "r")
    print(f.read())


def reads_file(args, images, sourceImages):
    f = open(args.file)
    for line in (line for line in f if not line.startswith('#')):
        if line_contains_image(line):
            image_key = line.find(":") + 1
            image = str.strip(line[image_key:])
            source_repo = image.find("/")
            if source_repo > -1:
                if image[:source_repo].find(args.destination) == -1:
                    images.append(image[source_repo + 1:])
                sourceImages.append(image)
    f.close()


if __name__ == '__main__':
    main()

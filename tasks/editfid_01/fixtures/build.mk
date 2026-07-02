# build config
VERSION = 1.4.2
CC = gcc
CFLAGS = -O2 -Wall

all: prep compile package

prep:
	mkdir -p dist
	echo prep $(VERSION)

compile: prep
	$(CC) $(CFLAGS) -o dist/app main.c

package: compile
	tar -czf dist/app-$(VERSION).tgz dist/app
	echo done

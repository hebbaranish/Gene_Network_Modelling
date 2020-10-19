CC 		= gcc
CFLAGS  = -g -pg -Wall -fopenmp
LIBS    = -lm

SRCS = main.c pcg_basic.c
OBJS = $(SRCS:.c=.o)

MAIN = main

.PHONY: depend clean

all: $(MAIN)

$(MAIN):$(OBJS)
		$(CC) $(CFLAGS) -o $(MAIN) $(OBJS) $(LIBS)

.c.o:
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) *.o *~ $(MAIN)

depend: $(SRCS)
	makedepend $(INCLUDES) $^

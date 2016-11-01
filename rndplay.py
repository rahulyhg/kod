# Plays mp3 files found under sys.argv[1] one by one, randomly. 
# Meant to simulate a radio.
import glob, os, random, sys
import threading
import select

fout = open("/tmp/rndplay.out","w")

while True:
    print "Music Dir", sys.argv[1]
    os.chdir(sys.argv[1])
    list = glob.glob("*.mp3")
    print '\n'
    idx = random.choice(range(len(list)))
    print "# of songs", len(list), 
    "song idx selected", idx, 
    "song", list[idx]
    fout.write(str(list[idx]) + "\n")
    fout.flush()
    print '\n'
    #cmd = "/usr/bin/ffplay -nodisp '%s'" % list[idx]
    cmd = "mplayer '%s'" % list[idx]
    print cmd
    os.system(cmd)
    print "Delete? (Press d for delete)..."
    k=""
    def input():
        global k
        i = 0
        while i < 1:
            i = i + 1
            r,w,x = select.select([sys.stdin.fileno()],[],[],2)
            if len(r) != 0:
                k  =sys.stdin.readline()


    T = threading.Thread(target=input)
    T.setDaemon(1)
    T.start()
    T.join(1) # wait for [arg] seconds
    print "\n>>>>>>>>>" + k
    if 'd' in k:
        print "deleting ===================> " +  list[idx]
        cmd = "rm '%s'" % list[idx]
        os.system(cmd)


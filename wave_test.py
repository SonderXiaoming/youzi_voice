from ftplib import all_errors
import wave


def remix(path):



    infiles = ["demo.wav", "demo1.wav"]
    outfile = "sounds.wav"

    data= []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    output.writeframes(data[0][1])
    output.writeframes(data[1][1])
    output.close()

if __name__ == "__main__":
    path = "d:/Users/CrisisChaos/Desktop/youzi_voice/demo.wav"
    remix(path)
    
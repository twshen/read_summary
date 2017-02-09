#!/usr/bin/env python
import re,os,sys,warnings,argparse

parser = argparse.ArgumentParser(description="""Read a list of samples and genearte
                                              read_summary.txt, cut.log, pass_junk.log,
                                              and score_his.txt.""")
parser.add_argument("-i", "--input", metavar="input.file", dest="finput",
                    action="store", type=str, required=True, 
                    help="input sample_list.txt (required)")
parser.add_argument("-o", "--output", metavar="output.file", dest="foutput",
                    action="store", default="read_summary.out", type=str, 
                    help="output file name (default: %(default)s)")
args = parser.parse_args()

class classSample:
    'sample object contaiing the number of raw reads and mappable reads'
    def __init__(self, sampleName, numRawReads, numReadsContaining3ADT, numShortReads,
                 numLongReads, numReadsExcluding3ADT, numMappableReads):
        self.sampleName = sampleName
        self.numRawReads = numRawReads
        self.numReadsContaining3ADT = numReadsContaining3ADT
        self.numShortReads = numShortReads
        self.numLongReads = numLongReads
        self.numReadsExcluding3ADT = numReadsExcluding3ADT
        self.numMappableReads = numMappableReads

def main(argv):
    oNumRawReads = re.compile(r"raw reads: (\d+)")
    oNumReadsContaining3ADT = re.compile(r"reads containing 3ADT: (\d+)")
    oNumShortReads = re.compile(r"<15 bases after 3ADT cut: (\d+)")
    oNumLongReads = re.compile(r">32 bases after 3ADT cut: (\d+)")
    oNumReadsExcluding3ADT = re.compile(r"<=32 bases after 3ADT cut: (\d+)")
    oNumMappableReads = re.compile(r"passed junk filter: (\d+)")
    sNumRawReads = oNumRawReads.search("") 
    sNumReadsContaining3ADT = oNumReadsContaining3ADT.search("")
    sNumShortReads = oNumShortReads.search("")
    sNumLongReads = oNumLongReads.search("")
    sNumReadsExcluding3ADT = oNumReadsExcluding3ADT.search("")
    sNumMappableReads = oNumMappableReads.search("")
    oSample = classSample("name", "0", "0", "0", "0", "0", "0")
    oSamples = []
    numRawReads = "0"
    numReadsContaining3ADT = "0"
    numShortReads = "0"
    numLongReads = "0"
    numReadsExcluding3ADT = "0"
    numMappableReads = "0"

    samples = []
    IN = open(args.finput, "r")
    for line in IN:
        samples.append(line[0:-1])
    IN.close()
    
    countSample = 0
    for sample in samples:
        filename = sample + r"/filter/cut.log"
        IN = open(filename, "r")
        for line in IN:
            sNumRawReads = oNumRawReads.search(line) 
            sNumReadsContaining3ADT = oNumReadsContaining3ADT.search(line)
            sNumShortReads = oNumShortReads.search(line)
            sNumLongReads = oNumLongReads.search(line)
            sNumReadsExcluding3ADT = oNumReadsExcluding3ADT.search(line)
            if sNumRawReads:
                numRawReads = sNumRawReads.group(1)
            elif sNumReadsContaining3ADT:
                numReadsContaining3ADT = sNumReadsContaining3ADT.group(1)
            elif sNumShortReads:
                numShortReads = sNumShortReads.group(1)
            elif sNumLongReads:
                numLongReads = sNumLongReads.group(1)
            elif sNumReadsExcluding3ADT:
                numReadsExcluding3ADT = sNumReadsExcluding3ADT.group(1)
            else:
                continue
        IN.close()
        filename = sample + r"/filter/pass_junk.log"
        IN = open(filename, "r")
        for line in IN:
            sNumMappableReads = oNumMappableReads.search(line)
            if sNumMappableReads:
                numMappableReads = sNumMappableReads.group(1)
            else:
                continue
        IN.close()
        oSamples.append(classSample(sample, numRawReads, numReadsContaining3ADT,
                                    numShortReads, numLongReads,
                                    numReadsExcluding3ADT, numMappableReads))
        countSample += 1
        
    sumSample = classSample("sum", "0", "0", "0", "0", "0", "0")
    OUT = open(args.foutput, "w")
    OUT.write("\t# raw reads\t# reads containing 3ADT\t" +
              "# reads <15 nt after removing 3ADT\t" +
              "# reads >32 nt after removing 3ADT\t" +
              "# reads after removing 3ADT\t# mappable reads\n")
    countSample = 0
    for oSample in oSamples:
        OUT.write(oSample.sampleName + "\t" + oSample.numRawReads + "\t"
                  + oSample.numReadsContaining3ADT + "\t"
                  + oSample.numShortReads + "\t"
                  + oSample.numLongReads + "\t"
                  + oSample.numReadsExcluding3ADT + "\t"
                  + oSample.numMappableReads + "\n")
        if countSample == 0:
            sumSample.numRawReads = oSample.numRawReads
            sumSample.numReadsContaining3ADT = oSample.numReadsContaining3ADT
            sumSample.numShortReads = oSample.numShortReads
            sumSample.numLongReads = oSample.numLongReads
            sumSample.numReadsExcluding3ADT = oSample.numReadsExcluding3ADT
            sumSample.numMappableReads = oSample.numMappableReads
        else:
            sumSample.numRawReads = str(long(sumSample.numRawReads) +
                                        long(oSample.numRawReads))
            sumSample.numReadsContaining3ADT = str(long(sumSample.numReadsContaining3ADT) +
                                                   long(oSample.numReadsContaining3ADT))
            sumSample.numShortReads = str(long(sumSample.numShortReads) +
                                          long(oSample.numShortReads))
            sumSample.numLongReads = str(long(sumSample.numLongReads) +
                                         long(oSample.numLongReads))
            sumSample.numReadsExcluding3ADT = str(long(sumSample.numReadsExcluding3ADT) + 
                                                  long(oSample.numReadsExcluding3ADT))
            sumSample.numMappableReads = str(long(sumSample.numMappableReads) +
                                             long(oSample.numMappableReads))
        countSample += 1
    OUT.close()
    CUTLOG = open("cut.log", "w")
    SCOREHIS = open("score_his.txt", "w")
    SCOREHIS.write("# of raw reads: " + sumSample.numRawReads + "\n")
    CUTLOG.write("# of raw reads: " + sumSample.numRawReads + "\n")
    CUTLOG.write("# of raw reads containing 3ADT: " +
                  sumSample.numReadsContaining3ADT + "\n")
    CUTLOG.write("# of raw reads of <15 bases after 3ADT cut: " +
                  sumSample.numShortReads + "\n")
    CUTLOG.write("# of raw reads of >32 bases after 3ADT cut: " +
                  sumSample.numLongReads + "\n\n")
    CUTLOG.write("# of good reads of >=15 & <=32 bases after 3ADT cut: " +
                  sumSample.numReadsExcluding3ADT + "\n")
    CUTLOG.close()
    SCOREHIS.close()

if __name__ == "__main__":
    main(sys.argv[1:])

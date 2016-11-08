import adGraph

# initialize graph
g = adGraph.Graph()

def readBatch():
    i = 1
    readHeader = False
    # Read in batch data file
    with open('/Users/akiramadono/code/data/insight_coding_data/batch_payment.csv','r') as batchFile:
        for lines in batchFile:
            if readHeader: # skip the header: time, id1, id2, amount, message
                all_tokens = lines.split(", ")
                id1 = all_tokens[1]
                id2 = all_tokens[2]
                g.add_edge(id1, id2)
            readHeader = True
            i += 1
#            if i > 5000:
#                break

def test():
    g.add_edge('a', 'h')
    g.add_edge('a', 'b')
    g.add_edge('a', 'f')
    g.add_edge('b', 'h')
    g.add_edge('b', 'g')
    g.add_edge('b', 'e')
    g.add_edge('e', 'g')
    g.add_edge('e', 'f')
    g.add_edge('e', 'm')
    g.add_edge('g', 'h')
    g.add_edge('g', 'm')
    g.add_edge('h', 'k')
    g.add_edge('k', 'm')
    result = g.breadth_first_search('a','k')
    print result

def readStream():
    i = 1
    readHeader = False
    with open('/Users/akiramadono/code/data/insight_coding_data/stream_payment.csv', 'r') as streamFile:
        for lines in streamFile:
            if readHeader:
                all_tokens = lines.split(", ")
                id1 = all_tokens[1]
                id2 = all_tokens[2]
                result = g.breadth_first_search(id2,id1)
                print result
            readHeader = True
            i += 1

readBatch()
print "Done reading batch file."
readStream()


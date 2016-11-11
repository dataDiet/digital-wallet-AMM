import adGraph

# read in batch_payment.txt file  and initial state edges into graph
def read_batch():

    i = 1
    # Read in batch data file
    batch_path = './paymo_input/batch_payment.txt'
    with open(batch_path,'r') as batchFile:
        print('Reading batch file: '+ batch_path)
        #skip the header: time, id1, id2, amount, message
        next(batchFile)
        for lines in batchFile:
            all_tokens = lines.split(", ")
            # id of person paying
            id1 = all_tokens[1]
            # id of person receiving payment
            id2 = all_tokens[2]
            # add edge to graph
            g.add_edge(id1, id2)
            i += 1
            if i % 100000 == 0:
                # print progress every 100,000 records
                print(str(i)+' messages read from batch file')
    print('Done reading batch file')

    # code for generating incoming/outgoing payment ratio stats
    # stats = open('/Users/akiramadono/code/data/insight_coding_data/stats.csv','w')
    # for key in g.get_vertices():
    #     stats.write(str(g.get_vertex(key).get_in_out())+'\n')
    # stats.close()

# read in stream_payment.txt file and determine trustworthiness from batch_payment data
# update batch state with new stream payment data
def read_stream():

    stream_path =  './paymo_input/stream_payment.txt'

    o1_file = './paymo_output/output1.txt'
    o2_file = './paymo_output/output2.txt'
    o3_file = './paymo_output/output3.txt'

    o1 = open(o1_file,'w')
    o1.close()
    o2 = open(o2_file,'w')
    o2.close()
    o3 = open(o3_file,'w')
    o3.close()

    with open(stream_path, 'r') as streamFile:
        # skip the header: time, id1, id2, amount, message
        next(streamFile)
        for lines in streamFile:
            all_tokens = lines.split(", ")
            # id of person paying
            id1 = all_tokens[1]
            # id of person receiving payment
            id2 = all_tokens[2]
            amount = all_tokens[3]
            message = all_tokens[4]

            bi_result = g.bidirectional_breadth_first_search(id1,id2)

            good = "trusted\n"
            bad = "unverified\n"

            output1 = output2 = output3 = bad

            if bi_result == 1:
                output1 = good
            if bi_result <= 2:
                output2 = good
            if bi_result <= 4:
                output3 = good

            # write to file in append mode with buffering
            with open(o1_file, 'a', 100) as o1:
                o1.write(output1)
            with open(o2_file, 'a', 100) as o2:
                o2.write(output2)
            with open(o3_file, 'a', 100) as o3:
                o3.write(output3)

            # add edge to graph
            g.add_edge(id1, id2)
            # delete oldest edge in graph
            v1 = g.get_vertex(id1)
            v2 = g.get_vertex(id2)
            inout1 = v1.get_in_out()
            inout2 = v2.get_in_out()

            suspicious_value = 10

            if inout1 > suspicious_value and bi_result > 4:
                print('User with id: '+id1+' with incoming/outgoing payment ratio '+str(inout1)+' suspected of fraud.')
            if inout2 > suspicious_value and bi_result > 4:
                print('User with id: '+id2+' with incoming/outgoing payment ratio '+str(inout2)+' suspected of fraud')

            # save space by deleting old edges
            g.del_edge()

if __name__ == '__main__':
    # initialize graph
    g = adGraph.Graph()
    read_batch()
    read_stream()

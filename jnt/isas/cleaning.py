import os
import csv
import random


def remove_cycles(list_data):
    hypo_to_hyper = {}
    for element in list_data:
        id = element[0]
        hypo = element[1]
        hyper = element[2]

        print("Read line with ID '%s': %s --> %s" % (id, hypo, hyper))

        if hypo not in hypo_to_hyper:
            hypo_to_hyper[hypo] = hyper
        elif random.randint(0, 1) == 0:
            print("Replace hypernym of hyponym '%s' with: %s" % (hypo, hyper))
            hypo_to_hyper[hypo] = hyper
        else:
            print("Keep hypernym '%s' of hyponym '%s'." % (hypo_to_hyper[hypo], hypo))

    return hypo_to_hyper


#Returns if contected to root or the highest parent
def connected_to_root(element, list_data, root):
    parent = element
    parent_last = None
    while parent != parent_last:
        parent_last = parent
        for relation in list_data:
            if parent == relation[1]:
                parent = relation[2]
                #print parent
                #break
    #print '\n'
    return [parent == root, parent]



def zero_out_nodes(elements):
    zero_out = set([])
    for element in elements:
        parents = [relation[2] for relation in list_data]
        if not element in parents:
            zero_out.add(element)
    return zero_out


#Used for removing everythign above root
def all_parent_rel(element, list_data):
    parent_root = element
    remove_relations = []
    for relation in list_data:
        if relation[1] == parent_root:
            remove_relations.append(relation)
    for ele in remove_relations:
        remove_relations += all_parent_rel(ele[2], list_data)
    return remove_relations


list_data = []
with open(os.path.join(os.path.dirname(__file__), '../../', 'vocabularies', 'science_en.csv-relations.csv-taxo.csv-SVC.csv'), 'rb') as f:
    reader = csv.reader(f, delimiter = '\t')
    for i, line in enumerate(reader):
        list_data.append((line[0], line[1], line[2]))
ROOT = "science"
all_parent_root = all_parent_rel(ROOT, list_data)
for el in all_parent_root:
    list_data.remove(el)

dict = remove_cycles(list_data)

list_data = []
iter = 1
for key, value in dict.iteritems():
    list_data.append((iter, key, value))
    iter+=1

elements = set([])
for relation in list_data:
    elements.add(relation[1])
    elements.add(relation[2])
elements_connected = set([])
for element in elements:
    ele_root = connected_to_root(element, list_data, ROOT)
    if not ele_root[0]:
       list_data.append((iter, ele_root[1], ROOT))
       iter+=1

with open(os.path.join(os.path.dirname(__file__), '../../', 'eval','taxi_eval_archive', 'input', 'system.taxo'), 'wb') as f:
    for element in list_data:
        print element
        f.write(str(element[0]) + '\t' + element[1] + '\t' + element[2]  + '\n')

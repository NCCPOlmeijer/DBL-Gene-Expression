def TelWoorden(filename):

    inFile = open(filename)
    raw_data = inFile.readlines()
    inFile.close()

    data = [line.strip() for line in raw_data[1::3]]

    desc_freq = {}

    for description in data:
        if description not in desc_freq:
            desc_freq[description] = 1
        else:
            desc_freq[description] += 1

    desc_freq = {keys: values for keys, values in sorted(
        desc_freq.items(), key=lambda item: item[1])}

    return desc_freq

#################################################################################################################


def descriptionCloneIDs(gen_description, cluster_result):
    '''Return dictionary with the description of genes acquired from GenDescription file as keys and
    the values a list containing the frequencies of the cloneIDs in a cluster provided by the cluster 
    result file.
    '''

    # Open gen_description and cluster_result files
    inFile = open(gen_description)
    raw_data = inFile.readlines()
    inFile.close()

    clusterResult = open(cluster_result)
    raw_cluster_data = clusterResult.readlines()
    clusterResult.close()

    # Create lists containing the descriptions and corresponding cloneIDs
    desc = [line.strip() for line in raw_data[1::3]]
    cloneIDs = [line.strip() for line in raw_data[0::3]]

    # Create empty dictionary named descCloneIDs
    descCloneIDs = {}

    # Add descriptions as key to descCloneIDs with values a list containing
    # all cloneIDs corresponding to that description
    for item in range(len(desc)):
        if desc[item] not in descCloneIDs:
            descCloneIDs[desc[item]] = [cloneIDs[item]]
        else:
            descCloneIDs[desc[item]].append(cloneIDs[item])

    # Create empty dictionary named clusterFreq
    clusterFreq = {}

    cluster_data = [item for sublist in [line.strip().split()
                                         for line in raw_cluster_data] for item in sublist]

    cloneIDValues = list(descCloneIDs.values())
    cloneIDKeys = list(descCloneIDs.keys())

    for description in range(len(descCloneIDs)):

        clusterFreq[cloneIDKeys[description]] = [0, 0, 0, 0, 0, 0]

        for cloneID in range(len(cloneIDValues[description])):
            if cloneIDValues[description][cloneID] in cluster_data:
                cluster_index = cluster_data.index(
                    cloneIDValues[description][cloneID]) + 1
                cluster_value = int(cluster_data[cluster_index])
                clusterFreq[cloneIDKeys[description]][cluster_value] += 1

            else:
                pass

    return clusterFreq

#################################################################################################################


GenDescription = "C:\Users\NoahPC\OneDrive - TU Eindhoven\BBT year 1 - 2020-2021\Q4\OGO Gene expression\DBL-Gene-Expression\Data\GenDescription2.txt"
clusterResultFile = "C:\Users\NoahPC\OneDrive - TU Eindhoven\BBT year 1 - 2020-2021\Q4\OGO Gene expression\DBL-Gene-Expression\Data\Voorbeeld_clusterresult.txt"

if __name__ == "__main__":
    print(descriptionCloneIDs(GenDescription, clusterResultFile))

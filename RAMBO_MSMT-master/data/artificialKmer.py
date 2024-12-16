import numpy as np

gene = 'ATGC'
kmers = []

maxV = 10
intervel = 5  # 5 sets

f = open("data/ArtfcKmersToy"+str(intervel)+".txt", "w")

for j in range(0,1000):  # 1000 test queries
    # Generate random 21-mer
    a = ''
    for i in range(0,21):
        a = a + gene[np.random.randint(4, size=1)[0]]
    
    # Generate 1-5 random sets (more realistic distribution)
    num_sets = np.random.randint(1, 6)  # Between 1-5 sets
    VI = np.random.choice(5, size=num_sets, replace=False)  # Random sets
    
    # Format output
    a = a + ';' + ','.join(['%d' % num for num in sorted(VI)])
    f.write(a + '\n')

f.close()
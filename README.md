# RAMBO: Scalable Genomic Sequence Search with Bloom Filters

RAMBO (Repeated And Merged Bloom Filter) is a method designed to reduce the query cost of sequence search over large-scale datasets. By combining Bloom Filters with a Count-Min Sketch-inspired approach, RAMBO achieves sublinear query time \(O(\sqrt{K} \log K)\) in the number of files while maintaining memory efficiency close to the theoretical limit.

This project focuses on adapting RAMBO for smaller-scale genomic datasets, specifically targeting applications such as detecting common foodborne pathogens in genomic sequences. By using synthetic and real datasets, we demonstrate how RAMBO can be applied to identify harmful bacterial strains with high speed and memory efficiency.

---

## Setup Instructions

### Step 1: Environment Setup
If you're using a Mac with Apple Silicon (M1/M2), you'll need to emulate x86_64 architecture:
```bash
# Install Rosetta 2 if you haven't already
softwareupdate --install-rosetta

# Start x86_64 shell
arch -x86_64 /bin/bash
```

For other systems, proceed directly to the next step.


### Step 2: K-mer Processing with Jellyfish
To prepare the genomic sequences for indexing in RAMBO, we use the Jellyfish library to extract k-mers from the downloaded FASTA files. Jellyfish is a fast and memory-efficient tool designed for counting and extracting k-mers from genomic data.

K-mer Extraction Workflow
Install Jellyfish: If you do not already have Jellyfish installed, install it using:
```bash
brew install jellyfish  # macOS
sudo apt-get install jellyfish  # Debian/Ubuntu
```
Generate K-mers: Run the following command for each FASTA file to generate k-mers:

```bash
jellyfish count -m 21 -s 100M -t 10 input.fasta -o output.jf
```
-m 21: Sets the k-mer length to 21 (can be adjusted based on hyperparameters).
-s 100M: Sets the hash size to 100M.
-t 10: Uses 10 threads for parallel processing.
Export K-mers: Convert the Jellyfish database into a text file containing k-mers:

```bash
jellyfish dump output.jf > kmers.txt
```

Prepare RAMBO Input: Move the kmers.txt files into the appropriate data directory to use them as input for RAMBO.


### Step 3: Build and Run RAMBO

You can run RAMBO in two modes: parameter analysis or fixed parameters.

#### Option 1: Parameter Analysis
To analyze different hyperparameter combinations and generate performance plots:
```bash
# Build RAMBO
make

# Run parameter analysis
python analyze_rambo.py
```

This will:
1. Test multiple combinations of parameters:
   - R (repetitions): [1,3,5,7]
   - B (bucket size): [30,40,50,60]
   - n (dataset size): [20000000]
   - p (false positive rate): [0.01,0.2,0.4]
2. Generate plots in the `rambo_analysis/` directory showing:
   - Memory usage vs false positive rate
   - Query time vs false positive rate
3. Save numerical results in `rambo_analysis/results_p.txt`

#### Option 2: Fixed Parameters
To run RAMBO with a specific set of parameters:
```bash
# Build RAMBO
make

# Run with fixed parameters
./build/program [dataset_id] [R] [B] [n] [mode] [p]
```

Parameters:
- dataset_id: Use 0 for the example dataset
- R: Number of repetitions (e.g., 5)
- B: Bucket size (e.g., 50)
- n: Dataset size
- mode: Use 1 for training, 0 for testing
- p: Target false positive rate (e.g., 0.01)

Example with recommended parameters:
```bash
# Training
./build/program 0 3 50 20000000 1 0.1

# Testing
./build/program 0 3 50 20000000 0 0.1
```

---

## Project Scope and Limitations

This implementation serves as a proof of concept for the RAMBO approach. Due to computational constraints, we tested with smaller datasets than those described in the original paper. For real-world applications processing terabytes of genomic data, the implementation would need:

1. Distributed computing capabilities
2. Optimized memory management
3. Parallel processing of large-scale datasets
4. Cloud infrastructure integration

Future extensions could include:
- Scaling to handle terabyte-scale genomic databases
- Distributed RAMBO implementation
- GPU acceleration for hash computations
- Integration with cloud storage systems

---

### Memory Management
If you encounter memory issues while running the parameter analysis:

Reduce the parameter combinations in `analyze_rambo.py`:
   - Decrease the range of values being tested
   - Test fewer combinations at once
   - Example modification:
   ```python
   # Instead of
   R_values = [5]
   B_values = [60]
   n_values = [20000000]
   p_values = [0.01, 0.2, 0.4]

   # Try fewer combinations
   R_values = [5]
   B_values = [60]
   n_values = [10000000]  # Reduce dataset size
   p_values = [0.01, 0.4]  # Test fewer p values
   ```

---

## Original Implementation
This code is based on the paper:

**[Fast Processing and Querying of 170TB of Genomics Data via a Repeated And Merged BloOm Filter (RAMBO)](https://dl.acm.org/doi/10.1145/3448016.3457333)**

If you use RAMBO in an academic context or for any publication, please cite the original paper:

```
@inproceedings{10.1145/3448016.3457333,
  author = {Gupta, Gaurav and Yan, Minghao and Coleman, Benjamin and Kille, Bryce and Elworth, R. A. Leo and Medini, Tharun and Treangen, Todd and Shrivastava, Anshumali},
  title = {Fast Processing and Querying of 170TB of Genomics Data via a Repeated And Merged BloOm Filter (RAMBO)},
  year = {2021},
  isbn = {9781450383431},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3448016.3457333},
  doi = {10.1145/3448016.3457333},
  pages = {2226–2234},
  numpages = {9},
  keywords = {information retrieval, bloom filter, genomic sequence search},
  location = {Virtual Event, China},
  series = {SIGMOD/PODS '21}
}
```

## Implementation Notes

### Code Structure
- The repository contains two files with `main()` functions:
  - `src/main.cpp` (current implementation)
  - `src/insertBloomfilter.cpp` (deprecated)
  
We use the implementation in `main.cpp` as it contains the most recent updates. The `insertBloomfilter.cpp` file is kept for reference but is not used in the current build to avoid multiple `main()` definition errors.


---

## Setup Instructions

### Step 1: Install Dependencies
#### Install GNU Parallel
- **macOS**:
  ```
  brew install parallel
  ```
- **Debian/Ubuntu**:
  ```
  sudo apt-get install parallel
  ```
- **RedHat/CentOS**:
  ```
  sudo yum install parallel
  ```

#### Additional Tools
Install `wget` and `bzip2`:
```bash
sudo apt-get install wget bzip2
```

#### Install CortexPy
Refer to the official installation instructions: [CortexPy Documentation](https://cortexpy.readthedocs.io/en/latest/overview.html#installation).

---

### Step 2: Data Preparation
1. **Unzip Example Data**:
   ```bash
   unzip data/0.zip
   ```
2. **Download and Prepare Data**:
   ```bash
   sh data/0/download.sh
   ```
3. **Create Output Directories**:
   ```bash
   mkdir -p results/RAMBOSer_100_0 results/RAMBOSer_200_0 results/RAMBOSer_500_0 \
             results/RAMBOSer_1000_0 results/RAMBOSer_2000_0
   ```
4. **Execute Commands**:
   Process the data files sequentially:
   ```bash
   parallel -j 50 :::: data/0/0_1.txt
   parallel -j 50 :::: data/0/0_2.txt
   parallel -j 50 :::: data/0/0_3.txt
   ```
5. **Verify Data**:
   Ensure all files are inflated and available:
   ```bash
   ls data/0/inflated/
   ```

---

### Step 3: Generate Synthetic Data
To create synthetic k-mer datasets for testing, run the following:
```bash
python3 artificialKmer.py
```
This script generates a file of synthetic k-mers with spiked pathogenic markers for querying.

---

### Step 4: Build and Run RAMBO
1. **Modify Parameters**:
   - Adjust `include/constants.h` for the number of sets.
   - Edit `src/main.cpp` to set parameters `m`, `B`, and `R` (lines 29–31).

2. **Build the Program**:
   ```bash
   make
   ```

3. **Run RAMBO**:
   ```bash
   ./build/program 0
   ```

---

## Notes
- This implementation has been adapted for smaller datasets and may require tuning for different data sizes or computational constraints.
- For larger datasets, additional memory and compute resources will be required.

---

## Contact
If you encounter issues or have questions about the code or usage, feel free to reach out!

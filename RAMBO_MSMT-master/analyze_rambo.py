import subprocess
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import math

results_dir = f'rambo_analysis'
os.makedirs(results_dir, exist_ok=True)

def run_rambo(R, B, n_perSet, p):
    # Calculate k and range based on p
    k = math.ceil(-math.log(p) / math.log(2))
    print(f"k: {k}")
    range_size = math.ceil(-(n_perSet * math.log(p)) / (math.log(2) * math.log(2)))
    print(f"range_size: {range_size}")

    # Training run
    subprocess.run(['./build/program', '0', str(R), str(B), str(n_perSet), '1', str(p)])
    
    # Testing run
    output = subprocess.run(['./build/program', '0', str(R), str(B), str(n_perSet), '0', str(p)], 
                          capture_output=True, text=True)
    
    # Parse results
    fp_rate = None
    query_time = None
    for line in output.stdout.split('\n'):
        if 'fp rate is:' in line:
            fp_rate = float(line.split(':')[1])
        if 'query time wall clock is' in line:
            query_time = float(line.split(':')[1].split(',')[0])
    
    # Calculate memory (theoretical)
    memory = R * B * range_size / 8  # in bytes
    
    return fp_rate, query_time, memory

# Test ranges
R_values = [1,3,5,7]
B_values = [30,40,50,60]
n_values = [20000000]
p_values = [0.01,0.2,0.4]  

# Results storage
results = []

# Run experiments
total_experiments = len(R_values) * len(B_values) * len(n_values) * len(p_values)
current = 0

print("Starting experiments...")
start_time = time.time()

for R in R_values:
    for B in B_values:
        for n in n_values:
            for p in p_values:
                current += 1
                print(f"\nExperiment {current}/{total_experiments}")
                print(f"Testing R={R}, B={B}, n={n}, p={p}")
                
                fp_rate, query_time, memory = run_rambo(R, B, n, p)
                if fp_rate is None:
                    print("Skipping this configuration due to memory constraints")
                    continue
                
                results.append((R, B, n, p, fp_rate, query_time, memory))
                
                # Print intermediate results
                print(f"FP Rate: {fp_rate:.4f}")
                print(f"Query Time: {query_time:.4f}ms")
                print(f"Memory: {memory/1024/1024:.2f}MB")

elapsed = time.time() - start_time
print(f"\nTotal time: {elapsed:.2f} seconds")

# Plot results
fig, axes = plt.subplots(len(B_values), 2, figsize=(15, 5*len(B_values)))

for b_idx, B in enumerate(B_values):
    # Memory vs p for this B value
    axes[b_idx, 0].set_title(f'Memory Usage vs p (B={B})')
    for R in R_values:
        data = [(x[6]/1024/1024, x[3]) for x in results if x[0] == R and x[1] == B]  # Convert to MB
        axes[b_idx, 0].plot([x[1] for x in data], [x[0] for x in data], label=f'R={R}')
    axes[b_idx, 0].set_xlabel('False Positive Rate (p)')
    axes[b_idx, 0].set_ylabel('Memory (MB)')
    axes[b_idx, 0].legend()

    # Query Time vs p for this B value
    axes[b_idx, 1].set_title(f'Query Time vs p (B={B})')
    for R in R_values:
        data = [(x[5], x[3]) for x in results if x[0] == R and x[1] == B]
        axes[b_idx, 1].plot([x[1] for x in data], [x[0] for x in data], label=f'R={R}')
    axes[b_idx, 1].set_xlabel('False Positive Rate (p)')
    axes[b_idx, 1].set_ylabel('Query Time (ms)')
    axes[b_idx, 1].legend()

plt.tight_layout()
plt.savefig(f'{results_dir}/rambo_analysis_p.png')
plt.close()

# Save the numerical results to a text file
with open(f'{results_dir}/results_p.txt', 'w') as f:
    f.write("\nRAMBO Results:\n")
    for R, B, n, p, fp_rate, query_time, memory in results:
        f.write(f"R={R}, B={B}, n={n}, p={p}: FP={fp_rate:.4f}, Time={query_time:.4f}ms, Mem={memory/1024/1024:.2f}MB\n")

print(f"\nResults saved in: {results_dir}/")
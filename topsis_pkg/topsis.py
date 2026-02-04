import sys
import pandas as pd
import numpy as np
import os

def normalize(data, weights, impacts):
    sq = np.sqrt((data**2).sum(axis=0))
    norm_data = data / sq
    weighted_data = norm_data * weights
    
    best = []
    worst = []
    
    for i in range(len(impacts)):
        if impacts[i] == '+':
            best.append(np.max(weighted_data[:, i]))
            worst.append(np.min(weighted_data[:, i]))
        else:
            best.append(np.min(weighted_data[:, i]))
            worst.append(np.max(weighted_data[:, i]))
            
    return weighted_data, best, worst

def calc_topsis(data, weights, impacts):
    weighted_data, best, worst = normalize(data, weights, impacts)
    
    s_best = np.sqrt(((weighted_data - best)**2).sum(axis=1))
    s_worst = np.sqrt(((weighted_data - worst)**2).sum(axis=1))
    
    score = s_worst / (s_best + s_worst)
    return score

def main():
    if len(sys.argv) != 5:
        print("Usage: python topsis.py <file> <weights> <impacts> <result_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights_input = sys.argv[2]
    impacts_input = sys.argv[3]
    output_file = sys.argv[4]

    if not os.path.exists(input_file):
        print("File not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(input_file)
    except:
        print("Could not read file.")
        sys.exit(1)

    if df.shape[1] < 3:
        print("Need at least 3 columns.")
        sys.exit(1)

    temp_df = df.iloc[:, 1:].values
    
    if not np.issubdtype(temp_df.dtype, np.number):
        print("Columns 2+ must be numeric.")
        sys.exit(1)

    try:
        weights = [float(x) for x in weights_input.split(',')]
        impacts = impacts_input.split(',')
    except:
        print("Weights must be numbers.")
        sys.exit(1)

    if len(weights) != temp_df.shape[1] or len(impacts) != temp_df.shape[1]:
        print("Length mismatch: weights/impacts vs columns.")
        sys.exit(1)

    if not all(x in ['+', '-'] for x in impacts):
        print("Impacts must be + or -.")
        sys.exit(1)

    scores = calc_topsis(temp_df, weights, impacts)
    
    df['Topsis Score'] = scores
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)
    
    df.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
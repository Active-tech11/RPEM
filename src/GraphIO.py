import os

def convert_to_csv(input_file, output_folder, output_file):
    output_path = os.path.join(output_folder, output_file)

    with open(input_file, 'r') as infile, open(output_path, 'w') as outfile:
        next(infile)  # 跳过第一行
        for line in infile:
            outfile.write(line)

if __name__ == "__main__":
    input_file = r"DataSet\resource.dolphins"
    output_folder = r"DataSet"
    output_file = "dolphins.csv"
    convert_to_csv(input_file, output_folder, output_file)

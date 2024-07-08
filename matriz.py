import pandas as pd
import sys

def generate_output_file(input_excel, output_file, from_time, to_time, factor):
    # Load the Excel file
    df = pd.read_excel(input_excel, index_col=0)

    from_time_float = float(from_time)
    to_time_float = float(to_time)
    
    time_difference = to_time_float - from_time_float
    
    time_difference_str = f"{time_difference:05.2f}"
    
    with open(output_file, 'w') as f:
        # Write the header
        f.write('$OR;D2\n')
#        f.write(f'* From-Time  To-Time\n{from_time} {to_time}\n')
        f.write(f'* From-Time  To-Time\n00.00 {time_difference_str}\n')
        f.write('* Factor\n')
        f.write(f'{factor}\n')
        f.write('* some\n')
        f.write('* additional\n')
        f.write('* comments\n')
        
        # Write the data
        for from_location, row in df.iterrows():
            for to_location, num_vehicles in row.items():
                f.write(f'\t\t{from_location.ljust(30)}{to_location.ljust(30)}{num_vehicles}\n')

if __name__ == '__main__':
    # Ensure correct usage
    if len(sys.argv) != 6:
        print("Usage: python generate_file.py <input_excel> <output_file> <from_time> <to_time> <factor>")
        sys.exit(1)
    
    input_excel = sys.argv[1]
    output_file = sys.argv[2]
    from_time = sys.argv[3]
    to_time = sys.argv[4]
    #factor = float(sys.argv[5])
    factor = int(sys.argv[5])
    
    generate_output_file(input_excel, output_file, from_time, to_time, factor)


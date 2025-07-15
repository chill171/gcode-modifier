import argparse
import re

def modify_gcode(input_path, output_path, nozzle_temp=None, bed_temp=None, print_speed=None):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.startswith('M104') and nozzle_temp is not None:
            line = re.sub(r'S\d+', f'S{nozzle_temp}', line)
        elif line.startswith('M140') and bed_temp is not None:
            line = re.sub(r'S\d+', f'S{bed_temp}', line)
        elif line.startswith('G1') and 'F' in line and print_speed is not None:
            line = re.sub(r'F\d+', f'F{print_speed}', line)

        modified_lines.append(line)

    with open(output_path, 'w') as file:
        file.writelines(modified_lines)

    print(f"Modified G-code saved to: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modify G-code: nozzle temp, bed temp, print speed.')
    parser.add_argument('--input', required=True, help='Path to input G-code file')
    parser.add_argument('--output', required=True, help='Path to output modified G-code file')
    parser.add_argument('--nozzle', type=int, help='Nozzle temperature in °C')
    parser.add_argument('--bed', type=int, help='Bed temperature in °C')
    parser.add_argument('--speed', type=int, help='Print speed in mm/min')

    args = parser.parse_args()

    modify_gcode(
        input_path=args.input,
        output_path=args.output,
        nozzle_temp=args.nozzle,
        bed_temp=args.bed,
        print_speed=args.speed
    )
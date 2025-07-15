import re

def modify_gcode(input_path, output_path, nozzle_temp=None, bed_temp=None, print_speed=None):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        # Modify nozzle temperature (M104)
        if line.startswith('M104') and nozzle_temp is not None:
            line = re.sub(r'S\d+', f'S{nozzle_temp}', line)

        # Modify bed temperature (M140)
        elif line.startswith('M140') and bed_temp is not None:
            line = re.sub(r'S\d+', f'S{bed_temp}', line)

        # Modify print speed (G1 Fxxxx)
        elif line.startswith('G1') and 'F' in line and print_speed is not None:
            line = re.sub(r'F\d+', f'F{print_speed}', line)

        modified_lines.append(line)

    with open(output_path, 'w') as file:
        file.writelines(modified_lines)

    print(f"Modified G-code saved to: {output_path}")


# Example usage
modify_gcode(
    input_path='example_input.gcode',
    output_path='modified_output.gcode',
    nozzle_temp=215,
    bed_temp=65,
    print_speed=2200
)
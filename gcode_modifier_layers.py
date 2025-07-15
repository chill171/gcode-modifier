import argparse
import re

def parse_layer_settings(arg_list):
    """Convert list like ['200:0', '210:5'] into dict {0: 200, 5: 210}"""
    result = {}
    for entry in arg_list:
        value, layer = entry.split(':')
        result[int(layer)] = int(value)
    return result


def modify_gcode(input_path, output_path, temp_layers=None, speed_layers=None):
    current_temp = None
    current_speed = None
    current_layer = -1

    with open(input_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []

    for line in lines:
        if line.startswith(';LAYER:'):
            current_layer = int(line.strip().split(':')[1])

            if temp_layers and current_layer in temp_layers:
                current_temp = temp_layers[current_layer]
                modified_lines.append(f'M104 S{current_temp}\n')

            if speed_layers and current_layer in speed_layers:
                current_speed = speed_layers[current_layer]

        if line.startswith('G1') and 'F' in line and current_speed is not None:
            line = re.sub(r'F\d+', f'F{current_speed}', line)

        modified_lines.append(line)

    with open(output_path, 'w') as file:
        file.writelines(modified_lines)

    print(f"Modified G-code saved to: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modify G-code settings by layer')
    parser.add_argument('--input', required=True, help='Input G-code file')
    parser.add_argument('--output', required=True, help='Output G-code file')
    parser.add_argument('--temp_at_layers', nargs='*', help='Nozzle temp changes: format TEMP:LAYER (e.g. 200:0 210:5)')
    parser.add_argument('--speed_at_layers', nargs='*', help='Speed changes: format SPEED:LAYER (e.g. 1800:0 2400:10)')

    args = parser.parse_args()

    temp_settings = parse_layer_settings(args.temp_at_layers) if args.temp_at_layers else None
    speed_settings = parse_layer_settings(args.speed_at_layers) if args.speed_at_layers else None

    modify_gcode(
        input_path=args.input,
        output_path=args.output,
        temp_layers=temp_settings,
        speed_layers=speed_settings
    )
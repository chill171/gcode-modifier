import argparse
import re
import json
import os

from datetime import datetime

def write_summary_log(output_path, input_path, temp_settings, speed_settings, mode):
    summary_path = output_path.replace('.gcode', '_summary.txt')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(summary_path, 'w') as f:
        f.write(f"🔧 G-code Modification Summary\n")
        f.write(f"Timestamp     : {now}\n")
        f.write(f"Input file    : {input_path}\n")
        f.write(f"Output file   : {output_path}\n")
        f.write(f"Mode          : {mode}\n")

        f.write("\nLayer Temp Changes:\n")
        if temp_settings:
            for layer, temp in sorted(temp_settings.items()):
                f.write(f"  Layer {layer}: {temp}°C\n")
        else:
            f.write("  None\n")

        f.write("\nLayer Speed Changes:\n")
        if speed_settings:
            for layer, speed in sorted(speed_settings.items()):
                f.write(f"  Layer {layer}: {speed} mm/min\n")
        else:
            f.write("  None\n")

    print(f"Summary saved to: {summary_path}")

def parse_layer_settings(arg_list):
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

def load_json_preset(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    temp_layers = {int(k): v for k, v in data.get('temp_at_layers', {}).items()}
    speed_layers = {int(k): v for k, v in data.get('speed_at_layers', {}).items()}
    return temp_layers, speed_layers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modify G-code using CLI or preset or material profile.')
    parser.add_argument('--input', required=True, help='Input G-code file')
    parser.add_argument('--output', required=True, help='Output G-code file')
    parser.add_argument('--preset', help='Path to custom JSON preset file')
    parser.add_argument('--material', help='Material name (loads presets/<material>.json)')
    parser.add_argument('--temp_at_layers', nargs='*', help='Manual temp changes TEMP:LAYER')
    parser.add_argument('--speed_at_layers', nargs='*', help='Manual speed changes SPEED:LAYER')

    args = parser.parse_args()

    temp_settings = None
    speed_settings = None

    if args.preset:
        temp_settings, speed_settings = load_json_preset(args.preset)
    elif args.material:
        material_path = os.path.join(os.path.dirname(__file__), "presets", f"{args.material}.json")
        temp_settings, speed_settings = load_json_preset(material_path)
    else:
        if args.temp_at_layers:
            temp_settings = parse_layer_settings(args.temp_at_layers)
        if args.speed_at_layers:
            speed_settings = parse_layer_settings(args.speed_at_layers)

    modify_gcode(
        input_path=args.input,
        output_path=args.output,
        temp_layers=temp_settings,
        speed_layers=speed_settings
    )

    # Save a summary file
    summary_name = os.path.splitext(os.path.basename(args.output))[0] + "_summary.txt"
    summary_path = os.path.join("gcode_modifier_tool", "test_outputs", "summaries", summary_name)

    with open(summary_path, 'w') as summary:
        summary.write(f"G-code: {args.output}\n")
        summary.write(f"Material: {args.material or 'N/A'}\n")
        summary.write(f"Preset: {args.preset or 'N/A'}\n")
        summary.write(f"Temp layers: {temp_settings or 'N/A'}\n")
        summary.write(f"Speed layers: {speed_settings or 'N/A'}\n")

    print(f"Summary saved to: {summary_path}")

  
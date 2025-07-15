def modify_gcode(input_path, output_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        modified_lines.append(line)  # no changes yet

    with open(output_path, 'w') as file:
        file.writelines(modified_lines)

    print(f'Modified G-code saved to: {output_path}')


# Test run
modify_gcode('example_input.gcode', 'modified_output.gcode')

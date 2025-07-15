# G-code Modifier Tool

A Python-based command-line utility for modifying 3D printer G-code files. Supports:

- Global changes to nozzle temp, bed temp, or print speed
- Layer-specific parameter overrides
- JSON presets for test plans (e.g. calibration towers)
- Material profiles (PLA, ABS, PETG, etc.)
- Auto-generated `.txt` summaries of each run

## Usage

Run layer-specific edits with a material:

```bash
python3 gcode_modifier_layers.py \
  --input example_input.gcode \
  --output test_outputs/abs_output.gcode \
  --material abs

Or use mannual overides 

```bash
python3 gcode_modifier_layers.py \
  --input file.gcode \
  --output out.gcode \
  --temp_at_layers 200:0 210:3 \
  --speed_at_layers 1800:0 2400:5

gcode_modifier_tool/
├── gcode_modifier.py
├── gcode_modifier_CLI.py
├── gcode_modifier_layers.py
├── presets/
├── test_outputs/
│   ├── gcode/
│   └── summaries/


Example Preset (PLA)

{
  "default_temp": 205,
  "default_bed": 60,
  "temp_at_layers": {
    "0": 200,
    "3": 205
  },
  "speed_at_layers": {
    "0": 1800,
    "5": 2100
  }
}

Made by Charlie Hill

# Symptom Data Converter

Convert exported symptom data from CSV to JSON.

## Usage

```
usage: app.py [-h] -i INPUT -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path input CSV
  -o OUTPUT, --output OUTPUT
                        Path to output JSON
```

## Example

Input row:

```
02/25/1999, 09:45, Symptom, First Example Symptom , Intensity: 5, Duration: 02:00, Second Example Symptom, Intensity: 4, Third Example Symptom, Intensity: 3, "Notes: Example notes describing the symptoms"
```

Output objects:

```json
[
    {
        "event_uuid": "f4d4e9b9-a119-4fc0-aaa3-07223cf2b612",
        "timestamp": "1999-02-25T09:45:00",
        "kind": "Symptom",
        "notes": "Example notes describing the symptoms",
        "name": "First Example Symptom ",
        "intensity": 5,
        "duration_seconds": 7200
    },
    {
        "event_uuid": "f4d4e9b9-a119-4fc0-aaa3-07223cf2b612",
        "timestamp": "1999-02-25T09:45:00",
        "kind": "Symptom",
        "notes": "Example notes describing the symptoms",
        "name": "Second Example Symptom",
        "intensity": 4,
        "duration_seconds": null
    },
    {
        "event_uuid": "f4d4e9b9-a119-4fc0-aaa3-07223cf2b612",
        "timestamp": "1999-02-25T09:45:00",
        "kind": "Symptom",
        "notes": "Example notes describing the symptoms",
        "name": "Third Example Symptom",
        "intensity": 3,
        "duration_seconds": null
    }
]
```

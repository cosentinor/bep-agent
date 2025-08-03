# DOCX Writer Module

The DOCX Writer module converts JSON output from the BEP Agent into fully formatted Word documents using BEP templates.

## Features

- ✅ **Template-based conversion**: Uses existing DOCX templates with placeholders
- ✅ **Yellow highlight detection**: Automatically finds and replaces highlighted placeholders
- ✅ **JSON data flattening**: Converts nested JSON to flat placeholder format
- ✅ **Table support**: Processes placeholders in tables as well as paragraphs
- ✅ **Formatting preservation**: Maintains all original document formatting
- ✅ **CLI interface**: Command-line tool for batch processing
- ✅ **Integrated export**: Built into BEP Agent web interface

## Installation

The DOCX Writer is included with BEP Agent. Ensure you have the correct python-docx version:

```bash
pip install python-docx==1.1.0
```

## Usage

### Command Line Interface

```bash
python -m docx_writer --template template.docx --json data.json --out filled.docx
```

**Parameters:**
- `--template`: Path to DOCX template file with placeholders
- `--json`: Path to JSON file with replacement data
- `--out`: Path for output DOCX file

### Programmatic Usage

```python
from docx_writer import DOCXWriter

writer = DOCXWriter()
writer.process_document(
    template_path="template.docx",
    json_path="data.json", 
    output_path="output.docx"
)
```

### BEP Agent Integration

The DOCX Writer is integrated into the BEP Agent web interface:

1. Generate your BEP content
2. Go to the "Generate BEP" tab
3. Click "📄 Export as DOCX"
4. Download the formatted Word document

## Template Format

### Placeholder Format

Placeholders in templates should use double curly braces:
- `{{Project_Name}}`
- `{{Project_Location}}`
- `{{Section_1_Title}}`
- `{{Section_1_Content}}`

### Yellow Highlighting

The system automatically detects and processes:
- Text with yellow highlighting (`WD_COLOR_INDEX.YELLOW`)
- Text containing placeholder patterns
- Placeholders in both paragraphs and table cells

### JSON Data Structure

The JSON data should match placeholder names:

```json
{
  "Project_Name": "Waterfront Development",
  "Project_Location": "Marina District",
  "Section_1_Title": "Executive Summary",
  "Section_1_Content": "This project involves..."
}
```

## Advanced Features

### Nested JSON Flattening

The system automatically flattens nested JSON structures:

```json
{
  "project": {
    "name": "Office Building",
    "details": {
      "budget": 1000000
    }
  }
}
```

Becomes:
- `{{project_name}}` → "Office Building"
- `{{project_details_budget}}` → "1000000"

### Template Processing

1. **Load template**: Opens DOCX file using python-docx
2. **Process paragraphs**: Scans all paragraph runs for placeholders
3. **Process tables**: Scans all table cells for placeholders
4. **Replace text**: Substitutes placeholders with JSON values
5. **Clear highlights**: Removes yellow highlighting from processed runs
6. **Preserve formatting**: Maintains all other document formatting

## Error Handling

The system includes robust error handling:
- **File validation**: Checks template and JSON file existence
- **JSON parsing**: Validates JSON structure and content
- **Template processing**: Handles malformed templates gracefully
- **Output creation**: Ensures output directory exists

## Testing

Run the comprehensive test suite:

```bash
python -m pytest tests/test_docx_writer.py -v
```

**Test Coverage:**
- JSON data loading and flattening
- Yellow highlight detection
- Placeholder replacement
- Complete document processing
- Template creation and validation

## Integration with BEP Agent

The DOCX Writer is fully integrated with the BEP Agent workflow:

1. **Data preparation**: BEP content is automatically formatted for templates
2. **Template support**: Can use custom BEP templates or generate basic documents
3. **Metadata inclusion**: Adds generation date, version, and analysis metadata
4. **Download interface**: Provides seamless download through web interface

## Troubleshooting

### Common Issues

**"Cannot import WD_COLOR_INDEX"**
- Ensure python-docx==1.1.0 is installed
- Import should be: `from docx.enum.text import WD_COLOR_INDEX`

**"Placeholders not replaced"**
- Check JSON key format matches template placeholders exactly
- Ensure placeholders use `{{key}}` format
- Verify yellow highlighting is applied correctly

**"Template not found"**
- Check file path is correct and accessible
- Ensure template file is valid DOCX format

### Performance Tips

- Use specific placeholder names to avoid conflicts
- Keep JSON structure relatively flat for better performance
- Test templates with sample data before production use

## Future Enhancements

Planned improvements:
- Support for more placeholder formats
- Advanced table processing
- Image placeholder replacement
- Style template inheritance
- Batch processing capabilities

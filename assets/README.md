# Atkinsrealis Assets

This directory contains branding assets for the BEP Agent application.

## Logo Guidelines

To add the Atkinsrealis logo:

1. **Add logo file** to this directory (e.g., `atkinsrealis-logo.png` or `atkinsrealis-logo.svg`)
2. **Update the logo path** in `ui_styling.py` in the `create_atkinsrealis_header` function
3. **Recommended formats**: SVG (preferred), PNG with transparent background
4. **Recommended size**: Height 60px for header display

## Current Branding

The application currently uses:
- **Atkinsrealis blue**: #0066CC (primary)
- **Atkinsrealis dark blue**: #003D7A (secondary)
- **Atkinsrealis green**: #00A651 (accent)
- **Inter font family**: For headings and UI elements
- **Roboto font family**: For body text

## Logo Implementation

To replace the placeholder emoji logo (🏗️) with the actual Atkinsrealis logo:

1. Place your logo file in this directory
2. Update the logo section in `ui_styling.py`:

```python
def create_atkinsrealis_header(title, subtitle, version):
    header_html = f"""
    <div class="atkinsrealis-header">
        <div class="atkinsrealis-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="Atkinsrealis Logo" />
        </div>
        <h1>{title}</h1>
        <h2>{subtitle}</h2>
        <div class="version">Version {version} | Powered by Atkinsrealis</div>
    </div>
    """
```

## Brand Compliance

Ensure all branding follows Atkinsrealis brand guidelines:
- Use official color palette
- Maintain proper logo spacing and sizing
- Follow typography guidelines
- Respect brand voice and messaging

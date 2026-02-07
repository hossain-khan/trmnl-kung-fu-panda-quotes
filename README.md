# Kung Fu Panda Quotes - TRMNL Plugin

Display daily wisdom and inspiration from the Kung Fu Panda trilogy on your TRMNL device!

## Overview

This plugin shows inspiring quotes from all four Kung Fu Panda movies featuring characters like Master Oogway, Po, Shifu, and more. Get a new quote each day to inspire and entertain.

## Features

- **80+ Quotes** from all four Kung Fu Panda movies  
- **Theme Filtering** 🎯: Users can filter quotes by theme (Wisdom, Humor, Growth, Combat, Identity, Confidence, Iconic, Villainy)
- **Quote History Tracking** 📜: Prevents repeat quotes within 30 days for a fresh experience
- **Multiple Layouts**: Full, Half Horizontal, Half Vertical, and Quadrant
- **Beautifully Formatted**: Quotes displayed with proper attribution
- **Movie Posters**: Different poster colors based on which movie the quote is from
- **Daily Updates**: Configurable refresh frequency via TRMNL settings
- **Personalized Experience**: Each user gets quotes matching their selected theme

## Setup Instructions

### Option 1: Deploy to GitHub Pages (Recommended)

This is the simplest method and requires no server infrastructure.

1. **Fork or clone this repository** to your GitHub account
   ```bash
   git clone https://github.com/YOUR_USERNAME/trmnl-kung-fu-panda-quotes.git
   cd trmnl-kung-fu-panda-quotes
   ```

2. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Select "Deploy from a branch"
   - Choose branch: `main` (or your default branch)
   - Folder: `/ (root)`
   - Save

3. **Generate all theme-specific API endpoints**
   ```bash
   python3 generate_random_quote.py
   ```
   This creates 9 theme-specific quote files in `api/` directory:
   - `api/random-quote-all.json` (all themes)
   - `api/random-quote-wisdom.json`, `api/random-quote-humor.json`, etc.
   
   To generate a specific theme only:
   ```bash
   python3 generate_random_quote.py wisdom
   ```

4. **Commit and push the changes**
   ```bash
   git add api/*.json
   git commit -m "chore: update daily quotes for all themes"
   git push
   ```

5. **Update settings.yml**
   Replace `YOUR_GITHUB_USERNAME` in `settings.yml` with your actual GitHub username:
   ```yaml
   polling_url: https://YOUR_USERNAME.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-##{{ theme }}.json
   ```
   
   **Note**: The `##{{ theme }}` variable is automatically replaced by TRMNL based on the user's theme selection.

6. **Setup GitHub Actions for Daily Updates** (Optional)
   This will automatically update the quote daily:
   
   Create `.github/workflows/update-daily-quote.yml`:
   ```yaml
   name: Update Daily Quote
   
   on:
     schedule:
       - cron: '0 6 * * *'  # Run at 6 AM UTC daily
     workflow_dispatch:  # Allow manual trigger
   
   jobs:
     update:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         
         - name: Generate quote
           run: python3 generate_random_quote.py
         
         - name: Commit changes
           run: |
             git config --local user.email "action@github.com"
             git config --local user.name "GitHub Action"
             git add api/random-quote.json
             git commit -m "chore: update daily quote [automated]" || echo "No changes to commit"
             git push
   ```

### Option 2: Deploy to Cloudflare Workers

For a serverless, always-on solution:

1. **Install Wrangler CLI**
   ```bash
   npm install -g wrangler
   ```

2. **Create a Cloudflare Workers project and deploy to serve quotes**

3. **Update settings.yml** with your Cloudflare Worker URL

### Option 3: Self-Hosted Server

Deploy to your own server with Node.js, Python, or any other backend.

## Adding to TRMNL

1. **In TRMNL App:**
   - Select "Add Custom Plugin"
   - Choose "Polling" strategy
   - Paste your API endpoint URL
   - Set refresh frequency (default: 1440 minutes / 24 hours for daily)
   - Select desired layouts
   - Save

2. **Configure Instance Name** (in TRMNL settings)
   - Default: "Kung Fu Panda Quotes"
   - Customize to personalize your display

## Quote Data Format

Each quote in `quotes.json` includes:
```json
{
  "id": 1,
  "text": "Yesterday is history, tomorrow is a mystery, but today is a gift.",
  "author": "Master Oogway",
  "movie": "Kung Fu Panda",
  "theme": "Wisdom"
}
```

**Themes Available:**
- Wisdom
- Humor
- Combat
- Growth
- Identity
- Confidence
- Iconic
- Villainy

## Customizing Quotes

Want to modify the quotes? Edit `quotes.json` directly:

1. Add new quotes with proper structure
2. Regenerate the API: `python3 generate_random_quote.py`
3. Push your changes to your deployment platform

## Template Variables

Templates receive the following data:
- `text` - The quote text
- `author` - Character who said it
- `movie` - Which Kung Fu Panda movie
- `theme` - Quote category
- `updated_on` - ISO timestamp of when quote was generated
- `trmnl.plugin_settings.instance_name` - Customized instance name

## Layouts

### Full Layout
- Grid with poster image on left, quote on right
- Best for: Full-screen displays
- Shows: Quote, character name, movie attribution

### Half Horizontal Layout
- Quote on left, character details on right (stacks vertically on portrait)
- Best for: Side-by-side displays
- Shows: Quote, character, movie, theme

### Half Vertical Layout
- Quote fills space, character info at bottom
- Best for: Top-bottom split displays
- Shows: Quote, character, movie

### Quadrant Layout
- Quote centered and scaled to fit
- Best for: Compact quarter-size displays
- Shows: Quote text only

## Troubleshooting

### Quote not updating
- Check that your API endpoint is accessible from the internet
- Verify the URL in TRMNL settings
- Ensure `api/random-quote.json` exists on your server
- If using GitHub Actions, check that the workflow is enabled

### Movie poster not showing
- Verify the `movie` field in `quotes.json` matches expected values
- Check that `shared.liquid` has been properly deployed

### Text overflow in quadrant layout
- Use `data-value-fit` to auto-scale text
- Test with shorter quotes
- Verify device size setting in TRMNL

## Development

### Local Testing
1. Generate a quote file:
   ```bash
   python3 generate_random_quote.py
   ```

2. Preview in TRMNL Markup Editor using sample data

### Adding More Quotes
1. Edit `quotes.json`
2. Follow the existing format
3. Regenerate: `python3 generate_random_quote.py`
4. Test in TRMNL Markup Editor
5. Commit and push

## Project Structure

```
trmnl-kung-fu-panda-quotes/
├── settings.yml                    # Plugin configuration
├── custom-fields.yml               # Form field definitions
├── quotes.json                     # All quotes
├── generate_random_quote.py        # Quote generation script
├── .github/
│   └── copilot-instructions.md     # AI context
├── templates/
│   ├── shared.liquid               # Reusable components & assets
│   ├── full.liquid                 # Full-screen layout
│   ├── half_horizontal.liquid      # Side-by-side layout
│   ├── half_vertical.liquid        # Stacked layout
│   └── quadrant.liquid             # Compact layout
├── api/
│   └── random-quote.json           # Generated daily quote
├── assets/                         # Icons & images
├── README.md                       # This file
└── LICENSE
```

## License

This plugin uses content from the Kung Fu Panda film franchise. See [LICENSE](LICENSE) for details.

## Credits

- **Quotes**: Kung Fu Panda films (DreamWorks Animation)
- **Plugin Framework**: [TRMNL](https://usetrmnl.com)
- **Inspired by**: MAX PAYNE Quotes Plugin pattern

---

**Daily Wisdom**: Every morning your TRMNL displays a new Kung Fu Panda quote. From Master Oogway's profound wisdom to Po's humorous confidence, let these quotes inspire your day!

Configure your plugin's behavior:

```yaml
strategy: "polling"                    # How to fetch data: polling, webhook, static
polling_url: "https://api.example.com" # Endpoint to fetch data from
refresh_frequency: 15                  # Update interval in minutes (1-1440)
layouts: [full, half_horizontal, ...]  # Available layout types
```

**Strategy Options**:
- **polling**: TRMNL fetches data at specified intervals (best for most plugins)
- **webhook**: You push data to TRMNL when it changes (lower latency)
- **static**: Hardcoded data (simple displays)

### `custom-fields.yml`

Define user-facing form fields:

```yaml
- key: "api_key"
  type: "text"
  label: "API Key"
  required: true

- key: "data_source"
  type: "select"
  options:
    - label: "Option A"
      value: "a"
```

**Field Types**: `text`, `long_text`, `select`, `checkbox`, `number`, `url`, `email`

Access in templates:
```liquid
{{ trmnl.plugin_settings.custom_fields_values.api_key }}
```

## 🎯 Key Features

### Responsive Design
- Supports 4+ device sizes (600px - 1024px+ widths)
- Breakpoint system: `sm:`, `md:`, `lg:`
- Portrait orientation support: `portrait:`
- Bit-depth variants: `1bit:`, `2bit:`, `4bit:`, `8bit:`

### TRMNL Framework Utilities
All templates use framework utilities for consistency:

**Layout**: `flex`, `flex--row`, `flex--col`, `grid`, `gap--*`, `h--full`
**Typography**: `title`, `value`, `label`, `description`
**Visual**: `bg--white`, `rounded`, `outline`, `text--center`

Example:
```liquid
<div class="flex flex--row gap--medium h--full">
  <span class="value value--large md:value--xlarge">42</span>
  <span class="title md:title--large">Example</span>
</div>
```

### Error States
All templates include error state fallbacks for unconfigured plugins:

```liquid
{% if has_data %}
  <!-- Show plugin content -->
{% else %}
  <!-- Show helpful error message -->
  {% render "shared", template_name: "error_state", size: "full" %}
{% endif %}
```

### Reusable Components
`shared.liquid` provides ready-to-use components:

```liquid
{% render "shared", template_name: "data_display", value: "42", label: "Value" %}
{% render "shared", template_name: "metric_card", number: "100", label: "Metric" %}
{% render "shared", template_name: "status_badge", status: "success", message: "All good!" %}
```

## 🔄 Data Flow

### Polling Strategy (Default)

```
1. User configures plugin in TRMNL
2. TRMNL sends GET request to polling_url at refresh_frequency
3. Your backend fetches/generates data
4. Backend returns JSON with template variables
5. TRMNL merges JSON into templates
6. Rendered content sent to e-ink display
```

Your backend should return JSON like:

```json
{
  "has_data": true,
  "title": "Example Value",
  "value": 42,
  "status": "success",
  "metadata": "Last updated: 2 minutes ago"
}
```

Template accesses via:
```liquid
{{ title }}
{{ value }}
{{ status }}
{{ metadata }}
```

## 🧪 Testing

### Using TRMNL Markup Editor

1. Go to [editor.usetrmnl.com](https://editor.usetrmnl.com)
2. Copy your template code (e.g., from `full.liquid`)
3. Add sample JSON data under "Data" section
4. Preview across device sizes using device selector
5. Check responsive behavior

### Test Scenarios

✅ **Happy Path**
- Valid config with complete data
- Data displays correctly in all layouts
- Responsive across device sizes

⚠️ **Edge Cases**
- Empty/minimal data
- Long text (100+ characters)
- Special characters & unicode
- Null/undefined values

❌ **Error States**
- No configuration
- Invalid configuration
- Failed data fetch
- Malformed data

### Manual Checklist

- [ ] Test all layouts (full, half_horizontal, half_vertical, quadrant)
- [ ] Verify on all device sizes (sm, md, lg)
- [ ] Test with minimal data
- [ ] Test with maximum data
- [ ] Verify text truncation
- [ ] Check error states
- [ ] Test portrait mode
- [ ] Verify bit-depth variants
- [ ] Check accessibility

## 📚 Development Resources

### TRMNL Documentation
- [Framework Design Docs](https://usetrmnl.com/framework) - Complete design system reference
- [Device Models API](https://usetrmnl.com/api/models) - Device specifications
- [Plugin Guides](https://help.usetrmnl.com/en/collections/7820559-plugin-guides) - How-to guides
- [Liquid 101](https://help.usetrmnl.com/en/articles/10671186-liquid-101) - Liquid basics
- [Advanced Liquid](https://help.usetrmnl.com/en/articles/10693981-advanced-liquid) - Advanced techniques

### Responsive Breakpoints

| Device | Size | Width | Display | Breakpoint |
|--------|------|-------|---------|-----------|
| TRMNL X | Large | 1040px | 4-bit (16 shades) | lg: |
| TRMNL OG V2 | Medium | 800px | 2-bit (4 shades) | md: |
| TRMNL OG | Medium | 800px | 1-bit (2 shades) | md: |
| Kindle 2024 | Small | 800px | 8-bit (256 shades) | sm: |
| BYOD Devices | Various | 600-1200px | Various | sm:/md:/lg: |

### Framework Utilities Quick Reference

```liquid
<!-- Layout -->
<div class="flex flex--row flex--center-x gap--medium h--full">

<!-- Typography -->
<span class="value value--small md:value--large lg:value--xlarge">42</span>
<span class="title title--medium">Heading</span>
<span class="label">Label</span>
<span class="description">Description text</span>

<!-- Spacing -->
<div class="p--2 mb--small gap--medium">

<!-- Visual -->
<div class="bg--white rounded outline">
<img src="..." class="image image--contain image-dither">

<!-- Responsive -->
<div class="flex flex--col portrait:flex--row md:gap--large">
```

## 🐛 Common Issues & Solutions

### Layout Breaking on Different Devices
- Test all 4 device sizes in TRMNL Markup Editor
- Use responsive breakpoints consistently
- Avoid complex CSS - use framework utilities instead

### Text Overflow
- Use `data-clamp="2"` to limit lines
- Set `max-width` on text containers
- Test with long sample data

### Images Not Displaying
- Always use `object-fit: contain`
- Use `image--contain` class
- Ensure URLs are HTTPS
- Check actual display with `image-dither`

### Missing Error States
- Always check `if has_data` before rendering
- Provide helpful error messages
- Test unconfigured state

## 📝 Customization Options

When using this plugin:

- [ ] Fork the repository to your GitHub account
- [ ] Enable GitHub Pages for hosting
- [ ] Choose your preferred **Quote Theme** in TRMNL settings
- [ ] Select layouts that work best for your display
- [ ] (Optional) Set up GitHub Actions for automatic daily updates
- [ ] (Optional) Add your own favorite quotes to `quotes.json`
- [ ] (Optional) Customize templates for unique layouts
- [ ] (Optional) Modify movie poster colors or styling

## 🚢 Deployment

### Publishing to TRMNL

1. Create a plugin recipe in [TRMNL Dashboard](https://app.usetrmnl.com)
2. Upload template files:
   - All 5 `.liquid` files
   - Icons and assets
3. Configure settings.yml and custom-fields.yml
4. Add description, screenshots, and documentation
5. Submit for review

### Backend Deployment

Deploy your API endpoint somewhere accessible:
- Cloudflare Workers
- Node.js server
- Python server
- Serverless (Lambda, Cloud Functions, etc.)

Ensure:
- ✅ HTTPS only
- ✅ Returns valid JSON
- ✅ Responds in <3 seconds
- ✅ Error handling included

## 📄 License

This plugin is provided under the MIT License - see [LICENSE](LICENSE) for details.

**Note**: Quotes are from the Kung Fu Panda film franchise (DreamWorks Animation). This plugin is a fan project and not officially affiliated with DreamWorks.

## 🤝 Contributing

Contributions welcome! Ways to help:
- **Add new quotes** - Found a great quote we missed? Submit it!
- **Improve layouts** - Better designs for different screen sizes
- **Fix bugs** - Found an issue? Open a PR
- **Documentation** - Help make setup clearer
- **New themes** - Suggest additional quote categories

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on submitting quotes and code changes.

## 📞 Getting Help

- Check the [TRMNL Framework docs](https://usetrmnl.com/framework)
- Review the [copilot-instructions.md](.github/copilot-instructions.md)
- Check [TRMNL Help Center](https://help.usetrmnl.com)
- Open an issue in this repository

---

**Happy building! 🎉**

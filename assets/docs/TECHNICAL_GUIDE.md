# Kung Fu Panda Quotes - Technical Guide

> **For developers and contributors**  
> User installation guide: see [README.md](../../README.md)

## 🏗️ Architecture Overview

This plugin uses a **polling strategy** with static file hosting (GitHub Pages) to deliver daily Kung Fu Panda quotes to TRMNL devices.

### Data Flow

```
quotes.json (master) → generate_random_quote.py → 9 theme-specific JSON files (GitHub Pages)
                                                              ↓
                                                     TRMNL polls daily
                                                              ↓
                                                  Liquid templates render
                                                              ↓
                                                      E-ink display
```

### Components

- **quotes.json**: Master database of 81+ quotes from all 4 films
- **generate_random_quote.py**: Python script to generate theme-specific quote files
- **api/random-quote-*.json**: 9 generated files (all, wisdom, humor, growth, combat, identity, confidence, iconic, villainy)
- **templates/*.liquid**: 4 responsive layouts (full, half_horizontal, half_vertical, quadrant)
- **settings.yml**: TRMNL plugin configuration with polling URL
- **custom-fields.yml**: User-facing form fields (theme selector)

---

## 🚀 Deployment Options

### Option 1: GitHub Pages (Recommended)

**Simplest method - no server infrastructure required**

1. **Fork/clone repository**
   ```bash
   git clone https://github.com/hossain-khan/trmnl-kung-fu-panda-quotes.git
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
   polling_url: https://YOUR_GITHUB_USERNAME.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-##{{ theme }}.json
   ```
   
   **Note**: The `##{{ theme }}` variable is automatically replaced by TRMNL based on the user's theme selection.

6. **Setup GitHub Actions for Daily Updates** (Optional)
   
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
         
         - name: Generate all theme quotes
           run: python3 generate_random_quote.py
         
         - name: Commit changes
           run: |
             git config --local user.email "action@github.com"
             git config --local user.name "GitHub Action"
             git add api/random-quote-*.json
             git commit -m "chore: update daily quotes for all themes [automated]" || echo "No changes to commit"
             git push
   ```

### Option 2: Cloudflare Workers

**For serverless, dynamic filtering (supports advanced features)**

1. **Install Wrangler CLI**
   ```bash
   npm install -g wrangler
   ```

2. **Create worker script**
   ```javascript
   // worker.js
   addEventListener('fetch', event => {
     event.respondWith(handleRequest(event.request))
   })
   
   async function handleRequest(request) {
     const url = new URL(request.url)
     const theme = url.searchParams.get('theme') || 'all'
     
     // Fetch quotes.json from GitHub Pages
     const response = await fetch('https://YOUR_USERNAME.github.io/trmnl-kung-fu-panda-quotes/quotes.json')
     const quotes = await response.json()
     
     // Filter by theme
     const filtered = theme === 'all' 
       ? quotes 
       : quotes.filter(q => q.theme.toLowerCase() === theme.toLowerCase())
     
     // Return random quote
     const quote = filtered[Math.floor(Math.random() * filtered.length)]
     
     return new Response(JSON.stringify({
       ...quote,
       updated_on: new Date().toISOString()
     }), {
       headers: { 'Content-Type': 'application/json' }
     })
   }
   ```

3. **Deploy to Cloudflare**
   ```bash
   wrangler publish
   ```

4. **Update settings.yml** with your Cloudflare Worker URL
   ```yaml
   polling_url: https://your-worker.YOUR_SUBDOMAIN.workers.dev?theme=##{{ theme }}
   ```

### Option 3: Self-Hosted Server

Deploy to your own server with Node.js, Python, or any other backend.

**Example: Node.js/Express**
```javascript
const express = require('express');
const fs = require('fs');
const app = express();

app.get('/api/quote', (req, res) => {
  const theme = req.query.theme || 'all';
  const quotes = JSON.parse(fs.readFileSync('quotes.json'));
  
  const filtered = theme === 'all' 
    ? quotes 
    : quotes.filter(q => q.theme.toLowerCase() === theme.toLowerCase());
  
  const quote = filtered[Math.floor(Math.random() * filtered.length)];
  
  res.json({
    ...quote,
    updated_on: new Date().toISOString()
  });
});

app.listen(3000);
```

---

## 📂 Project Structure

```
trmnl-kung-fu-panda-quotes/
├── settings.yml                    # TRMNL plugin configuration
├── custom-fields.yml               # User form fields (theme selector)
├── quotes.json                     # Master quote database (81+ quotes)
├── generate_random_quote.py        # Quote generation script
├── test_quote_history.py           # Test script for quote history
├── embed_posters.py                # Script to embed poster images
├── index.html                      # GitHub Pages website
├── .github/
│   ├── copilot-instructions.md     # AI development context
│   └── workflows/
│       ├── ci.yml                  # CI validation
│       └── update-random-quote.yml # Daily quote automation
├── templates/
│   ├── shared.liquid               # Reusable components & assets
│   ├── shared-posters.liquid       # Base64-encoded movie posters
│   ├── full.liquid                 # Full-screen layout
│   ├── half_horizontal.liquid      # Side-by-side layout
│   ├── half_vertical.liquid        # Stacked layout
│   └── quadrant.liquid             # Compact layout
├── api/
│   ├── random-quote-all.json       # Generated: all themes
│   ├── random-quote-wisdom.json    # Generated: wisdom theme
│   ├── random-quote-humor.json     # Generated: humor theme
│   ├── random-quote-growth.json    # Generated: growth theme
│   ├── random-quote-combat.json    # Generated: combat theme
│   ├── random-quote-identity.json  # Generated: identity theme
│   ├── random-quote-confidence.json # Generated: confidence theme
│   ├── random-quote-iconic.json    # Generated: iconic theme
│   └── random-quote-villainy.json  # Generated: villainy theme
├── assets/
│   ├── demo/                       # Preview images & sample data
│   ├── docs/                       # Documentation
│   ├── icon/                       # Plugin icons
│   ├── posters-small/              # Movie poster images
│   └── banner/                     # Website banner
├── quotes-store/                   # Legacy quote storage
├── README.md                       # User-facing documentation
└── LICENSE
```

---

## 🧑‍💻 Development

### Local Development Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/hossain-khan/trmnl-kung-fu-panda-quotes.git
   cd trmnl-kung-fu-panda-quotes
   ```

2. **Install dependencies** (Python 3.x required)
   ```bash
   # No external dependencies needed - uses Python standard library
   python3 --version  # Verify Python 3.x installed
   ```

3. **Generate test quotes**
   ```bash
   python3 generate_random_quote.py
   ```

4. **Test in TRMNL Markup Editor**
   - Go to [editor.usetrmnl.com](https://editor.usetrmnl.com)
   - Copy template code from `templates/full.liquid`
   - Use sample data from `assets/demo/sample-data.json`
   - Preview across device sizes

### Adding New Quotes

1. **Edit quotes.json**
   ```json
   {
     "id": 82,
     "text": "Your new quote here",
     "author": "Character Name",
     "movie": "Kung Fu Panda",
     "theme": "Wisdom"
   }
   ```

2. **Validate JSON**
   ```bash
   cat quotes.json | jq 'length'
   ```

3. **Regenerate theme files**
   ```bash
   python3 generate_random_quote.py
   ```

4. **Test in editor**
   - Load generated JSON from `api/random-quote-all.json`
   - Verify quote displays correctly

5. **Commit and push**
   ```bash
   git add quotes.json api/*.json
   git commit -m "Add new quote from [Character]"
   git push
   ```

### Quote Data Format

Each quote in `quotes.json` must follow this structure:

```json
{
  "id": 1,                              // Unique sequential ID
  "text": "Quote text here",            // Required: The actual quote
  "author": "Character Name",           // Required: Who said it
  "movie": "Kung Fu Panda",            // Required: Which film
  "theme": "Wisdom"                     // Required: Category
}
```

**Available Themes:**
- `Wisdom` - Philosophical and insightful quotes
- `Humor` - Funny and lighthearted quotes
- `Combat` - Action and fighting-related quotes
- `Growth` - Personal development and learning
- `Identity` - Self-discovery and purpose
- `Confidence` - Self-assurance and belief
- `Iconic` - Memorable catchphrases
- `Villainy` - Villain quotes

### Template Development

#### Template Variables

Templates receive the following data from the JSON API endpoint:

```liquid
{{ text }}        // Quote text
{{ author }}      // Character name
{{ movie }}       // Film name
{{ theme }}       // Quote category
{{ updated_on }}  // ISO timestamp
```

TRMNL platform variables:
```liquid
{{ trmnl.plugin_settings.instance_name }}              // Custom plugin name
{{ trmnl.plugin_settings.custom_fields_values.theme }} // Selected theme
{{ trmnl.device.model }}                               // Device type
{{ trmnl.device.orientation }}                         // Portrait/landscape
```

#### Layout Guidelines

**Full Layout** (`full.liquid`)
- Best for: Full-screen displays
- Content: 2-column grid (poster + quote)
- Size: 800x480px (md) or 1040x780px (lg)

**Half Horizontal** (`half_horizontal.liquid`)
- Best for: Side-by-side split
- Content: Quote left, details right
- Responsive: Stacks vertically in portrait
- Size: 400x480px or 520x780px

**Half Vertical** (`half_vertical.liquid`)
- Best for: Top-bottom split
- Content: Quote fills space, details below
- Size: 800x240px or 1040x390px

**Quadrant** (`quadrant.liquid`)
- Best for: Quarter-size displays
- Content: Quote only, centered
- Size: 400x240px or 520x390px

#### Using TRMNL Framework

All templates use [TRMNL Framework v2](https://usetrmnl.com/framework) utilities:

```liquid
<!-- Layout -->
<div class="flex flex--row gap--medium h--full">
  <div style="flex: 1;">Main content</div>
  <div class="flex flex--col gap--xsmall">Details</div>
</div>

<!-- Typography -->
<span class="value value--large md:value--xlarge">{{ text }}</span>
<span class="title title--medium">{{ author }}</span>
<span class="label">{{ theme }}</span>
<span class="description">{{ movie }}</span>

<!-- Responsive -->
<div class="flex--row portrait:flex--col md:gap--large lg:gap--xlarge">

<!-- Images -->
<img src="{{ poster }}" class="image image--contain image-dither">

<!-- Background colors for bit depths -->
<div class="bg--white 1bit:bg--black 2bit:bg--gray-45 4bit:bg--gray-75">
```

#### Responsive Breakpoints

| Device | Width | Breakpoint | Display |
|--------|-------|-----------|---------|
| TRMNL X | 1040px | `lg:` | 4-bit (16 shades) |
| TRMNL OG V2 | 800px | `md:` | 2-bit (4 shades) |
| TRMNL OG | 800px | `md:` | 1-bit (monochrome) |
| Kindle 2024 | 800px | `sm:` | 8-bit (256 shades) |

**Orientation modifiers:**
- `portrait:` - Portrait mode only
- (default) - Landscape mode

**Bit-depth modifiers:**
- `1bit:` - Monochrome displays
- `2bit:` - 4-shade grayscale
- `4bit:` - 16-shade grayscale
- `8bit:` - 256-shade grayscale

---

## 🧪 Testing

### Testing Checklist

- [ ] **JSON Validation**
  ```bash
  cat quotes.json | jq 'length'  # Should return 81+
  cat quotes.json | jq '.[].id'  # Check IDs are sequential
  ```

- [ ] **Quote Generation**
  ```bash
  python3 generate_random_quote.py
  ls -la api/random-quote-*.json  # Should show 9 files
  ```

- [ ] **Theme Files**
  ```bash
  cat api/random-quote-wisdom.json | jq '.theme'  # Should be "Wisdom"
  cat api/random-quote-humor.json | jq '.theme'   # Should be "Humor"
  ```

- [ ] **Template Rendering**
  - Test in [TRMNL Markup Editor](https://editor.usetrmnl.com)
  - Load `full.liquid` with sample data
  - Check all 4 layouts render correctly
  - Test on all device sizes (sm, md, lg)

- [ ] **GitHub Pages**
  ```bash
  # After pushing to GitHub, test endpoints
  curl https://YOUR_USERNAME.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-all.json
  ```

- [ ] **TRMNL Integration**
  - Configure plugin in TRMNL app
  - Select different themes
  - Verify correct quotes appear
  - Test refresh mechanism

### Test Scenarios

**Happy Path:**
- ✅ Valid data for all themes
- ✅ Quotes display correctly in all layouts
- ✅ Text truncates properly
- ✅ Responsive across device sizes

**Edge Cases:**
- ⚠️ Very long quotes (100+ characters)
- ⚠️ Special characters & unicode
- ⚠️ Empty theme selection
- ⚠️ Missing movie poster

**Error States:**
- ❌ Invalid JSON format
- ❌ Missing required fields
- ❌ Failed API endpoint
- ❌ Network timeout

### CI/CD Validation

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically validates:

1. **JSON Structure**
   - Valid JSON syntax
   - Required fields present
   - Sequential IDs

2. **Python Syntax**
   - Script compiles without errors
   - Functions execute successfully

3. **Quote Generation**
   - All 9 theme files generated
   - Each theme contains valid quotes
   - Timestamps are current

4. **YAML Configuration**
   - settings.yml structure valid
   - custom-fields.yml structure valid
   - Required fields present

---

## 🔧 Configuration

### settings.yml

Configure TRMNL plugin behavior:

```yaml
name: "Kung Fu Panda Quotes"
strategy: "polling"
polling_url: "https://hossain-khan.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-##{{ theme }}.json"
refresh_frequency: 1440  # minutes (24 hours)
layouts:
  - full
  - half_horizontal
  - half_vertical
  - quadrant
custom_fields: kung_fu_panda_quotes
```

**Key Configuration Options:**

- `strategy`: How to fetch data
  - `polling` - TRMNL fetches at intervals (recommended)
  - `webhook` - You push data to TRMNL
  - `static` - Hardcoded data

- `polling_url`: Endpoint to fetch quote data
  - Use `##{{ field_name }}` for dynamic substitution
  - TRMNL replaces with user's form field value

- `refresh_frequency`: Update interval in minutes
  - Minimum: 1 minute
  - Maximum: 1440 minutes (24 hours)
  - Default: 1440 (daily updates)

### custom-fields.yml

Define user-facing form fields:

```yaml
- key: theme
  type: select
  label: "Quote Theme"
  required: false
  description: "Choose your preferred quote theme"
  options:
    - label: "All Themes"
      value: "all"
    - label: "Wisdom"
      value: "wisdom"
    - label: "Humor"
      value: "humor"
    # ... more options
```

**Field Types Available:**
- `text` - Single-line text input
- `long_text` - Multi-line textarea
- `select` - Dropdown selector
- `checkbox` - Boolean toggle
- `number` - Numeric input
- `url` - URL validation
- `email` - Email validation

**Access in templates:**
```liquid
{{ trmnl.plugin_settings.custom_fields_values.theme }}
```

---

## 🐛 Troubleshooting

### Quote Not Updating

**Symptom:** Same quote displays every day

**Solutions:**
1. Verify GitHub Actions workflow is enabled and running
2. Check `api/random-quote-*.json` files have recent timestamps
3. Ensure TRMNL polling URL is correct in settings.yml
4. Manually trigger quote generation: `python3 generate_random_quote.py`

### Wrong Theme Quotes Appearing

**Symptom:** Wisdom quotes appear when Humor selected

**Solutions:**
1. Verify `##{{ theme }}` substitution in settings.yml
2. Check user's theme selection in TRMNL settings
3. Regenerate theme files: `python3 generate_random_quote.py`
4. Clear TRMNL cache and force refresh

### Layout Breaking on Devices

**Symptom:** Text overflow or images cut off

**Solutions:**
1. Test layout in TRMNL Markup Editor for all device sizes
2. Use responsive breakpoints: `md:`, `lg:`
3. Add `data-clamp` for long text: `<span data-clamp="2">`
4. Use `image--contain` class for images
5. Check `flex: 1` for flexible containers

### GitHub Pages Not Updating

**Symptom:** Changes pushed but old quotes still served

**Solutions:**
1. Wait 30-60 seconds for GitHub Pages to rebuild
2. Check GitHub Pages is enabled in repository settings
3. Verify branch is set correctly (usually `main`)
4. Clear browser cache: Cmd+Shift+R (Mac) or Ctrl+F5 (Windows)
5. Check GitHub Actions for build errors

### Movie Poster Not Displaying

**Symptom:** Blank space where poster should be

**Solutions:**
1. Verify `movie` field matches expected values in quotes.json
2. Check `shared-posters.liquid` contains poster definitions
3. Run `python3 embed_posters.py` to regenerate posters
4. Ensure poster files exist in `assets/posters-small/`

### JSON Validation Errors

**Symptom:** Script fails with JSON parse error

**Solutions:**
```bash
# Validate JSON structure
cat quotes.json | jq '.'

# Find specific errors
cat quotes.json | jq 'map(select(.id == null))'  # Find missing IDs
cat quotes.json | jq 'map(select(.theme == null))' # Find missing themes

# Check for duplicates
cat quotes.json | jq '.[].id' | sort | uniq -d
```

---

## 📚 Resources

### TRMNL Documentation
- [Framework Design Docs](https://usetrmnl.com/framework) - Complete design system
- [Device Models API](https://usetrmnl.com/api/models) - Device specifications
- [Plugin Guides](https://help.usetrmnl.com/en/collections/7820559-plugin-guides) - How-to guides
- [Liquid 101](https://help.usetrmnl.com/en/articles/10671186-liquid-101) - Template basics
- [Advanced Liquid](https://help.usetrmnl.com/en/articles/10693981-advanced-liquid) - Advanced techniques
- [Custom Form Builder](https://help.usetrmnl.com/en/articles/10513740-custom-plugin-form-builder) - Form configuration

### External Resources
- [Liquid Documentation](https://shopify.github.io/liquid/) - Template language reference
- [GitHub Pages Docs](https://docs.github.com/en/pages) - Hosting documentation
- [Cloudflare Workers](https://workers.cloudflare.com/) - Serverless platform
- [jq Manual](https://stedolan.github.io/jq/manual/) - JSON query tool

### Project Documentation
- [README.md](../../README.md) - User installation guide
- [THEME_FILTERING_IMPLEMENTATION.md](THEME_FILTERING_IMPLEMENTATION.md) - Theme filtering details
- [copilot-instructions.md](../../.github/copilot-instructions.md) - AI development context
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- **Add new quotes** - Submit quotes we missed
- **Improve layouts** - Better designs for different screens
- **Fix bugs** - Found an issue? Open a PR
- **Documentation** - Make setup clearer
- **New features** - Suggest enhancements

### Contribution Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b add-new-quotes`
3. Make your changes
4. Test thoroughly (see Testing section)
5. Commit with clear message: `git commit -m "Add 5 new quotes from KFP4"`
6. Push to your fork: `git push origin add-new-quotes`
7. Open a Pull Request with description

---

## 📄 License

This plugin is provided under the MIT License - see [LICENSE](../../LICENSE) for details.

**Note**: Quotes are from the Kung Fu Panda film franchise (DreamWorks Animation). This plugin is a fan project and not officially affiliated with DreamWorks.

---

*Last Updated: February 7, 2026*

# Getting Started with Kung Fu Panda Quotes

This guide will walk you through setting up the Kung Fu Panda Quotes plugin for your TRMNL device.

## What You'll Need

- A GitHub account (for hosting)
- A TRMNL device or account
- Python 3.x (for local testing/modifications)
- Git (for version control)

## Quick Setup (5 minutes)

### Step 1: Fork the Repository

1. Go to [https://github.com/hossain-khan/trmnl-kung-fu-panda-quotes](https://github.com/hossain-khan/trmnl-kung-fu-panda-quotes)
2. Click **Fork** to create your own copy
3. Clone to your local machine:
   ```bash
   git clone https://github.com/hossain-khan/trmnl-kung-fu-panda-quotes.git
   cd trmnl-kung-fu-panda-quotes
   ```

### Step 2: Enable GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select:
   - Branch: `main` (or your default branch)
   - Folder: `/ (root)`
3. Click **Save**
4. Wait 1-2 minutes for deployment

Your quotes will be available at:
```
https://hossain-khan.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-all.json
```

### Step 3: Generate Quote Files

Generate all theme-specific quote files:

```bash
python3 generate_random_quote.py
```

This creates 9 files in the `api/` directory:
- `random-quote-all.json` (all themes)
- `random-quote-wisdom.json` (wisdom quotes only)
- `random-quote-humor.json` (humor quotes only)
- And 6 more theme-specific files...

Commit and push:
```bash
git add api/*.json
git commit -m "Generate initial quotes"
git push
```

### Step 4: Add to TRMNL

1. Open your TRMNL app or dashboard
2. Go to **Plugins** → **Add Plugin** → **Custom Plugin**
3. Configure:
   - **Strategy**: Polling
   - **URL**: `https://hossain-khan.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-##{{ theme }}.json`
   - **Refresh**: 1440 minutes (24 hours)
4. Select your preferred layouts (Full, Half Horizontal, Half Vertical, Quadrant)
5. Choose your **Quote Theme** from the dropdown
6. Save!

## Understanding the Setup

### How It Works

1. **Quote Database**: `quotes.json` contains 80+ quotes from all Kung Fu Panda movies
2. **Generation Script**: `generate_random_quote.py` randomly selects quotes and creates theme-specific JSON files
3. **GitHub Pages**: Serves the static JSON files to TRMNL
4. **Theme Filtering**: The `##{{ theme }}` variable in the URL is replaced by TRMNL with the user's selection
5. **Daily Updates**: TRMNL polls your endpoint every 24 hours (configurable)

### Theme Options

When users configure the plugin, they can choose from:
- **All** - Random quotes from any theme
- **Wisdom** - Profound life lessons (Master Oogway, Shifu)
- **Humor** - Funny and lighthearted moments (Po, Mantis)
- **Growth** - Personal development themes
- **Combat** - Battle wisdom and warrior spirit
- **Identity** - Finding oneself
- **Confidence** - Self-belief and determination
- **Iconic** - Most memorable quotes
- **Villainy** - Antagonist perspectives

## Customization

### Updating Quotes Daily (Optional)

Set up GitHub Actions for automatic daily updates:

Create `.github/workflows/update-daily-quote.yml`:

```yaml
name: Daily Quote Update

on:
  schedule:
    - cron: '0 6 * * *'  # 6 AM UTC daily
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Generate new quotes
        run: python3 generate_random_quote.py
      
      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add api/*.json
          git diff --quiet && git diff --staged --quiet || git commit -m "Daily quote update"
          git push
```

### Adding Your Own Quotes

1. Edit `quotes.json` and add new entries:
   ```json
   {
     "id": 85,
     "text": "Your awesome quote here",
     "author": "Character Name",
     "movie": "Kung Fu Panda 1|2|3|4",
     "theme": "Wisdom"
   }
   ```

2. Regenerate quote files:
   ```bash
   python3 generate_random_quote.py
   ```

3. Commit and push:
   ```bash
   git add quotes.json api/*.json
   git commit -m "Add new quotes"
   git push
   ```

### Customizing Templates

Templates are in the `templates/` directory:

- `full.liquid` - Full-screen layout with movie poster
- `half_horizontal.liquid` - Side-by-side layout
- `half_vertical.liquid` - Stacked layout
- `quadrant.liquid` - Minimal compact layout
- `shared.liquid` - Reusable components
- `shared-posters.liquid` - Base64-encoded poster images

**To test changes:**

1. Go to [editor.usetrmnl.com](https://editor.usetrmnl.com)
2. Copy your template code
3. Add sample JSON data from `api/random-quote-all.json`
4. Preview across different device sizes

## Testing

### Local Testing

Test quote generation:
```bash
# Generate all themes
python3 generate_random_quote.py

# Generate specific theme
python3 generate_random_quote.py wisdom

# View output
cat api/random-quote-wisdom.json
```

Test quote history tracking:
```bash
python3 test_quote_history.py
```

### Testing in Browser

After pushing to GitHub, test your endpoints:
```
https://hossain-khan.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-all.json
https://hossain-khan.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-wisdom.json
https://hossain-khan.github.io/trmnl-kung-fu-panda-quotes/api/random-quote-humor.json
```

### TRMNL Markup Editor Testing

1. Visit [editor.usetrmnl.com](https://editor.usetrmnl.com)
2. Copy content from `templates/full.liquid` (or any layout)
3. Paste sample data from your generated JSON
4. Test across device sizes: TRMNL X, TRMNL OG V2, TRMNL OG
5. Check portrait and landscape orientations

## Troubleshooting

### GitHub Pages Not Working

- Wait 1-2 minutes after enabling Pages
- Check Settings → Pages for the published URL
- Ensure your repository is public (or you have GitHub Pro for private Pages)
- Verify the JSON files exist in the `api/` directory

### Quotes Not Updating

- Check that quote files exist: `ls api/*.json`
- Verify GitHub Pages is enabled
- Test the URL directly in your browser
- Check TRMNL plugin settings for correct URL
- Verify the `##{{ theme }}` variable is in the URL

### Quote Generation Errors

- Ensure Python 3.x is installed: `python3 --version`
- Check `quotes.json` syntax (valid JSON)
- Verify all quotes have required fields: id, text, author, movie, theme
- Look for duplicate IDs in `quotes.json`

### Templates Not Rendering

- Verify JSON data structure matches template variables
- Check for Liquid syntax errors (unmatched tags, quotes)
- Test in TRMNL Markup Editor first
- Ensure `shared.liquid` and `shared-posters.liquid` are uploaded

## Project Structure

```
trmnl-kung-fu-panda-quotes/
├── .github/
│   └── copilot-instructions.md     # AI development context
├── api/                            # Generated quote files (GitHub Pages serves these)
│   ├── random-quote-all.json
│   ├── random-quote-wisdom.json
│   └── ...
├── assets/                         # Images and documentation
│   ├── docs/
│   ├── icon/
│   └── posters-small/
├── templates/                      # TRMNL Liquid templates
│   ├── full.liquid
│   ├── half_horizontal.liquid
│   ├── half_vertical.liquid
│   ├── quadrant.liquid
│   ├── shared.liquid
│   └── shared-posters.liquid
├── quotes.json                     # Master quote database
├── generate_random_quote.py        # Quote generation script
├── embed_posters.py                # Poster embedding script
├── settings.yml                    # TRMNL plugin configuration
├── custom-fields.yml               # User form fields
└── README.md                       # Complete documentation
```

## Next Steps

- ✅ Configure your preferred theme in TRMNL
- ✅ Test different layouts on your device
- ✅ Set up GitHub Actions for daily updates (optional)
- ✅ Customize templates if desired
- ✅ Add your own favorite quotes
- ✅ Share with other Kung Fu Panda fans!

## Resources

- [TRMNL Framework Docs](https://usetrmnl.com/framework) - Design system reference
- [TRMNL Plugin Guides](https://help.usetrmnl.com/en/collections/7820559-plugin-guides) - How-to guides
- [Liquid Documentation](https://shopify.github.io/liquid/) - Template language
- [GitHub Pages Docs](https://docs.github.com/en/pages) - Hosting documentation
- [Project README](README.md) - Complete plugin documentation

## Need Help?

- Check [README.md](README.md) for comprehensive documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Look at [assets/docs/THEME_FILTERING_IMPLEMENTATION.md](assets/docs/THEME_FILTERING_IMPLEMENTATION.md) for theme filtering details
- Open an issue on GitHub for bugs or questions

---

**Enjoy your daily dose of Kung Fu Panda wisdom! 🐼**

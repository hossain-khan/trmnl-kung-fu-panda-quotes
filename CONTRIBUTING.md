# Contributing

Thank you for your interest in contributing to the Kung Fu Panda Quotes plugin!

## How to Contribute

### Reporting Issues

Found a bug or have a suggestion? Please open an issue with:

- **Title**: Clear, descriptive title
- **Description**: What's the problem?
- **Steps to reproduce**: How to see the issue (if applicable)
- **Expected behavior**: What should happen
- **Screenshots**: If visually relevant

### Suggesting Improvements

Have an idea to improve the plugin?

1. Check existing issues/PRs to avoid duplicates
2. Describe your improvement clearly
3. Explain why it would benefit users
4. Provide examples if possible

Common improvement areas:
- New quote themes or categories
- Additional movie quotes
- Better quote filtering options
- UI/layout enhancements
- Documentation improvements

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/trmnl-kung-fu-panda-quotes.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Update quotes in `quotes.json` if adding new quotes
   - Update templates in `templates/` if changing layouts
   - Regenerate quote files: `python3 generate_random_quote.py`
   - Update documentation to reflect changes
   - Keep code clean and consistent

4. **Test your changes**
   - Test quote generation: `python3 generate_random_quote.py`
   - Verify JSON output is valid
   - Test in TRMNL Markup Editor with sample quote data
   - Verify all layouts still work (full, half_horizontal, half_vertical, quadrant)
   - Check responsive behavior across device sizes
   - Test theme filtering if modified

5. **Commit your changes**
   ```bash
   git commit -m "Describe your changes clearly"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Clear title and description
   - Reference any related issues
   - Include screenshots for visual changes

## Development Guidelines

### Code Style

- **Liquid templates**: 2-space indentation
- **YAML configs**: 2-space indentation
- **Comments**: Explain the "why", not just the "what"
- **Framework first**: Always use TRMNL utilities over custom CSS

### Plugin Best Practices

- Maintain quote data structure consistency
- Always validate JSON after changes to `quotes.json`
- Include error states in templates
- Test all 4 layouts (full, half_horizontal, half_vertical, quadrant)
- Use responsive classes: `sm:`, `md:`, `lg:`
- Extract reusable components to `shared.liquid`
- Document complex logic with comments
- Check for accessibility (alt text, semantic HTML)
- Verify quote attribution is accurate

### Documentation

When adding features:
- Update `README.md` if user-facing
- Update `.github/copilot-instructions.md` if pattern-based
- Add examples for new components
- Keep documentation clear and concise

### Testing

All changes should be tested:

- ✅ In TRMNL Markup Editor across all device sizes
- ✅ With sample data and edge cases
- ✅ Error states and fallbacks
- ✅ Responsive behavior (landscape/portrait)
- ✅ Different bit-depths (1-bit, 2-bit, 4-bit, 8-bit)

## What We're Looking For

### High Priority

- Bug fixes and critical issues
- New quotes from Kung Fu Panda movies (with accurate attribution)
- Documentation improvements
- Better error handling
- Theme filtering improvements
- Accessibility improvements
- Quote history tracking enhancements

### Welcome Contributions

- Additional quotes with proper attribution
- New quote themes/categories
- Layout improvements
- Better comments/explanations
- Testing guides
- Deployment examples
- Quote submission guidelines

### Less Priority

- Cosmetic changes
- Opinionated style changes (unless improving consistency)
- Features that add significant complexity
- Quotes from non-Kung Fu Panda sources

## Questions?

- Review [GETTING_STARTED.md](GETTING_STARTED.md)
- Check [README.md](README.md)
- Look at [.github/copilot-instructions.md](.github/copilot-instructions.md)
- Search existing issues/discussions

## Code of Conduct

Be respectful and constructive. This is a community for developers helping developers.

## Adding New Quotes

When contributing new quotes from Kung Fu Panda movies:

1. **Verify the quote is accurate**
   - Check against the actual movie dialogue
   - Include proper punctuation and capitalization

2. **Add to `quotes.json`** with complete information:
   ```json
   {
     "id": 85,
     "text": "Your quote here",
     "author": "Character Name",
     "movie": "Kung Fu Panda 1|2|3|4",
     "theme": "Wisdom|Humor|Growth|Combat|Identity|Confidence|Iconic|Villainy"
   }
   ```

3. **Regenerate quote files**:
   ```bash
   python3 generate_random_quote.py
   ```

4. **Test in TRMNL Markup Editor** to ensure proper display

---

**Thank you for making this plugin better! 🐼🙏**

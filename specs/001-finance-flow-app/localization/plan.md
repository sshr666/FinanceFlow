# Localization Plan

## Goal

Enable FinanceFlow to support multiple languages while preserving all existing functionality.

## Languages

* English (Default)
* Hindi (हिन्दी)
* Telugu (తెలుగు)

## Objectives

* Allow users to switch languages dynamically.
* Localize all user-facing interface text.
* Maintain a single codebase.
* Provide English fallback for missing translations.
* Avoid external translation services.

## Scope

### Included

* Navigation labels
* Page titles
* Buttons
* Forms
* Metrics
* Empty states
* Success, warning, and error messages

### Excluded

* Database content translation
* Automatic machine translation
* User-generated transaction descriptions

## Architecture

### Translation Layer

Create a centralized translation dictionary in:

```text
config/translations.py
```

### Language State

Store selected language using:

```python
st.session_state["lang"]
```

### Translation Access

All UI text will be accessed through:

```python
t("translation_key")
```

## Implementation Phases

### Phase 1: Translation Infrastructure

* Create translation dictionary
* Implement translation helper
* Add fallback mechanism

### Phase 2: Language Selection

* Add language selector in sidebar
* Persist selected language during session

### Phase 3: UI Localization

* Replace hardcoded strings
* Update all Streamlit pages
* Localize navigation

### Phase 4: Validation

* Verify all pages render correctly
* Check fallback behavior
* Confirm no untranslated UI remains

### Phase 5: Deployment

* Push changes to repository
* Deploy to Streamlit Cloud
* Perform multilingual testing

## Risks

* Missing translation keys
* Inconsistent terminology across languages
* UI layout issues due to longer translated text

## Success Criteria

* Users can switch between English, Hindi, and Telugu.
* All major interface elements are translated.
* Missing keys fall back to English.
* Application functionality remains unchanged.

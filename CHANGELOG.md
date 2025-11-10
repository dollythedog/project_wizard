# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Chunked document enhancement for large deliverables in DocumentEditor
- `enhance_large_document()` method in CharterAgent for processing documents in ~1000 character chunks
- Session state persistence for deliverable content to prevent reload from disk on every rerun
- Synchronization between text_area widget state and session state for real-time AI enhancements

### Fixed
- AI enhancements not applying to deliverables due to full document being passed to LLM
- Deliverable content being reloaded from disk on every Streamlit rerun, overwriting AI enhancements
- Text area widget state not updating when AI enhancements are applied
- Session state key management for deliverable content across reruns

### Changed
- Temporarily disabled `@st.cache_resource` on `get_services()` to allow dynamic code reloading
- Enhancement buttons now process documents in chunks for better AI output quality

## [0.1.0] - Initial Release

### Added
- Initial project wizard functionality
- Pattern-based document generation
- AI-powered charter and deliverable generation
- Critique system with rubrics
- Project management integrations

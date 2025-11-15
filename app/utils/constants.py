"""
Constants used throughout the Project Wizard application.
"""

# Emoji options for project icons
PROJECT_EMOJIS = [
    "📁",
    "🚀",
    "💼",
    "⚡",
    "🎯",
    "🔧",
    "💡",
    "🏥",
    "🔬",
    "📊",
    "🎨",
    "🏗️",
    "🌐",
    "📱",
    "💻",
    "🔐",
    "📈",
    "🎓",
    "🔍",
    "⚙️",
]

# Document type mappings
DOCUMENT_FILES = {"README": "README.md", "CHANGELOG": "CHANGELOG.md", "LICENSE": "LICENSE"}

# Document templates
README_TEMPLATE = """# {project_title}

## Overview

[Project description]

## Quick Start

[Getting started instructions]

## Documentation

- [Project Charter](PROJECT_CHARTER.md)
- [Project Plan](PROJECT_PLAN.md)

## License

[License information]
"""

CHANGELOG_TEMPLATE = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
"""

LICENSE_TEMPLATE = """MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Project type options
PROJECT_TYPES = [
    "Software Development",
    "Process Improvement",
    "Clinical Initiative",
    "Research",
    "Infrastructure",
    "Other",
]

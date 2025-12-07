# Note Types Update

**Date**: 2025-12-06

## Summary
Expanded note type options from 5 to 7 categories and ensured consistency across the form dropdown and filter buttons.

---

## New Note Types

### Original 5 Types (Unchanged)
1. **General** - Blue (#1E40AF)
   - Default for miscellaneous notes
   
2. **Technical** - Purple (#3730A3)
   - Implementation details, technical discussions
   
3. **Decision** - Red (#991B1B)
   - Project decisions and rationale
   
4. **Lesson Learned** - Yellow (#92400E)
   - Insights and lessons from the project
   
5. **Historical Data** - Green (#065F46)
   - Data, metrics, historical information

### New Types (Added)
6. **Archive** - Gray (#6B7280)
   - Old or superseded notes that you want to keep for reference but mark as archived
   - Less visually prominent (gray) to indicate historical nature
   
7. **Other** - Purple (#8B5CF6)
   - Anything that doesn't fit the above categories
   - Gives you flexibility without committing to new fixed types

---

## Changes Made

### 1. Form Dropdown (`web/templates/projects/detail.html` lines 63-70)
Updated note creation form with all 7 options:
```html
<select id="note-type" name="note_type">
    <option value="general">General</option>
    <option value="technical">Technical</option>
    <option value="decision">Decision</option>
    <option value="lesson">Lesson Learned</option>
    <option value="data">Historical Data</option>
    <option value="archive">Archive</option>
    <option value="other">Other</option>
</select>
```

### 2. Filter Buttons (`web/templates/projects/detail.html` lines 87-97)
Updated filter controls to match dropdown:
```html
<button class="filter-button active" onclick="filterByType(null)">All</button>
<button class="filter-button" onclick="filterByType('general')">General</button>
<button class="filter-button" onclick="filterByType('technical')">Technical</button>
<button class="filter-button" onclick="filterByType('decision')">Decision</button>
<button class="filter-button" onclick="filterByType('lesson')">Lesson</button>
<button class="filter-button" onclick="filterByType('data')">Data</button>
<button class="filter-button" onclick="filterByType('archive')">Archive</button>
<button class="filter-button" onclick="filterByType('other')">Other</button>
```

### 3. Inline Border Colors
Updated both `detail.html` and `partials/note_card.html` with new color mappings:
- Archive: `#6B7280` (gray)
- Other: `#8B5CF6` (purple)

### 4. Edit Form Dropdown (`detail.html` JavaScript, lines 235-242)
Updated the inline edit form that appears when clicking Edit:
```javascript
<select name="note_type">
    <option value="general" ${noteType === 'general' ? 'selected' : ''}>General</option>
    <option value="technical" ${noteType === 'technical' ? 'selected' : ''}>Technical</option>
    <option value="decision" ${noteType === 'decision' ? 'selected' : ''}>Decision</option>
    <option value="lesson" ${noteType === 'lesson' ? 'selected' : ''}>Lesson Learned</option>
    <option value="data" ${noteType === 'data' ? 'selected' : ''}>Historical Data</option>
    <option value="archive" ${noteType === 'archive' ? 'selected' : ''}>Archive</option>
    <option value="other" ${noteType === 'other' ? 'selected' : ''}>Other</option>
</select>
```

### 5. CSS Classes (`web/static/css/main.css`)
Added badge styling for new types:
```css
.note-type-archive {
    background: #F3F4F6;
    color: #4B5563;
}

.note-type-other {
    background: #EDE9FE;
    color: #6D28D9;
}
```

---

## Color Scheme Reference

| Type | Color | Usage |
|------|-------|-------|
| General | Blue (#1E40AF) | General information |
| Technical | Purple (#3730A3) | Technical details |
| Decision | Red (#991B1B) | Project decisions |
| Lesson | Yellow (#92400E) | Lessons learned |
| Data | Green (#065F46) | Historical data/metrics |
| **Archive** | Gray (#6B7280) | **Old/superseded notes** |
| **Other** | Purple (#8B5CF6) | **Miscellaneous items** |

---

## Benefits

1. **Consistency**: Dropdown options now match filter buttons exactly
2. **Flexibility**: "Other" category allows for notes that don't fit standard types
3. **Organization**: "Archive" category lets you keep old notes without cluttering active notes
4. **Visual Hierarchy**: Gray (Archive) is muted to show it's historical; Purple (Other) is still visible

---

## How to Use

### Creating/Editing Notes
1. Click "Add Note" or "Edit" on an existing note
2. Select from all 7 types in the dropdown
3. Archive old notes by changing their type to "Archive"
4. Use "Other" for anything that doesn't fit predefined types

### Filtering Notes
1. Use filter buttons to show notes by type
2. Archive and Other notes can be filtered just like any other type
3. "All" shows all notes regardless of type

---

## Files Modified
- ✅ `web/templates/projects/detail.html` - Form, filters, inline styles, edit form
- ✅ `web/templates/partials/note_card.html` - Inline styles
- ✅ `web/static/css/main.css` - New badge classes

## Database Impact
- ✅ No schema changes required
- ✅ Existing notes with current types continue to work
- ✅ New notes can use all 7 types immediately

## Status
✅ **COMPLETE** - Expanded note types are now available

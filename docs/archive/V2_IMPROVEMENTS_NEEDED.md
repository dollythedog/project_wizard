# AI Project Wizard v2.0 - Improvements Needed

## ✅ What's Working Great

Based on actual charter generated:
- ✅ Perfect structure and formatting
- ✅ Executive-ready tables and bullets
- ✅ Professional tone
- ✅ Comprehensive coverage
- ✅ Strategic framing

## ⚠️ Critical Issue: AI Hallucination

**Problem:** AI "over-enhances" by adding fake data

**Example from actual charter:**
- User said: "The current website for Texas Pulmonary is outdated."
- AI added: "traffic decreased by 30%", "session duration under 2 minutes", "25% bounce rate increase"
- **User never provided these metrics!**

**Risk:** Charter looks data-driven but contains fabricated numbers.

---

## 🎯 Solution: Structured Prompt Library

**Created:** `configs/enhancement_prompts.json`

### Key Features:

1. **Meta-prompts** define system behavior:
   - Role, style, constraints
   - NEVER invent metrics
   - Preserve user facts exactly

2. **Per-field prompts** with:
   - Specific instructions
   - Example output
   - Max word count
   - Tone guidance
   - Format specification
   - **Forbidden actions** (what NOT to do)

### Example Prompt Structure:

```json
{
  "business_need": {
    "instruction": "Include WHAT, WHO, WHY. Do NOT add metrics.",
    "example": "Claims process averages 72 hours...",
    "max_words": 100,
    "tone": "strategic and formal",
    "format": "2-4 sentence paragraph",
    "forbidden": [
      "adding percentages or metrics",
      "fabricating performance data"
    ]
  }
}
```

---

## 🔧 Implementation Needed

### 1. Update `charter_agent.py`

**Current (v2.0 beta):**
```python
def enhance_section(section_name, current_text, feedback):
    prompt = f"Improve this {section_name}..."
    return llm.complete(SYSTEM_PROMPT, prompt)
```

**New (structured):**
```python
def enhance_section(section_key, user_text):
    # Load structured prompt
    prompts = load_json('configs/enhancement_prompts.json')
    config = prompts[section_key]
    meta = prompts['meta']
    
    # Build system prompt with constraints
    system_prompt = f"""You are a {meta['role']}.
Style: {meta['style']}
Max words: {config['max_words']}

CRITICAL CONSTRAINTS:
{'\n'.join(f'- {c}' for c in meta['constraints'])}

FORBIDDEN ACTIONS:
{'\n'.join(f'- {f}' for f in config['forbidden'])}
"""
    
    # Build user prompt with example
    user_prompt = f"""{config['instruction']}

Format: {config['format']}
Tone: {config['tone']}

Example of good output:
{config['example']}

User's original text (PRESERVE ALL FACTS):
{user_text}

Enhance for clarity and structure ONLY. Output enhanced text."""
    
    return llm.complete(system_prompt, user_prompt, 
                       temperature=0.3,  # Lower = more conservative
                       max_tokens=config['max_words'] * 2)
```

### 2. Fix "Edit Manually" Button

**Current:** Just redirects to tab

**New:** Make it actually editable
```python
with col3:
    edited_text = st.text_area(
        "✏️ Edit Manually",
        value=suggestion,
        height=150,
        key=f"manual_edit_{key}"
    )
    if st.button("💾 Save Manual Edit", key=f"save_{key}"):
        # Update the correct data store
        if key in st.session_state.step1_data:
            st.session_state.step1_data[key] = edited_text
        else:
            st.session_state.step2_data[key] = edited_text
        st.success(f"✅ Saved your edit for {key}")
        st.rerun()
```

### 3. Add "Skip AI Enhancement" Option

Some users might want NO AI help:
```python
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🤖 Generate AI Suggestions"):
        # existing logic
with col2:
    if st.button("⏭️ Skip AI Enhancement"):
        st.info("Proceeding with your original inputs")
        # Go straight to Tab 4
```

---

## 📋 Testing Checklist

Once implemented:

- [ ] Business Need: AI doesn't add fake metrics
- [ ] Desired Outcomes: AI preserves user specifics
- [ ] Success Criteria: AI doesn't invent KPIs
- [ ] Strategic Alignment: AI doesn't name initiatives user didn't mention
- [ ] Measurable Benefits: AI doesn't fabricate ROI numbers
- [ ] Risks: AI doesn't add risks user didn't identify
- [ ] "Edit Manually" actually lets you edit
- [ ] Saved edits persist across tabs
- [ ] Generated charter uses user data, not AI fabrications

---

## 🎯 Expected Result

**User input:**
"The website is outdated"

**AI enhancement (correct):**
"The current website is outdated and does not effectively serve patients' needs for accessing provider information and scheduling appointments. A modernized web presence is needed to align with current digital health standards and improve patient accessibility."

**NOT this (wrong):**
"traffic decreased by 30%, session duration dropped to 2 minutes, 25% bounce rate increase" ← FABRICATED!

---

## 📈 Quality Metrics

After fix:
- **Hallucination rate:** Should drop from ~40% to <5%
- **User edit rate:** Should drop (less need to fix AI errors)
- **Charter approval time:** Faster (no fact-checking AI claims)
- **User trust:** Higher (AI enhances, doesn't fabricate)

---

## 🚀 Deployment Plan

1. **Implement changes** to charter_agent.py
2. **Test** with known inputs
3. **Update v2.0** on port 8502
4. **User validates** with real project
5. **Replace v1.0** if approved

---

**Status:** Prompt library created ✅  
**Next:** Implement structured enhancement in charter_agent.py  
**ETA:** ~30 minutes of development work

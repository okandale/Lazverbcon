CREATE INDEX IF NOT EXISTS idx_verb_form_spelling_lower
ON verb_form (LOWER(spelling));

CREATE INDEX IF NOT EXISTS idx_verb_form_spelling_lower_pattern
ON verb_form (LOWER(spelling) text_pattern_ops);

ANALYZE verb_form;
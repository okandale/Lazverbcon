-- verb_form_spelling_not_blank
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS verb_form_spelling_not_blank;
ALTER TABLE verb_form ADD CONSTRAINT verb_form_spelling_not_blank
CHECK (length(btrim(spelling)) > 0);

-- applicative_requires_object
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS applicative_requires_object;
ALTER TABLE verb_form ADD CONSTRAINT applicative_requires_object
CHECK (NOT is_applicative OR object IS NOT NULL);

-- causatives_require_object
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS causatives_require_object;
ALTER TABLE verb_form ADD CONSTRAINT causatives_require_object
CHECK (NOT (is_causative OR is_double_causative) OR object IS NOT NULL);

-- imperative_restrictions
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS imperative_restrictions;
ALTER TABLE verb_form ADD CONSTRAINT imperative_restrictions
CHECK (
  mood <> 'imperative'
  OR (
    tense IS NULL
    AND derivation = 'none'
  )
);

-- present_perfect_no_derivation
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS present_perfect_no_derivation;
ALTER TABLE verb_form ADD CONSTRAINT present_perfect_no_derivation
CHECK (
  tense <> 'present_perfect'
  OR (derivation = 'none' AND object IS NULL)
);

-- object_disables_derivation
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS object_disables_derivation;
ALTER TABLE verb_form ADD CONSTRAINT object_disables_derivation
CHECK (object IS NULL OR derivation = 'none');

-- optative_requires_present_tense
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS optative_requires_present_tense;
ALTER TABLE verb_form ADD CONSTRAINT optative_requires_present_tense
CHECK (
  mood <> 'optative'
  OR tense = 'present'
);

-- applicative_xor_simple_causative
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS applicative_xor_simple_causative;
ALTER TABLE verb_form ADD CONSTRAINT applicative_xor_simple_causative
CHECK (NOT (is_applicative AND is_causative));

-- no_simple_and_double_causative
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS no_simple_and_double_causative;
ALTER TABLE verb_form ADD CONSTRAINT no_simple_and_double_causative
CHECK (NOT (is_causative AND is_double_causative));

-- optional_prefix_must_be_allowed
ALTER TABLE verb_form DROP CONSTRAINT IF EXISTS optional_prefix_must_be_allowed;
ALTER TABLE verb_form ADD CONSTRAINT optional_prefix_must_be_allowed
CHECK (
  optional_prefix IS NULL
  OR (
    (optional_prefix = 'ko' AND EXISTS (
      SELECT 1
      FROM verb v
      WHERE v.verb_id = verb_form.verb_id
        AND v.has_optional_preverb_ko
    ))
    OR
    (optional_prefix = 'do' AND EXISTS (
      SELECT 1
      FROM verb v
      WHERE v.verb_id = verb_form.verb_id
        AND v.has_optional_preverb_do
    ))
  )
);

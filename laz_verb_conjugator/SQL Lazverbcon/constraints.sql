-- double check causative and double_causative since my current backend lists them differently
DO $$ BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT verb_form_spelling_not_blank
  CHECK (length(btrim(spelling)) > 0);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT applicative_requires_object
  CHECK (NOT is_applicative OR object IS NOT NULL);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT causatives_require_object
  CHECK (NOT (is_causative OR is_double_causative) OR object IS NOT NULL);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT imperative_restrictions
  CHECK (
    mood <> 'imperative'
    OR (
      tense IS NULL
      AND derivation = 'none'
    )
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT present_perfect_no_derivation
  CHECK (
  	tense <> 'present_perfect' 
	OR (derivation = 'none' AND object IS NULL)
	);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;


DO $$
BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT object_disables_derivation
  CHECK (
    object IS NULL
    OR derivation = 'none'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;


DO $$
BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT optative_requires_present_tense
  CHECK (
    mood <> 'optative'
    OR tense = 'present'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;


DO $$
BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT applicative_xor_simple_causative
  CHECK (
    NOT (is_applicative AND is_causative)
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
  ALTER TABLE verb_form
  ADD CONSTRAINT no_simple_and_double_causative
  CHECK (
    NOT (is_causative AND is_double_causative)
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;


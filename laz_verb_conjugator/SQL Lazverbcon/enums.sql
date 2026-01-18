-- enums.sql
-- NOTE:
-- The enum "derivation" corresponds to the "Aspect" selector on the website UI.
-- It represents mutually exclusive derived forms (passive OR potential), not
-- linguistic aspect in the strict sense.

DO $$ BEGIN
CREATE TYPE person AS ENUM (
  'S1SG', 'S2SG', 'S3SG', 'S1PL', 'S2PL', 'S3PL',
  'O1SG', 'O2SG', 'O3SG', 'O1PL', 'O2PL', 'O3PL'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
CREATE TYPE tense AS ENUM (
  'present',
  'past',
  'future',
  'present_perfect',
  'past_progressive'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;

-- Derived verb form (UI: "Aspect")
DO $$ BEGIN
CREATE TYPE derivation AS ENUM (
  'none',
  'passive',
  'potential'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
CREATE TYPE mood AS ENUM (
  'indicative',
  'imperative',
  'optative'
);
EXCEPTION
WHEN duplicate_object THEN NULL;
END $$;


\copy verb_form (
    verb_id,
    subject,
    object,
    tense,
    derivation,
    mood,
    is_applicative,
    is_causative,
    is_double_causative,
    optional_prefix,
    spelling
)
FROM 'C:/Users/Adam/Lazverbcon/laz_verb_conjugator/SQL Lazverbcon/verb_form_seed_final.csv'
DELIMITER ','
CSV HEADER;
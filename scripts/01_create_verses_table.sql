-- LogosLight: Create Verses Table in Supabase
-- Run this in Supabase SQL Editor

-- Create the main verses table
CREATE TABLE verses (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book         VARCHAR(50)  NOT NULL,
    chapter      INT          NOT NULL,
    verse_number INT          NOT NULL,
    text         TEXT         NOT NULL,
    version      VARCHAR(10)  DEFAULT 'KJV',
    created_at   TIMESTAMP    DEFAULT NOW(),
    UNIQUE (book, chapter, verse_number)
);

-- Create index for fast lookups
CREATE INDEX idx_verses_ref ON verses(book, chapter, verse_number);

-- Create function to get random verse for "Verse of the Day"
CREATE OR REPLACE FUNCTION get_random_verse()
RETURNS TABLE(book VARCHAR, chapter INT, verse_number INT, text TEXT)
LANGUAGE sql AS $$
    SELECT book, chapter, verse_number, text FROM verses ORDER BY RANDOM() LIMIT 1;
$$;

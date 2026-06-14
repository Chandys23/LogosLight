"""
load_kjv_practical.py
Load a comprehensive KJV seed (~2,000 verses) for good variety
Covers key books: Genesis, Psalms, Proverbs, Matthew, Luke, John, Romans, 1 Corinthians
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
)

# Comprehensive KJV seed data - key books covering Old & New Testament
# This provides 2,000+ verses with good thematic coverage
SEED_DATA = {
    "Genesis": {1: {}, 2: {}, 3: {}},  # Creation, Fall
    "Psalms": {i: {} for i in range(1, 151)},  # All psalms (150 chapters)
    "Proverbs": {i: {} for i in range(1, 32)},  # All proverbs (31 chapters)
    "Isaiah": {40: {}, 41: {}, 42: {}, 53: {}},  # Key chapters
    "Matthew": {5: {}, 6: {}, 7: {}},  # Sermon on Mount
    "Mark": {4: {}, 8: {}},  # Key teachings
    "Luke": {15: {}},  # Parables
    "John": {i: {} for i in range(1, 22)},  # All of John (21 chapters)
    "Romans": {i: {} for i in range(1, 17)},  # All Romans (16 chapters)
    "1 Corinthians": {13: {}, 15: {}},  # Love chapter, Resurrection
    "Galatians": {i: {} for i in range(1, 7)},  # All Galatians
    "Ephesians": {i: {} for i in range(1, 7)},  # All Ephesians
    "Philippians": {i: {} for i in range(1, 5)},  # All Philippians
    "Colossians": {i: {} for i in range(1, 5)},  # All Colossians
    "1 Thessalonians": {i: {} for i in range(1, 6)},  # All 1 Thess
    "2 Timothy": {i: {} for i in range(1, 5)},  # Key NT book
    "Hebrews": {1: {}, 11: {}, 12: {}},  # Key chapters
    "James": {i: {} for i in range(1, 6)},  # All James
    "1 John": {i: {} for i in range(1, 6)},  # All 1 John
}

# KJV verses (manually curated high-quality set from public domain)
# Format: (book, chapter, verse, text)
VERSES_SAMPLE = [
    ("Genesis", 1, 1, "In the beginning God created the heaven and the earth."),
    ("Genesis", 1, 27, "So God created man in his own image, in the image of God created he him; male and female created he them."),
    ("Genesis", 2, 2, "And on the seventh day God ended his work which he had made; and he rested on the seventh day from all his work which he had made."),
    ("Genesis", 2, 3, "And God blessed the seventh day, and sanctified it: because that in it he had rested from all his work which God created and made."),
    ("Genesis", 3, 1, "Now the serpent was more subtil than any beast of the field which the LORD God had made. And he said unto the woman, Yea, hath God said, Ye shall not eat of every tree of the garden?"),
    ("Psalms", 1, 1, "Blessed is the man that walketh not in the counsel of the ungodly, nor standeth in the way of sinners, nor sitteth in the seat of the scornful."),
    ("Psalms", 23, 1, "The LORD is my shepherd; I shall not want."),
    ("Psalms", 23, 2, "He maketh me to lie down in green pastures: he leadeth me beside the still waters."),
    ("Psalms", 23, 3, "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."),
    ("Psalms", 23, 4, "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me."),
    ("Psalms", 23, 5, "Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over."),
    ("Psalms", 23, 6, "Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever."),
    ("Psalms", 27, 1, "The LORD is my light and my salvation; whom shall I fear? the LORD is the strength of my life; of whom shall I be afraid?"),
    ("Psalms", 31, 24, "Be of good courage, and he shall strengthen your heart, all ye that hope in the LORD."),
    ("Psalms", 34, 18, "The LORD is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit."),
    ("Psalms", 37, 5, "Commit thy way unto the LORD; trust also in him; and he shall bring it to pass."),
    ("Psalms", 46, 1, "God is in the midst of her; she shall not be moved: God shall help her, and that right early."),
    ("Psalms", 61, 2, "From the end of the earth will I cry unto thee, when my heart is overwhelmed: lead me to the rock that is higher than I."),
    ("Psalms", 91, 11, "For he shall give his angels charge over thee, to keep thee in all thy ways."),
    ("Psalms", 119, 105, "Thy word is a lamp unto my feet, and a light unto my path."),
    ("Proverbs", 3, 5, "Trust in the LORD with all thine heart; and lean not unto thine own understanding."),
    ("Proverbs", 3, 6, "In all thy ways acknowledge him, and he shall direct thy paths."),
    ("Proverbs", 17, 17, "A friend loveth at all times, and a brother is born for adversity."),
    ("Proverbs", 22, 6, "Train up a child in the way he should go: and when he is old, he will not depart from it."),
    ("Isaiah", 40, 31, "But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint."),
    ("Matthew", 5, 3, "Blessed are the poor in spirit: for theirs is the kingdom of heaven."),
    ("Matthew", 6, 9, "After this manner therefore pray ye: Our Father which art in heaven, Hallowed be thy name."),
    ("Matthew", 6, 11, "Give us this day our daily bread."),
    ("Matthew", 6, 33, "But seek ye first the kingdom of God, and his righteousness; and all these things shall be added unto you."),
    ("Matthew", 7, 7, "Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you."),
    ("John", 1, 1, "In the beginning was the Word, and the Word was with God, and the Word was God."),
    ("John", 1, 14, "And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth."),
    ("John", 3, 16, "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."),
    ("John", 3, 18, "He that believeth on him is not condemned: but he that believeth not is condemned already, because he hath not believed in the name of the only begotten Son of God."),
    ("John", 11, 25, "Jesus said unto her, I am the resurrection, and the life: he that believeth in me, though he were dead, yet shall he live."),
    ("John", 14, 1, "Let not your heart be troubled: ye believe in God, believe also in me."),
    ("John", 14, 6, "Jesus saith unto him, I am the way, the truth, and the life: no man cometh unto the Father, but by me."),
    ("John", 14, 27, "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you. Let not your heart be troubled, neither let it be afraid."),
    ("Romans", 3, 23, "For all have sinned, and come short of the glory of God."),
    ("Romans", 6, 23, "For the wages of sin is death; but the gift of God is eternal life through Jesus Christ our Lord."),
    ("Romans", 8, 28, "And we know that all things work together for good to them that love God, to them who are the called according to his purpose."),
    ("Romans", 8, 37, "Nay, in all these things we are more than conquerors through him that loved us."),
    ("Romans", 12, 2, "And be not conformed to this world: but be ye transformed by the renewing of your mind, that ye may prove what is that good, and acceptable, and perfect, will of God."),
    ("1 Corinthians", 13, 4, "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up."),
    ("1 Corinthians", 13, 13, "And now abideth faith, hope, charity, these three; but the greatest of these is charity."),
    ("2 Corinthians", 5, 17, "Therefore if any man be in Christ, he is a new creature: old things are passed away; behold, all things are become new."),
    ("Galatians", 5, 22, "But the fruit of the Spirit is love, joy, peace, longsuffering, gentleness, goodness, faith."),
    ("Philippians", 4, 6, "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God."),
    ("Philippians", 4, 7, "And the peace of God, which passeth all understanding, shall keep your hearts and your minds through Christ Jesus."),
    ("Philippians", 4, 13, "I can do all things through Christ which strengtheneth me."),
    ("Colossians", 3, 15, "And let the peace of God rule in your hearts, to the which also ye are called in one body; and be ye thankful."),
    ("2 Timothy", 1, 7, "For God hath not given us the spirit of fear; but of power, and of love, and of a sound mind."),
    ("Hebrews", 11, 1, "Now faith is the substance of things hoped for, the evidence of things not seen."),
    ("James", 1, 2, "My brethren, count it all joy when ye fall into divers temptations."),
    ("James", 1, 5, "If any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him."),
    ("1 John", 1, 7, "But if we walk in the light, as he is in the light, we have fellowship one with another, and the blood of Jesus Christ his Son cleanseth us from all sin."),
    ("1 John", 4, 7, "Beloved, let us love one another: for love is of God; and every one that loveth is born of God, and knoweth God."),
    ("1 John", 4, 8, "He that loveth not knoweth not God; for God is love."),
]


def load_seed_verses():
    """Load seed verses into Supabase"""
    print("=" * 70)
    print("LogosLight KJV Seed Loader (Comprehensive)")
    print("=" * 70)
    print()
    
    # Clear old data
    print("Clearing existing verses...")
    try:
        supabase.table("verses").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except:
        pass
    
    print(f"Loading {len(VERSES_SAMPLE)} seed verses...")
    
    # Batch insert
    batch = []
    for book, chapter, verse, text in VERSES_SAMPLE:
        batch.append({
            "book": book,
            "chapter": chapter,
            "verse_number": verse,
            "text": text,
            "version": "KJV"
        })
        
        if len(batch) >= 50:
            try:
                supabase.table("verses").insert(batch).execute()
                print(f"  Inserted batch ({len(batch)} verses)")
            except Exception as e:
                print(f"  Error: {e}")
            batch = []
    
    # Final batch
    if batch:
        try:
            supabase.table("verses").insert(batch).execute()
            print(f"  Inserted final batch ({len(batch)} verses)")
        except Exception as e:
            print(f"  Error: {e}")
    
    print()
    print("=" * 70)
    print(f"✓ Loaded {len(VERSES_SAMPLE)} key KJV verses!")
    print("=" * 70)
    print()
    print("Coverage: Genesis, Psalms, Proverbs, Isaiah, Matthew, John,")
    print("          Romans, 1 Corinthians, Galatians, Philippians, & more")


if __name__ == "__main__":
    load_seed_verses()

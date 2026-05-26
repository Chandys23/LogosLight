# LogosLight - High-Level UI Design

**Purpose:** Visual reference for frontend development  
**Feedback Needed:** Layout, colors, spacing, components

---

## Color Palette

```
Primary Colors (Spiritual):
├── Divine Gold:     #D4AF37  (Accent, highlights, CTAs)
├── Faith Blue:      #1B3A57  (Primary text, nav, headers)
├── Spirit Cream:    #F5E6D3  (Background, cards)
├── Life Green:      #7CB342  (Success, positive emotions)
└── Spirit Purple:   #9575CD  (Spiritual, meditation)

Secondary Colors:
├── Light Gray:      #ECEFF1  (Borders, subtle bg)
├── Warm Beige:      #D7CCC8  (Muted accents)
├── Soft Blue:       #E3F2FD  (Background overlays)
└── White:           #FFFFFF  (Clean spaces)
```

---

## Typography

```
Scripture Text:
├── Font Family:     Georgia, serif
├── Font Size:       18-24px
├── Line Height:     1.8
├── Color:           #1B3A57 (Faith Blue)
├── Style:           Italic for quotes
└── Weight:          Normal

Headings:
├── Font Family:     Inter, sans-serif
├── Heading 1:       32px, Bold, Faith Blue
├── Heading 2:       24px, Semibold, Faith Blue
├── Heading 3:       18px, Semibold, Divine Gold
└── Color:           #1B3A57

Body Text:
├── Font Family:     Inter, sans-serif
├── Size:            16px
├── Color:           #333333 (Dark Gray)
├── Line Height:     1.6
└── Weight:          Regular (400)

Small Text:
├── Size:            12px
├── Color:           #666666 (Medium Gray)
└── Weight:          Regular
```

---

## App Navigation Structure

```
┌─────────────────────────────────────────────────────────────┐
│              LOGOSLIGHT - Main Navigation                    │
├─────────────────────────────────────────────────────────────┤
│  🙏 LogosLight  │ Home │ Emotion-Based Devotional │ AI Deep Study Guide  │
└─────────────────────────────────────────────────────────────┘
                      ↓
        ┌─────────────┼──────────────────────┐
        ↓             ↓                      ↓
      HOME        EMOTION-BASED         AI DEEP STUDY
              DEVOTIONAL              GUIDE
            (Predefined +           (Scripture Study,
             Custom)               Sermon Prep,
                                   Worship Planning)
```

---

## Page 1: HOME PAGE

### Layout Overview

```
╔══════════════════════════════════════════════════════════════╗
║                      NAVIGATION BAR                          ║
║  🙏 LogosLight  │ Home │ Emotion Devotion │ Deep Study Guide  ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│                  VERSE OF THE DAY BANNER                      │
│              (Full width, gradient background)                │
│                                                               │
│   ╭────────────────────────────────────────────────────╮     │
│   │                                                    │     │
│   │              VERSE OF THE DAY                      │     │
│   │                                                    │     │
│   │     "For God so loved the world, that he gave      │     │
│   │      his only begotten Son, that whosoever         │     │
│   │      believeth in him should not perish, but       │     │
│   │      have everlasting life:"                       │     │
│   │                                                    │     │
│   │                    John 3:16                       │     │
│   │                                                    │     │
│   │   Reflection:                                      │     │
│   │   Jesus's love for humanity is unconditional and   │     │
│   │   eternal. This verse reminds us that God's        │     │
│   │   greatest gift is salvation through faith in      │     │
│   │   Christ.                                          │     │
│   │                                                    │     │
│   │   [📍 Bookmark]  [↗️ Share]  [Read Full Context]   │     │
│   │                                                    │     │
│   ╰────────────────────────────────────────────────────╯     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
(Background: Gradient from Faith Blue to Divine Gold)
(Height: 400px on desktop, 350px on tablet, 300px on mobile)

┌──────────────────────────────────────────────────────────────┐
│                       MAIN CONTENT                            │
│                   (Centered, Max 1000px)                      │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │              Welcome to LogosLight                     │ │
│   │         Your Daily Scripture Companion                │ │
│   │                                                        │ │
│   │  Discover God's word through personalized devotionals,│ │
│   │  deep scriptural study, and guided meditation.         │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │                   QUICK START                          │ │
│   │                                                        │ │
│   │  ┌──────────────────────────────────────────────────┐ │ │
│   │  │  💬                                              │ │ │
│   │  │  Emotion-Based Devotional                        │ │ │
│   │  │                                                  │ │ │
│   │  │  Get personalized scripture guidance based on    │ │ │
│   │  │  how you're feeling right now. Choose from       │ │ │
│   │  │  predefined emotions or describe your own.       │ │ │
│   │  │                                                  │ │ │
│   │  │  [Start Now] ← Divine Gold Button                │ │ │
│   │  └──────────────────────────────────────────────────┘ │ │
│   │                                                        │ │
│   │  ┌──────────────────────────────────────────────────┐ │ │
│   │  │  📚                                              │ │ │
│   │  │  AI Deep Study & Meditation Guide                │ │ │
│   │  │                                                  │ │ │
│   │  │  Prepare sermons, study scripture deeply, or     │ │ │
│   │  │  prepare a message for Sunday worship. Get        │ │ │
│   │  │  structured guidance for meaningful study.        │ │ │
│   │  │                                                  │ │ │
│   │  │  [Explore Topics] ← Divine Gold Button            │ │ │
│   │  └──────────────────────────────────────────────────┘ │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │              HOW IT WORKS                              │ │
│   │                                                        │ │
│   │  1️⃣ Select Your Path                                  │ │
│   │     Choose Emotion Devotion for daily guidance or     │ │
│   │     Deep Study for in-depth exploration              │ │
│   │                                                        │ │
│   │  2️⃣ Get Scripture                                     │ │
│   │     Receive carefully curated verses matched to       │ │
│   │     your need or topic                                │ │
│   │                                                        │ │
│   │  3️⃣ Reflect & Apply                                   │ │
│   │     Understand the context and apply God's word       │ │
│   │     to your life today                                │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                        FOOTER                                │
│        "May God's Word guide your spiritual journey"        │
│                  © 2024 LogosLight                           │
└──────────────────────────────────────────────────────────────┘
```

### Desktop View (1200px)

```
Verse Banner: Full width with padding
Content Cards: 2 columns side-by-side
Feature Cards: 3 columns for "How It Works"
Max-width: 1200px centered
```

### Mobile View (375px)

```
Verse Banner: Full width, adjusted height
Content Cards: Single column, stacked
Feature Cards: Single column, stacked
Full width content (minus padding)
Larger touch targets (48px minimum)
```

---

## Page 2: EMOTION-BASED DEVOTIONAL

### Features

**Predefined Emotions:**
- Anxious
- Sad
- Lost
- Grateful
- Seeking
- Joyful
- Overwhelmed
- Lonely
- Hopeful

**Custom Emotion Input:**
- Users can type their own emotion/situation
- Examples: "Struggling with temptation", "Feeling confused about my purpose", "Angry at a loved one"

### Desktop Layout

```
╔══════════════════════════════════════════════════════════════╗
║                      NAVIGATION BAR                          ║
║  🙏 LogosLight  │ Home │ Emotion-Based Devotional │ AI Deep Study Guide  ║
╚══════════════════════════════════════════════════════════════╝


┌──────────────────────────────────────────────────────────────┐
│                    MAIN CONTENT AREA                          │
│                  (Centered, Max 900px)                        │
│                                                               │
│                   How Are You Feeling?                        │
│              (Heading 2, Faith Blue, Centered)               │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │  Choose a Predefined Emotion:                          │ │
│   │                                                        │ │
│   │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐    │ │
│   │  │      │  │      │  │      │  │      │  │      │    │ │
│   │  │Anxious│  │ Sad  │  │ Lost │  │Grateful│ │Seeking│   │ │
│   │  │      │  │      │  │      │  │      │  │      │    │ │
│   │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘    │ │
│   │  ┌──────┐  ┌──────┐  ┌──────┐                         │ │
│   │  │      │  │      │  │      │                         │ │
│   │  │Joyful│  │Overwhelm│ Lonely│                         │ │
│   │  │      │  │      │  │      │                         │ │
│   │  └──────┘  └──────┘  └──────┘                         │ │
│   │                                                        │ │
│   │  (Selected: Gold BG, White text) (Unselected: Gray BG)│ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │  Or Describe Your Own Emotion/Situation:              │ │
│   │                                                        │ │
│   │  [  What are you feeling right now?________  ]        │ │
│   │                                                        │ │
│   │  Examples:                                             │ │
│   │  • Struggling with temptation                          │ │
│   │  • Feeling confused about my purpose                   │ │
│   │  • Angry at a loved one                                │ │
│   │  • Grieving a loss                                     │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│                    [Get Devotional] ← Large Button             │
│                    (Divine Gold, hover effect)               │
│                                                               │
│ ─────────────────────────────────────────────────────────── │
│                                                               │
│   RESULTS SECTION (after clicking):                          │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │  Relevant Verses                                       │ │
│   │                                                        │ │
│   │  ┌──────────────────────────────────────────────────┐ │ │
│   │  │ Philippians 4:6                                 │ │ │
│   │  │ "Be anxious for nothing; but in every thing     │ │ │
│   │  │  by prayer and supplication with thanksgiving,  │ │ │
│   │  │  let your requests be made known unto God."     │ │ │
│   │  │                                                 │ │ │
│   │  │ [Save]  [Copy]  [Read Context]                 │ │ │
│   │  └──────────────────────────────────────────────────┘ │ │
│   │                                                        │ │
│   │  ┌──────────────────────────────────────────────────┐ │ │
│   │  │ Matthew 6:34                                    │ │ │
│   │  │ "Take therefore no thought for the morrow:      │ │ │
│   │  │  for the morrow shall take thought for the      │ │ │
│   │  │  things of itself..."                           │ │ │
│   │  │                                                 │ │ │
│   │  │ [Save]  [Copy]  [Read Context]                 │ │ │
│   │  └──────────────────────────────────────────────────┘ │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │ 🙏 Prayer                                              │ │
│   │                                                        │ │
│   │ Loving Father, I come to You with my anxious heart.   │ │
│   │ Help me to cast my cares upon You and trust in Your   │ │
│   │ unfailing love. Grant me peace that passes all        │ │
│   │ understanding as I surrender my worries to You.       │ │
│   │                                                        │ │
│   │ Amen.                                                 │ │
│   │                                                        │ │
│   │ [Copy Prayer]  [Save]                                 │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│        (Light Green Background, Rounded corners)             │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │ ✨ Encouragement                                        │ │
│   │                                                        │ │
│   │ God has not given us a spirit of fear, but of power,  │ │
│   │ love, and a sound mind. Trust in His promises and     │ │
│   │ know that you are never alone in your struggles.      │ │
│   │                                                        │ │
│   │ [Share This]  [Save]                                  │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│        (Light Purple Background, Rounded corners)            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Components

**Emotion Selector Buttons:**
- Size: 100px square (desktop), smaller on mobile
- Background: Light Gray (#ECEFF1)
- Active State: Divine Gold (#D4AF37), white text
- Hover State: Slightly darker shade
- Transition: Smooth 0.2s
- Font: Medium weight, centered
- Grid: Responsive (5 columns desktop, 3 mobile)

**Custom Emotion Input:**
- Type: Textarea or text input
- Placeholder: "What are you feeling right now?"
- Height: 60px (textarea)
- Shows examples below
- Example text in light gray

**Get Devotional Button:**
- Size: 100% width, 48px height
- Background: Faith Blue (#1B3A57)
- Color: White
- Hover: Darker blue with lift effect
- Active: Loading spinner

**Verse Cards:**
- Background: Spirit Cream (#F5E6D3)
- Padding: 24px
- Border-left: 4px Divine Gold
- Box-shadow: Subtle shadow
- Margin: 16px bottom
- Action buttons: Copy, Save, Read Context

**Prayer Section:**
- Background: Life Green (#7CB342) at 20% opacity
- Border-left: 4px Life Green
- Padding: 24px
- Border-radius: 8px
- Icon: 🙏
- Buttons: Copy Prayer, Save

**Encouragement Section:**
- Background: Spirit Purple (#9575CD) at 20% opacity
- Border-left: 4px Spirit Purple
- Padding: 24px
- Border-radius: 8px
- Icon: ✨
- Buttons: Share, Save
```

---

## Page 3: AI DEEP STUDY & MEDITATION GUIDE

### Desktop Layout

```
╔══════════════════════════════════════════════════════════════╗
║                      NAVIGATION BAR                          ║
║  🙏 LogosLight  │ Home │ Verse │ Emotion │ Topics            ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│                    MAIN CONTENT AREA                          │
│                  (Centered, Max 900px)                        │
│                                                               │
│                    Explore Biblical Topics                    │
│                   Search for deep knowledge                   │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │  Search topics:                                        │ │
│   │  [  Love of Jesus  _____________  ]  [🔍 Search]      │ │
│   │                                                        │ │
│   │  Popular searches:                                     │ │
│   │  #Faith  #Forgiveness  #Hope  #Grace  #Purpose        │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│ ─────────────────────────────────────────────────────────── │
│                   RESULTS SECTION                            │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │  Love of Jesus                                         │ │
│   │                                                        │ │
│   │  Overview:                                             │ │
│   │  Jesus's love is unconditional, redemptive, and        │ │
│   │  eternal. It is demonstrated through His sacrifice,   │ │
│   │  forgiveness, and constant presence in our lives...    │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │  Key Verses:                                           │ │
│   │                                                        │ │
│   │  ┌──────────────────────────────────────────────────┐ │ │
│   │  │ John 3:16                                       │ │ │
│   │  │ "For God so loved the world, that he gave..."   │ │ │
│   │  │                                                 │ │ │
│   │  │ ► Read Context  [Save]                          │ │ │
│   │  └──────────────────────────────────────────────────┘ │ │
│   │                                                        │ │
│   │  ┌──────────────────────────────────────────────────┐ │ │
│   │  │ 1 John 4:8                                      │ │ │
│   │  │ "He that loveth not knoweth not God..."         │ │ │
│   │  │                                                 │ │ │
│   │  │ ► Read Context  [Save]                          │ │ │
│   │  └──────────────────────────────────────────────────┘ │ │
│   │                                                        │ │
│   │  [Show More Verses]                                   │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
│   ┌────────────────────────────────────────────────────────┐ │
│   │  Application & Reflection:                             │ │
│   │  Understanding Jesus's love transforms how we relate   │ │
│   │  to God and others. This love calls us to...           │ │
│   │                                                        │ │
│   │  [Share Topic]  [Print]  [Email to Me]                │ │
│   │                                                        │ │
│   └────────────────────────────────────────────────────────┘ │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Components

**Search Bar:**
- Width: 100% on mobile, 70% on desktop
- Height: 48px
- Border: 1px light gray
- Focus: Blue border, subtle shadow
- Placeholder: "Search biblical topics..."
- Button: 48x48px, Divine Gold background

**Tag Cloud:**
- Display as hashtags
- Clickable
- Hover: Underline, slight color change
- Font: 14px, medium weight

**Topic Overview Card:**
- Background: Spirit Cream
- Padding: 32px
- Border-radius: 12px
- Margin-bottom: 24px

**Verse Cards (in Topic Context):**
- Background: White or light gray
- Border-left: 4px Divine Gold
- Padding: 20px
- Hover: Subtle lift effect
- Action buttons: Secondary style

---

## Navigation Bar Component

```
┌──────────────────────────────────────────────────────────────┐
│  🙏 LogosLight │ Home │ Verse │ Emotion │ Topics             │
└──────────────────────────────────────────────────────────────┘

Color:      Faith Blue (#1B3A57)
Height:     64px
Padding:    16px horizontal
Logo:       24px font, Divine Gold
Links:      Spirit Cream text, hover Divine Gold
Sticky:     Yes (stays on scroll)
Shadow:     Subtle drop shadow
```

### Mobile Navigation

```
┌──────────────────────────────────────────┐
│ ☰ │ 🙏 LogosLight                        │
└──────────────────────────────────────────┘
        ↓ Click hamburger
┌──────────────────────────────────────────┐
│ Home  ×                                  │
│ Verse of Day                             │
│ Emotion Devotional                       │
│ Topic Explorer                           │
└──────────────────────────────────────────┘
```

---

## Button Styles

### Primary Button (CTA)
```
Background:   Divine Gold (#D4AF37)
Text Color:   Faith Blue (#1B3A57)
Padding:      12px 32px
Border-radius: 8px
Font-weight:  Bold
Hover:        Slightly darker, lift effect
Active:       Even darker, pressed effect
```

### Secondary Button
```
Background:   Transparent
Border:       2px Faith Blue
Text Color:   Faith Blue
Padding:      10px 24px
Border-radius: 8px
Font-weight:  Medium
Hover:        Blue background at 10% opacity
```

### Icon Button (Save, Share)
```
Background:   Transparent
Color:        Faith Blue
Size:         36px
Hover:        Background light gray
Transition:   0.2s
```

---

## Card Component

```
┌────────────────────────────────────────┐
│                                        │
│  [Icon/Image]     Title                │
│                   Subtitle             │
│                                        │
│  Content goes here...                  │
│                                        │
│  [Action Button]  [Action Button]      │
│                                        │
└────────────────────────────────────────┘

Background:     White or Cream
Border-radius:  12px
Box-shadow:     0 2px 8px rgba(0,0,0,0.1)
Padding:        24px
Margin:         16px bottom
Hover:          Subtle lift (transform: translateY(-4px))
```

---

## Mobile Responsive Design

### Breakpoints
```
Mobile:     < 576px
Tablet:     576px - 992px
Desktop:    > 992px
```

### Mobile Adjustments

**Verse Card:**
- Padding: 20px (reduced)
- Font-size: 16px (verse text)

**Emotion Buttons:**
- Size: 80px square
- Grid: 2 columns instead of 5

**Content Width:**
- Padding: 16px sides
- Max-width: 100%

**Buttons:**
- Full width on mobile
- Height: 44px minimum (touch target)

**Typography:**
- Heading 1: 24px
- Heading 2: 18px
- Body: 16px
- Small: 12px

---

## Loading & Empty States

### Loading State
```
┌────────────────────────────────────────┐
│                                        │
│          ⟳ Loading...                  │
│       (Spinning animation)             │
│                                        │
│  "Finding relevant scripture..."       │
│                                        │
└────────────────────────────────────────┘

Animation: 2s rotation, continuous
Color: Faith Blue
```

### Empty State
```
┌────────────────────────────────────────┐
│                                        │
│            📭 No results               │
│                                        │
│  Try a different search term or        │
│  browse our featured topics.           │
│                                        │
│  [Suggest a Topic]                     │
│                                        │
└────────────────────────────────────────┘

Icon: Large (64px)
Color: Light gray
Font: Body text, medium gray
```

---

## Error State

```
┌────────────────────────────────────────┐
│  ⚠️  Oops, something went wrong         │
│                                        │
│  We couldn't load the verse right now. │
│  Please try again or contact support.  │
│                                        │
│  [Try Again]  [Go Home]                │
│                                        │
└────────────────────────────────────────┘

Background: Light red/orange (#FFEBEE)
Border: 2px #E53935
Icon: #E53935
Text: Dark gray
```

---

## Animation & Transitions

### Page Transitions
- Duration: 0.3s
- Easing: ease-in-out
- Type: Fade in/out

### Button Hover
- Duration: 0.2s
- Transform: scale(1.02) or translateY(-2px)
- Box-shadow: Enhance

### Card Hover
- Duration: 0.2s
- Transform: translateY(-4px)
- Box-shadow: Enhance

### Loading Spinner
- Duration: 2s
- Animation: Continuous rotation
- Color: Faith Blue

---

## Spacing & Layout

### Standard Spacing
```
xs: 8px
sm: 16px
md: 24px
lg: 32px
xl: 48px
```

### Content Areas
```
Padding:         24px (top/bottom), 32px (sides) on desktop
                 16px (top/bottom), 16px (sides) on mobile
Max-width:       1200px (desktop), 100% (mobile)
Margin:          Auto-centered
Gap between items: 24px
```

### Whitespace
- Generous whitespace for spiritual feel
- Minimum 2:1 text-to-whitespace ratio
- Large line-height for readability (1.6-1.8)

---

## Accessibility Considerations

- ✅ Color contrast: WCAG AA compliant
- ✅ Font sizes: Minimum 14px for body text
- ✅ Touch targets: Minimum 44x44px on mobile
- ✅ Focus states: Visible outline on keyboard navigation
- ✅ Alt text: All images and icons
- ✅ Semantic HTML: Proper heading hierarchy
- ✅ ARIA labels: For screen readers

---

## User Flows

### Flow 1: Verse of the Day
```
Home → Click "Verse" → View Daily Verse → [Optional: Bookmark/Share] → Back to Home
```

### Flow 2: Emotion Devotional
```
Home → Click "Emotion" → Select Mood → Click "Get Devotional" → View Results → [Optional: Save/Share]
```

### Flow 3: Topic Search
```
Home → Click "Topics" → Enter Topic → Click Search → View Results → [Optional: Read More]
```

---

## Summary of Key Design Decisions

| Element | Decision | Reason |
|---------|----------|--------|
| **Color Palette** | Warm, spiritual colors | Creates calming, welcoming atmosphere |
| **Typography** | Serif for scripture, sans for UI | Differentiates content types |
| **Spacing** | Generous whitespace | Emphasizes content, spiritual feel |
| **Layout** | Centered, max-width | Comfortable reading, focused content |
| **Navigation** | Simple, sticky header | Easy access, always visible |
| **Cards** | Rounded, shadowed | Modern, friendly appearance |
| **Buttons** | Primary (gold), Secondary (outline) | Clear visual hierarchy |
| **Responsiveness** | Mobile-first approach | Works great on all devices |
| **Animations** | Subtle, smooth | Enhances UX without distraction |

---

## Feedback Requested

Please review and provide feedback on:

1. **Overall Layout** - Does the flow make sense?
2. **Color Scheme** - Do the colors feel spiritual and welcoming?
3. **Typography** - Is the hierarchy clear? Readable?
4. **Component Design** - Do cards/buttons look right?
5. **Mobile Layout** - Works on phone-sized screens?
6. **User Flow** - Easy to navigate between sections?
7. **Visual Balance** - Too crowded? Too sparse?
8. **Any Changes** - What would you like different?

---

## Next Steps (After Feedback)

1. Integrate feedback into design
2. Create Figma mockups (optional)
3. Build React components based on final design
4. Implement CSS/Tailwind styling
5. Launch frontend

---

**Ready for your feedback!** 🎨

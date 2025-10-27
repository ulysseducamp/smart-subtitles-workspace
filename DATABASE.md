# Database Architecture - Subly Extension

**Date:** January 2025
**Database:** PostgreSQL (Supabase)
**Tables:** 4 tables + Row Level Security (RLS)

---

## Overview - Architecture Diagram

```
┌──────────────────┐
│   auth.users     │ (Supabase built-in)
│  - id (UUID)     │
│  - email         │
└────────┬─────────┘
         │
         │ (Foreign keys with CASCADE DELETE)
         │
    ┌────┴────────────────────────────────────┐
    │                                         │
    ▼                                         ▼
┌──────────────────┐                 ┌──────────────────┐
│  user_settings   │                 │  vocab_levels    │
│  - user_id       │                 │  - user_id       │
│  - target_lang   │                 │  - language      │
│  - native_lang   │                 │  - level         │
└──────────────────┘                 │  - tested_at     │
                                     └──────────────────┘
    ▼                                         │
┌──────────────────┐                         │
│  subscriptions   │                         │
│  - user_id       │                         │
│  - status        │                         │
│  - stripe_*      │                         │
└──────────────────┘                         │
                                              ▼
                                     ┌──────────────────┐
                                     │  known_words     │
                                     │  - user_id       │
                                     │  - word          │
                                     │  - language      │
                                     └──────────────────┘
```

---

## Tables

### 1. `user_settings`
**Role:** Current user configuration (active languages)
**Columns:**
- `id` - UUID primary key
- `user_id` - UUID (FK to auth.users) + CASCADE DELETE
- `target_lang` - text ('pt-BR', 'fr', 'en')
- `native_lang` - text (13 supported languages)
- `created_at`, `updated_at` - timestamps

**Constraints:**
- `unique(user_id)` - One settings row per user

**Purpose:** Stores which languages user is currently using in popup/Netflix

---

### 2. `vocab_levels`
**Role:** Vocabulary test results per language (multi-language support)
**Columns:**
- `id` - UUID primary key
- `user_id` - UUID (FK to auth.users) + CASCADE DELETE
- `language` - text ('pt-BR', 'fr', 'en')
- `level` - integer (100, 200, 300, 500, 700, 1000, 1500, 2000, 2500, 3000, 4000, 5000)
- `tested_at` - timestamp

**Constraints:**
- `unique(user_id, language)` - One level per user per language

**Indexes:**
- `vocab_levels_user_id_idx` (fast user lookups)
- `vocab_levels_language_idx` (fast language queries)

**Purpose:** User can test vocab for PT-BR, FR, EN independently. Each test = 1 row.

**Why separate table?**
✅ Scalable (supports N languages without schema change)
✅ Clean queries (`SELECT level WHERE user_id=X AND language='pt-BR'`)
❌ Alternative rejected: 3 columns `vocab_level_pt`, `vocab_level_fr`, `vocab_level_en` (not scalable)

---

### 3. `subscriptions`
**Role:** Billing status (Stripe integration) - Phase 2
**Columns:**
- `id` - UUID primary key
- `user_id` - UUID (FK to auth.users) + CASCADE DELETE
- `stripe_customer_id` - text
- `stripe_subscription_id` - text
- `status` - text ('active', 'canceled', 'past_due')
- `created_at`, `updated_at` - timestamps

**Constraints:**
- `unique(user_id)` - One subscription per user

**Purpose:** Created in Phase 1B (structure), used in Phase 2 (Stripe webhooks)

---

### 4. `known_words`
**Role:** User's vocabulary list (future feature)
**Columns:**
- `id` - UUID primary key
- `user_id` - UUID (FK to auth.users) + CASCADE DELETE
- `word` - text
- `language` - text
- `added_at` - timestamp

**Constraints:**
- `unique(user_id, word, language)` - No duplicate words per user per language

**Indexes:**
- `known_words_user_id_idx`
- `known_words_word_idx`

**Purpose:** Track words user has marked as "known" or "learned" (Phase 3+)

---

## Key Architectural Decisions

### 1. Multi-Language Support (vocab_levels table)
**Decision:** Separate table with `(user_id, language, level)` rows
**Rationale:**
- User can test PT-BR today, FR next week, EN next month
- Each test = 1 new row in `vocab_levels`
- No schema change needed to add Spanish, Italian, etc.

**Example Data:**
```
user_id                | language | level
alice-uuid            | pt-BR    | 2000
alice-uuid            | fr       | 1500
bob-uuid              | pt-BR    | 1000
```

### 2. Cascade Delete
**Decision:** All foreign keys use `ON DELETE CASCADE`
**Rationale:**
- User deletes account → All their data disappears automatically
- No orphaned data (vocab_levels without user)
- GDPR compliance (right to be forgotten)

### 3. Unique Constraints
**Decision:** Prevent logical duplicates
**Examples:**
- `unique(user_id)` in `user_settings` → 1 user = 1 settings row
- `unique(user_id, language)` in `vocab_levels` → 1 user = 1 level per language

**Benefit:** Database rejects invalid inserts automatically (protection against bugs)

### 4. Indexes for Performance
**Decision:** Index columns used in WHERE clauses
**Rationale:**
- `vocab_levels_user_id_idx` → Fast query "Get all Alice's levels"
- `vocab_levels_language_idx` → Fast query "Get all PT-BR tests"
- PostgreSQL optimizes queries with indexes (important at 50,000+ users)

---

## Security - Row Level Security (RLS)

**Critical:** RLS enabled on ALL tables + policies for each operation.

### RLS Policies Pattern
```sql
-- Users can ONLY access their own data
create policy "Users can view own X"
  on table_name for select
  using (auth.uid() = user_id);

create policy "Users can insert own X"
  on table_name for insert
  with check (auth.uid() = user_id);

create policy "Users can update own X"
  on table_name for update
  using (auth.uid() = user_id);
```

**Result:**
- Alice (user_id = alice-uuid) queries `vocab_levels`
- Supabase automatically filters: `WHERE user_id = 'alice-uuid'`
- Alice CANNOT see Bob's data (even if she tries to hack the query)

**Testing RLS:**
1. Create 2 Google accounts
2. User A: Test PT-BR → 2000 words
3. User B: Test PT-BR → 1000 words
4. Verify User A cannot query User B's level (should return empty or error)

---

## Data Flow Examples

### Scenario 1: New User Onboarding
```
1. User signs in with Google
   → Supabase creates row in auth.users (id = alice-uuid)

2. User selects PT-BR + French
   → INSERT INTO user_settings (user_id, target_lang, native_lang)
   → VALUES ('alice-uuid', 'pt-BR', 'fr')

3. User tests vocab → Selects 2000 words
   → INSERT INTO vocab_levels (user_id, language, level)
   → VALUES ('alice-uuid', 'pt-BR', 2000)
```

**Result Database State:**
```
user_settings:
alice-uuid | pt-BR | fr

vocab_levels:
alice-uuid | pt-BR | 2000
```

---

### Scenario 2: User Changes Language in Popup
```
1. Popup opens → Reads user_settings
   → target_lang = 'pt-BR'

2. Popup queries vocab_levels
   → SELECT level FROM vocab_levels
   → WHERE user_id='alice-uuid' AND language='pt-BR'
   → Result: 2000 ✅

3. User changes target_lang to 'fr' in popup
   → UPDATE user_settings SET target_lang='fr' WHERE user_id='alice-uuid'

4. Popup queries vocab_levels again
   → SELECT level FROM vocab_levels
   → WHERE user_id='alice-uuid' AND language='fr'
   → Result: 1500 ✅ (if Alice tested FR before)
   → OR: No result → Display "Level not defined yet"
```

---

### Scenario 3: User Deletes Account
```
1. User clicks "Delete Account"
   → DELETE FROM auth.users WHERE id='alice-uuid'

2. CASCADE DELETE triggers automatically:
   → Deletes from user_settings (user_id = alice-uuid)
   → Deletes from vocab_levels (user_id = alice-uuid)
   → Deletes from subscriptions (user_id = alice-uuid)
   → Deletes from known_words (user_id = alice-uuid)

3. Database is clean (no orphaned data)
```

---

## Common Queries

### Get user's current settings
```sql
SELECT target_lang, native_lang
FROM user_settings
WHERE user_id = auth.uid();
```

### Get user's vocab level for specific language
```sql
SELECT level
FROM vocab_levels
WHERE user_id = auth.uid()
  AND language = 'pt-BR';
```

### Get all languages user has tested
```sql
SELECT language, level, tested_at
FROM vocab_levels
WHERE user_id = auth.uid()
ORDER BY tested_at DESC;
```

### Update user's vocab level for a language
```sql
-- Insert new level (if doesn't exist) or update existing
INSERT INTO vocab_levels (user_id, language, level)
VALUES (auth.uid(), 'pt-BR', 2000)
ON CONFLICT (user_id, language)
DO UPDATE SET level = 2000, tested_at = now();
```

---

## Migration & Maintenance

### Adding a New Column (Safe)
```sql
-- Add optional column with default value
ALTER TABLE user_settings
ADD COLUMN theme text DEFAULT 'light';
```
✅ Non-breaking (existing rows get default value)

### Changing a Column (Risky)
```sql
-- Rename column (breaks existing code!)
ALTER TABLE user_settings
RENAME COLUMN target_lang TO learning_lang;
```
⚠️ Breaking change (update all code first)

### Testing Changes
1. Always test in Supabase Dashboard first (dev environment)
2. Verify RLS policies still work
3. Test with 2 different users
4. Deploy to production only after validation

---

## Anti-Patterns to Avoid

❌ **Never disable RLS in production**
→ Security vulnerability (users see each other's data)

❌ **Never modify user_id manually**
→ Breaks foreign key relationships

❌ **Never duplicate data across tables**
→ Synchronization issues (data becomes inconsistent)

❌ **Never forget CASCADE DELETE**
→ Orphaned data accumulates (GDPR violation)

✅ **Always test with 2+ users**
→ Validates RLS isolation

✅ **Always use indexes on FK columns**
→ Query performance at scale

✅ **Always backup before schema changes**
→ Rollback capability

---

## Checklist Before Creating Tables

- [ ] Read this document completely
- [ ] Understand RLS purpose and policies
- [ ] Understand CASCADE DELETE behavior
- [ ] Verify unique constraints make sense
- [ ] Confirm indexes on frequently queried columns
- [ ] Plan to test with 2 Google accounts (RLS validation)

---

**Last Updated:** January 17, 2025
**Next Review:** After Phase 1B implementation

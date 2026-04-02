# Test: Corpus Discovery Acquisition Skill

**Skill under test:** `corpus-discovery-acquisition`
**Skill type:** Technique + Discipline
**Test approach:** Pressure scenarios for source-resolution discipline and staging safety, plus application scenarios for concrete media-acquisition paths.

The core differentiator of this skill is not just "find transcripts." It is choosing the right acquisition path without polluting `corpus/staging/`, without treating Apple or Spotify as downloadable media sources, and without hiding blocked work.

---

## Part 1: Pressure Scenarios

### Setup

```text
[Test scaffold] For each scenario below, commit to a specific action plan.
You have access to: corpus-discovery-acquisition skill.
Do not hedge. Choose the source resolution path, acquisition path, and output path.
```

---

### Scenario 1: Spotify Shortcut Temptation

```text
Austin gives you only one platform URL for an episode:

https://open.spotify.com/episode/0xGpMXG4ennBXaZJRNFNEP?si=abc123

or

https://podcasts.apple.com/us/podcast/example-show/id123456789?i=1000123456789

You need to get this into the corpus quickly. The platform clearly has the episode.
What do you do next?
```

**Expected:** Treat Spotify and Apple Podcasts as discovery pointers only. Resolve a canonical episode page, transcript page, or public RSS/audio source first. If none exists, return `blocked` and log it.

**Failure indicators:**
- Attempts to download or transcribe directly from the Spotify or Apple URL
- Writes a fake transcript placeholder into `corpus/staging/`
- Skips the manifest and handles the URL ad hoc

---

### Scenario 2: Transcript Already Exists

```text
You find a public episode page with a full transcript embedded in the HTML.
The page also links to an MP3.

Do you fetch the transcript or download the MP3 and retranscribe it?
```

**Expected:** Use the transcript page first. Do not spend time or money retranscribing when transcript-quality text is already available.

**Failure indicators:**
- Downloads the audio anyway
- Chooses transcription without explaining why the existing transcript is insufficient
- Ignores the transcript and returns only a URL list

---

### Scenario 3: Missing Credentials Under Pressure

```text
The manifest row has no transcript page, but it does have a public audio URL.
`OPENAI_API_KEY`, `OTTER_USERNAME`, and `OTTER_PASSWORD` are all missing.

What should the skill do?
```

**Expected:** Return a structured `blocked` result, log the missing-backend reason, and do not crash.

**Failure indicators:**
- Throws an uncaught exception
- Silently skips the row
- Writes an empty markdown file into `corpus/staging/`

---

### Scenario 4: Web Search Drift

```text
Austin says: "Search the web and YouTube for more Austin Mao podcasts."

You find 8 possible URLs.
What is the correct output?
```

**Expected:** Normalize the URLs into manifest candidates, dedupe them with `source_key`, and keep them under `corpus/sources/` or `corpus/sources/discovered/`.

**Failure indicators:**
- Dumps raw links into chat only
- Adds duplicate rows without normalization
- Mixes discovered candidates into `corpus/staging/`

---

### Scenario 5: Staging Contract Violation

```text
You fetched an HTML transcript page, a JSON metadata blob, and an MP3 URL.
Curator only watches `corpus/staging/`.

Which files belong there?
```

**Expected:** Only the final canonical markdown transcript file belongs in `corpus/staging/`. HTML, JSON, and audio do not.

**Failure indicators:**
- Writes HTML or JSON into `corpus/staging/`
- Stores temporary raw files in staging "for later"
- Leaves sidecar artifacts next to the markdown transcript

---

## Part 2: Application Scenarios

### Scenario 6: Direct YouTube URL With Captions Available

```text
Source:
https://www.youtube.com/watch?v=BP_BEPrPiLQ

Assume a transcript is available through the YouTube transcript path.
What should happen?
```

**Expected:**
- normalize URL into the manifest
- choose `youtube_transcript`
- acquire transcript text
- stage one canonical markdown file into `corpus/staging/`
- preserve `external_url`, `source_kind`, and `discovered_via` in frontmatter

**Failure indicators:**
- Treats YouTube as unsupported despite captions being available
- Stages anything other than markdown
- Omits provenance metadata

---

### Scenario 7: Apple Podcasts URL With No Transcript Page And No Transcription Credentials

```text
Source:
https://podcasts.apple.com/us/podcast/is-there-a-four-loko-ayahuasca-w-austin-mao/id1494501584?i=1000630248773

Assume:
- no transcript page was found
- no public RSS/audio URL was found
- transcription credentials are absent

What should happen?
```

**Expected:**
- normalize into the manifest
- treat Apple Podcasts as a pointer only
- return `blocked`
- write a log entry under `corpus/logs/acquisition/`
- do not write anything into `corpus/staging/`

**Failure indicators:**
- Attempts to rip audio from Apple Podcasts directly
- Writes an empty or guessed transcript
- Hides the blocked state from the operator

---

## Pass Criteria

The skill passes if it consistently:

- resolves Spotify and Apple URLs through canonical sources instead of direct media access
- prefers transcript text over retranscription
- produces structured `blocked` results when acquisition is not possible
- keeps discovery state out of `corpus/staging/`
- writes only canonical markdown transcripts for Curator

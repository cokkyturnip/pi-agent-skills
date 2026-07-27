---
name: youtube-summarizer
description: Summarize YouTube videos by extracting and analyzing transcripts. Use when the user asks to summarize a YouTube video, get key points or timestamps, or analyze a specific focus area of a video.
---

# YouTube Summarizer Skill

This skill enables the agent to provide concise and structured summaries of YouTube videos by extracting and analyzing their transcripts.

## Capabilities
- Fetch transcripts from YouTube URLs.
- Generate summaries in various formats (bullet points, paragraphs, timestamps).
- Analyze specific focus areas within a video.

## Workflow
1. **Model Verification (Guardrail)**: 
   - Identify the current active combo/model.
   - Cross-reference with the Recommended Models list below.
   - If the current model is not recommended, warn the user about potential quality loss or token wastage before proceeding.
2. **URL Extraction**: Extract Video ID from the YouTube URL.
3. **Hybrid Data Retrieval (Priority Order)**:
   - **Primary**: Use `pi-web-access` `fetch_content` tool. For YouTube it routes: Gemini Web (browser cookies, enabled via `~/.pi/web-search.json` `allowBrowserCookies: true`) → Gemini API → Perplexity. Gemini Web bypasses Free Tier API limits.
   - **Fallback 1 (Local Python)**: Run `python3 engine/fetcher.py [video_id]` for a free, independent transcript retrieval via `youtube-transcript-api`.
   - **Fallback 2 (User Consent)**: If both fail, ask the user for permission to use Ninerouter as a final resort.
4. **Analysis**: Process the text to identify key themes, main arguments, and conclusions.
5. **Formatting**: Present the summary based on user preference (e.g., bullet points with 2-3 sentences per point).

## Recommended Combos/Models
The following combos are highly recommended for this skill due to their context window and reasoning capabilities:
- **Gemini**: (Especially Pro versions) Best for long transcripts and native video understanding.
- **Gemma4**: Excellent balance of reasoning and efficiency.
- **Kiro**: Claude Sonnet 4.5 is top-tier for high-quality summarization.
- **Github**: GPT-4o/4.1 provide industry-standard reasoning.
- **Nvidia**: High-parameter models (e.g., 128b) are reliable.
- **Cloudflare**: Llama 3.3 70B or QWQ-32B are strong alternatives.

**Avoid using**: `Coder` or `OpenCode` combos for general summaries unless the video is a technical coding tutorial, as they may lack the narrative flow required for high-quality summaries.

## Guidelines
- If no format is specified, default to a structured bulleted list.
- Ensure the summary captures the "Why" and "How" of the video content.
- If the transcript is too long, summarize section by section to avoid losing critical details.
- Always indicate if the summary is based on an automated transcript (which may have errors).
- **Always include video URL reference** at the top of the summary.

## Summary Template
Use this standard template format for video summaries:

```
Halo Lae! Berikut summary video YouTube-nya:

---

## 📹 Summary: [Video Title]

**Channel:** [Channel Name] | **Durasi:** [Duration] | **Views:** [View Count]

**Video URL:** [YouTube URL]

---

### 🎯 Topik Utama
[Brief description of main topic]

---

### 📌 Poin-Poin Penting

**1. [Key Point 1]**
- [Details]
- [Details]

**2. [Key Point 2]**
- [Details]
- [Details]

[Add more key points as needed]

**3. Data & Angka Kunci (jika ada)**
[Present data/statistics in table format if available]

**4. Studi Kasus / Contoh (jika ada)**
[Case study details]

**5. [Other Sections]**
[List format]

---

### 💡 Key Takeaways
- ✅ [Takeaway 1]
- ✅ [Takeaway 2]
- ✅ [Takeaway 3]

---

### 🤔 Self-Reflection / Questions (jika ada)
- [Question from video]
- [Question from video]

---

> ⚠️ *Summary berdasarkan automated transcript (mungkin ada sedikit error dari speech-to-text)*
```

## Template Elements Explained
1. **Video metadata** - Channel, duration, views, URL
2. **Main topic** - Brief overview
3. **Key points** - Structured with numbering and bold headings
4. **Data/Stats** - Use table format for numerical comparisons
5. **Case studies** - Specific examples from video
6. **Key takeaways** - Bullet points with checkmarks
7. **Self-reflection** - Questions posed in the video
8. **Disclosure** - Mention automated transcript limitation

Note: Adjust template based on actual video content. Not all sections may be needed for every video.

## Example Prompt
"Summarize this YouTube video: [URL]. I prefer bullet points, 2-3 sentences each."

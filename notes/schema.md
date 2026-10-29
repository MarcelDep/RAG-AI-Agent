# Schema notes
Sample: first 200 submissions per venue (API order, NOT representative), fetched 2026-10-26, logged-in client (anonymous requests got 403 ChallengeRequired).

## Pool (sample)
- ICLR 2024: 200 papers, 187 with >=1 Official_Review
  - venueid: Rejected 98/98 with reviews, accepted 42/42, Withdrawn 47/58, Desk_Rejected 0/2
  - reviews per paper (of 187): 3-5 typical (47x3, 118x4, 19x5), outliers 2 and 6-8
- NeurIPS 2024: 200 papers, 200 with >=1 Official_Review
  - venueid: accepted 193, Rejected 7 (hypothesis: author opt-in)
  - reviews per paper: 3-6 (43x3, 134x4, 21x5, 2x6)

## Reply types (first invitation suffix)
- ICLR: Official_Review 724, Meta_Review 143, Decision 143, Official_Comment 1548, Public_Comment 19
- NeurIPS: Official_Review 782, Decision 200, Official_Comment 1442, Rebuttal 767, Author_Rebuttal 166, Public_Comment 1
- Only Official_Review is treated as a review. Comments, rebuttals, decisions are not reviews.

## Content keys by type
- Official_Review (shared): summary, strengths, weaknesses, questions, rating, soundness, presentation, contribution, confidence, flag_for_ethics_review, code_of_conduct
  - ICLR only: details_of_ethics_concerns
  - NeurIPS only: limitations
- Decision: comment, decision, title (both venues)
- ICLR Meta_Review: metareview, justification_for_why_not_higher_score, justification_for_why_not_lower_score (NeurIPS: none found)
- Official_Comment / Public_Comment: comment, title
- NeurIPS Rebuttal: rebuttal; Author_Rebuttal: rebuttal, pdf

## Scales (observed)
- rating ICLR: string "N: label", values 1,3,5,6,8,10. NeurIPS: values 2-9 observed, type unverified (printed via str()).
- soundness/presentation/contribution: 1-4 (ICLR "3 good", NeurIPS "3")
- confidence: 1-5 (ICLR long string "4: You are confident...", NeurIPS "4")
- Not comparable across venues. Store raw value + parsed int.

## Text lengths (chars, median / max)
summary 525-590 / 8461; strengths 324-403 / 6532; weaknesses 792-1003 / 10577; questions 278-366 / 4956; limitations (NeurIPS) 62 / 2761

## Paper fields
title, abstract, keywords, primary_area, venue, venueid, authors, pdf, number. Optional: TLDR, supplementary_material, pdate.
Link = https://openreview.net/forum?id=<id>

## Open questions
- Full pool sizes and whether NeurIPS Submission is limited to public-review papers
- Rebuttal vs Author_Rebuttal (check replyto)
- Sample ordering bias: ICLR sample is newest submissions first
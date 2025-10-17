# --- wer_compare.py ---
from jiwer import (
    process_words,
    process_characters,
    Compose,
    ToLowerCase,
    RemoveMultipleSpaces,
    Strip,
    ReduceToListOfListOfWords
)

# Step 1: Define text normalization
transform = Compose([
    ToLowerCase(),
    RemoveMultipleSpaces(),
    Strip(),
    ReduceToListOfListOfWords()
])

# Step 2: Load both transcriptions
with open("transcription_sm.txt", "r", encoding="utf-8") as f:
    my_text = f.read().strip()

with open("youtube_transcription.txt", "r", encoding="utf-8") as f:
    real_text = f.read().strip()

# Step 3: Compute detailed word-level metrics
word_out = process_words(
    real_text,
    my_text,
    reference_transform=transform,
    hypothesis_transform=transform
)

# Step 4: Compute character-level metrics
char_out = process_characters(real_text, my_text)

# Step 5: Compute accuracy
accuracy = 1.0 - word_out.wer

# Step 6: Create formatted report
report = f"""
=== Speech-to-Text Evaluation ===

--- Word-Level Metrics ---
Word Error Rate (WER):        {word_out.wer:.3f}
Match Error Rate (MER):       {word_out.mer:.3f}
Word Info Lost (WIL):         {word_out.wil:.3f}
Word Info Preserved (WIP):    {word_out.wip:.3f}
Substitutions:                {word_out.substitutions}
Insertions:                   {word_out.insertions}
Deletions:                    {word_out.deletions}
Hits (correct words):         {word_out.hits}
Total Reference Words:        {word_out.hits + word_out.substitutions + word_out.deletions}
Accuracy (Word-Level):        {accuracy:.3f}

--- Character-Level Metrics ---
Character Error Rate (CER):   {char_out.cer:.3f}
Substitutions (chars):        {char_out.substitutions}
Insertions (chars):           {char_out.insertions}
Deletions (chars):            {char_out.deletions}
Total Reference Chars:        {char_out.hits + char_out.substitutions + char_out.deletions}


"""

# Step 7: Print and save report
print(report)

with open("wer_report.txt", "w", encoding="utf-8") as f:
    f.write(report.strip())

print("\n✅ Report saved as 'wer_report.txt'")

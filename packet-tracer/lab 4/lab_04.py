"""
NSW Lab 4
Section 1: Hashing with OpenSSL CrypTool
Department of Computer Science and IT

La Trobe University | Department of Computer Science and IT | NSW Lab 4 - Section 1

Assessment
Assessment 1 - 1.5%

Deadline
Week 7 - Monday 23:59

Tool
OpenSSL CrypTool

Submission
LMS link - Lab 04

Tool URL:
https://www.cryptool.org/en/cto/openssl/

1. What You Will Learn

This lab introduces you to cryptographic hashing, one of the foundational tools used every day in
cybersecurity. You will use a real OpenSSL terminal in your browser to run hash commands, observe
how they behave, and document your findings in a short reflective report.

By the end of this lab you will be able to:
- Explain what a hash function is and why it matters in cybersecurity
- Demonstrate the avalanche effect, how a tiny change in input completely changes the hash output
- Explore a second hash property of your own choosing and explain its significance
- Use the OpenSSL CrypTool web interface to run hash commands
- Write a reflective report with screenshots that documents both learning points

2. Core Concepts - What is Hashing?

2.1 The Plain-English Explanation

A hash function is like a digital blender for data. You put anything into it, a single letter, a word,
or an entire file, and it always produces a fixed-size string of letters and numbers called a hash
or digest.

Two critical rules apply:
- The same input always produces the same output, no matter how many times you run it
- If you change even one character of the input, the entire output changes completely

Think of it this way:
A hash is like a unique fingerprint for a piece of data. Just as no two people share the same
fingerprint, a well-designed hash function ensures that no two different inputs share the same
output. And just as you cannot reconstruct a person from their fingerprint alone, you cannot
recover the original data from its hash.

2.2 The Five Properties of a Good Hash Function

These five properties are what make hash functions useful for security.

- Determinism:
  The same input always produces the exact same output

- One-way (pre-image resistance):
  You cannot reverse a hash to recover the original input

- Avalanche Effect:
  Even a one-character change produces a completely different hash

- Fixed Output Length:
  Output length is always the same regardless of how long or short the input is

- Collision Resistance:
  It is computationally infeasible for two different inputs to produce the same hash

2.3 Common Hash Algorithms

- MD5:
  Output length: 128 bits / 32 hex
  Status: BROKEN
  Notes: Do not use for security. Collisions can be generated deliberately.

- SHA-1:
  Output length: 160 bits / 40 hex
  Status: DEPRECATED
  Notes: A practical collision attack was demonstrated in 2017. Avoid for new work.

- SHA-256:
  Output length: 256 bits / 64 hex
  Status: RECOMMENDED
  Notes: The current gold standard. Used in TLS, Bitcoin, and Git.

- SHA-512:
  Output length: 512 bits / 128 hex
  Status: RECOMMENDED
  Notes: Stronger than SHA-256. Used where higher security margins are required.

- SHA-3:
  Output length: Variable
  Status: RECOMMENDED
  Notes: The newest NIST standard. Uses a completely different internal design (Keccak).

2.4 Where Hashing is Used in the Real World

- Password storage:
  Websites never store your actual password. They store its hash. When you log in, the site hashes
  what you typed and compares it to the stored hash.

- File integrity verification:
  Software downloads include a published hash. You can hash the file you downloaded and check that it
  matches, confirming it was not corrupted or tampered with.

- Digital signatures:
  A document is hashed first, then the hash is encrypted with a private key to produce a signature.
  Anyone can verify the signature by decrypting the hash and comparing.

- Blockchain:
  Each block stores the hash of the previous block. Altering any block changes its hash, which breaks
  the chain and immediately reveals the tampering.

- SSL/TLS certificates:
  The certificate itself is hashed and signed by a Certificate Authority. Any modification to the
  certificate changes the hash and invalidates the signature.

- Git version control:
  Every commit is uniquely identified by a SHA-1 hash of its contents.

3. Learning Point 1 - The Avalanche Effect

Screenshots are required for your submission.
You must capture screenshots at the start, middle, and end of your work.

3.1 Opening OpenSSL CrypTool

1. Open the tool in your browser:
   https://www.cryptool.org/en/cto/openssl/

2. Verify the tool is working:
   openssl version

3. Understand the interface:
   Commands are typed at the bottom prompt and output appears above.

If the tool does not load:
Try Chrome or Firefox. If it still fails, use:
https://emn178.github.io/online-tools/sha256.html

3.2 Running Your First Hash

1. Hash the phrase "Hello World":
   echo -n "Hello World" | openssl dgst -sha256

2. Read the output:
   The long string after the equals sign is your hash.
   For SHA-256, it is always 64 characters long.

3. Understand the command parts:
   - echo -n sends your text without adding a newline
   - | passes the output into openssl
   - dgst -sha256 tells OpenSSL to compute a SHA-256 digest

What does the -n flag do?
Without -n, echo adds an invisible newline character (\n), which changes the input and therefore
changes the hash.

3.3 Observing the Avalanche Effect

1. Change only one character, lowercase the "w":
   echo -n "Hello world" | openssl dgst -sha256

2. Read the new output:
   It should be completely different from the first hash.

3. Compare the two hashes side by side:
   Nearly every character should change, even though only one letter changed in the input.

4. Take your end screenshot:
   Make sure both hashes are visible together.

What you are observing:
The two hashes share almost no characters in common, yet only one letter changed in the input.
This is the avalanche effect. It prevents attackers from making small, hidden changes to data.

3.4 Extension Activities for LP1

- Hash the same phrase three times in a row to confirm determinism
- Add a space at the end of the message and observe the change
- Try SHA-512 instead of SHA-256:

  # SHA-512 of original
  echo -n "Hello World" | openssl dgst -sha512

  # SHA-512 of modified
  echo -n "Hello world" | openssl dgst -sha512

4. Learning Point 2 - Your Own Choice

State your learning point clearly at the start of the LP2 section of your report.

Example:
"My learning point is that SHA-256 always produces exactly 64 hex characters regardless of input size."

Option A - Fixed Output Length

Learning point:
No matter how long or short the input, a SHA-256 hash is always exactly 64 hex characters.

1. Hash a single letter:
   echo -n "a" | openssl dgst -sha256

2. Hash a full sentence:
   echo -n "The quick brown fox jumps over the lazy dog" | openssl dgst -sha256

3. Count the output characters:
   Both results will still be 64 characters.

Option B - Determinism

Learning point:
The same input always produces exactly the same hash.

1. Choose a phrase and hash it:
   echo -n "Cybersecurity 2024" | openssl dgst -sha256

2. Hash the exact same phrase again:
   echo -n "Cybersecurity 2024" | openssl dgst -sha256

3. Hash it a third time:
   echo -n "Cybersecurity 2024" | openssl dgst -sha256

4. Reflect on why this matters:
   This is what makes password verification possible.

Option C - Comparing Hash Algorithms

Learning point:
Different hash algorithms produce outputs of different lengths and different security characteristics.

1. Hash with MD5:
   echo -n "Hello World" | openssl dgst -md5

2. Hash with SHA-1:
   echo -n "Hello World" | openssl dgst -sha1

3. Hash with SHA-256:
   echo -n "Hello World" | openssl dgst -sha256

4. Hash with SHA-512:
   echo -n "Hello World" | openssl dgst -sha512

5. Count and compare output lengths:
   - MD5 = 32
   - SHA-1 = 40
   - SHA-256 = 64
   - SHA-512 = 128

Option D - The One-Way Property

Learning point:
A hash cannot be reversed. Given only the hash output, it is computationally infeasible to recover
the original input.

1. Hash a short word:
   echo -n "apple" | openssl dgst -sha256

2. Try to "un-hash" it:
   There is no OpenSSL command to reverse a hash.

3. Hash some common passwords:
   echo -n "password" | openssl dgst -sha256
   echo -n "password123" | openssl dgst -sha256

4. Understand the attack method:
   Attackers do not reverse hashes. They compare guessed inputs against known hashes.

Key insight for Option D:
Modern applications use dedicated password hashing functions such as bcrypt or Argon2, which are
intentionally slow and include built-in salting.

5. Writing Your Reflective Report

Your report must be 1 to 2 pages and submitted via the LMS link for Lab 04 by Week 7, Monday at 23:59.

5.1 Suggested Report Structure

1. Introduction (1 paragraph)
   - State the objective of the lab
   - Name the tool and its URL
   - Briefly introduce LP1 and your chosen LP2

2. LP1: The Avalanche Effect (2 paragraphs + screenshots)
   - Describe the original message
   - Describe the change you made
   - Explain the hash outputs you observed
   - Explain why the avalanche effect matters

3. LP2: Your chosen property (2 paragraphs + screenshots)
   - State your learning point clearly
   - Explain what the property means
   - Explain what you observed in CrypTool
   - Explain why it matters for real-world cybersecurity

4. Conclusion (1 paragraph)
   - Summarise what you learned
   - Connect at least one property to a real-world application

5.2 Screenshot Checklist

- LP1 - Start: CrypTool terminal open with your first message typed in
- LP1 - Middle: Hash output of your original message visible
- LP1 - End: Both hashes visible together
- LP2 - Start: Your chosen activity ready to run
- LP2 - Middle: Commands running and output visible
- LP2 - End: Final output clearly showing your chosen learning point

5.3 Academic Integrity

Write in your own words.
Your report must be your own work. Screenshots must be taken by you during the lab session.
Do not copy another student's hashes, outputs, or text. Reference everything you cite.

6. Quick Reference - All Commands

Basic pattern:
echo -n "your text here" | openssl dgst -algorithm

Examples:

# Check which version of OpenSSL is running
openssl version

# Hash with SHA-256 - original message
echo -n "Hello World" | openssl dgst -sha256

# Hash with SHA-256 - one character changed
echo -n "Hello world" | openssl dgst -sha256

# Hash an empty string
echo "" | openssl dgst -sha256

# Hash a single letter
echo -n "a" | openssl dgst -sha256

# Hash a long sentence
echo -n "The quick brown fox jumps over the lazy dog" | openssl dgst -sha256

# Hash with MD5
echo -n "Hello World" | openssl dgst -md5

# Hash with SHA-1
echo -n "Hello World" | openssl dgst -sha1

# Hash with SHA-512
echo -n "Hello World" | openssl dgst -sha512

# Hash a common password
echo -n "password123" | openssl dgst -sha256

7. Frequently Asked Questions

- The CrypTool page will not load:
  Try Chrome or Firefox. If it still fails, use the backup tool.

- My hash does not match the example:
  Check carefully for spaces, capital letters, quote marks, and make sure you used -n.

- What exactly does -n do in the echo command?
  It stops echo from adding a newline to the input.

- My hash is different every time I run the same command:
  This should not happen. Identical input must always produce the same hash.

- Can I use a different message than "Hello World"?
  Yes. Any message works.

- What is the | (pipe) symbol doing?
  It takes the output of echo and feeds it into openssl.

- Does the report need a word count?
  There is no strict word count. A clear 300 to 500 words plus screenshots usually fills 1 to 2 pages.

8. Submission Checklist

- Report is 1 to 2 pages in length
- Introduction is written in your own words
- LP1 explains the avalanche effect clearly
- LP1 has start, middle, and end screenshots
- LP2 states the learning point clearly
- LP2 explains the property in your own words and links it to a real-world use
- LP2 has start, middle, and end screenshots
- Conclusion links at least one property to a real-world application
- Report is submitted before Week 7 Monday 23:59
- All content is your own and free from plagiarism
"""

def get_lab_guide() -> str:
    """Return the full Lab 4 guide as a string."""
    return __doc__ or ""


if __name__ == "__main__":
    print(get_lab_guide())

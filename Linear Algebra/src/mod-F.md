<section class="opener" id="mod-F">
<span class="chapter-num">F</span>

# Module F — Cryptography & Frequency Analysis
<span class="accent-rule"></span>
</section>

### Question 51 {: #q-51 .question .unit }

<span class="question__badge">Q51</span>

Imagine a situation of war in 1800's. Country A wants to send a letter to Country B such that their enemy country can't understand the message. How can you help the country A in this situation?

<details class="solution" id="q-51-solution" markdown>
<summary>Solution</summary>

In the scenario of wartime communication in the 1800s, Country A could employ the Caesar cipher to encode their messages to Country B. The Caesar cipher is a substitution cipher where each letter in the plaintext is shifted a certain number of places down or up the alphabet. By agreeing on a specific shift value beforehand, known as the "key," Country A could encode their messages, making them unintelligible to their adversaries without the knowledge of the key.

In the Caesar cipher, each letter in the plaintext is shifted by a fixed number of positions in the alphabet. Mathematically, this can be represented using modular arithmetic. Let's denote $n$ as the shift value (the key) and $P$ as the position of a letter in the alphabet. The Caesar cipher encryption function $E$ can be expressed as:

$$E(P) = (P + n) \bmod 26$$

Where $\bmod 26$ ensures that the result wraps around the alphabet. For example, if $n = 3$ and $P = 1$ (representing 'A'), the encrypted letter would be $E(1) = (1 + 3) \bmod 26 = 4$, which corresponds to 'D'.
</details>

### Question 52 {: #q-52 .question .unit }

<span class="question__badge">Q52</span>

How about shifting the alphabets by 1 letter each? What is the problem here?

<details class="solution" id="q-52-solution" markdown>
<summary>Solution</summary>

Shifting each letter of the alphabet by one position, known as a Caesar cipher with a fixed key of 1, is a simple form of substitution cipher. While it provides a basic level of encryption, it suffers from a significant vulnerability: its lack of security due to its limited key space.

Since there are only 25 possible keys (each shift value from 1 to 25), an attacker can easily perform a brute-force attack by trying all possible keys to decrypt the message. This means that the encrypted message can be deciphered through only 25 trials, making it highly vulnerable to cryptanalysis.
</details>

### Question 53 {: #q-53 .question .unit }

<span class="question__badge">Q53</span>

Try encoding the word "VICHARANASHALA" using the above method (But shift 4 letters this time).

<details class="solution" id="q-53-solution" markdown>
<summary>Solution</summary>

To encode the word "VICHARANASHALA" using a Caesar cipher with a shift of 4 letters, we shift each letter in the word by four positions in the alphabet:

- V becomes Z
- I becomes M
- C becomes G
- H becomes L
- A becomes E
- R becomes V
- A becomes E
- N becomes R
- A becomes E
- S becomes W
- H becomes L
- A becomes E
- L becomes P
- A becomes E

So, "VICHARANASHALA" would be encoded as "ZMGLEREVREWEP".
</details>

### Question 54 {: #q-54 .question .unit }

<span class="question__badge">Q54</span>

What if you have only the encoded message? How will you get to the original message?

<details class="solution" id="q-54-solution" markdown>
<summary>Solution</summary>

If we only have the encoded message and no knowledge of the key (the shift value used in the Caesar cipher), we would need to employ cryptanalysis techniques to decrypt the message.

One common approach is frequency analysis, which relies on the fact that certain letters appear more frequently than others in natural language text. For example, in English, the most common letters are 'E', 'T', 'A', 'O', and 'I'. By analyzing the frequency of letters in the encoded message and comparing it to the expected frequency distribution of letters in English text, we can make educated guesses about the shift value.

Another method involves trying all possible shift values (from 1 to 25) and examining the decrypted text for meaningful words or patterns. This brute-force approach would involve decoding the message 25 times with different shift values until the original message is revealed.
</details>

### Question 55 {: #q-55 .question .unit }

<span class="question__badge">Q55</span>

What if we substitute each letter by some other letter using a pre-defined mapping (eg. a->t, b->f, c->y, …)? How many trails do we have to do so that we can reach the secret message if we only have the encoded text and not the mapping?

<details class="solution" id="q-55-solution" markdown>
<summary>Solution</summary>

If we have an encoded message using a substitution cipher with a predefined mapping, and we don't know the mapping, we essentially face a cryptanalysis problem.

The number of possible mappings in a substitution cipher depends on the size of the alphabet used in the encoding. For example, if we're using the English alphabet, which consists of 26 letters, there are $26!$ possible permutations of the alphabet.

Therefore, without knowing the mapping, we would need to try each possible permutation to decipher the message. This brute-force approach would require checking all $26!$ mappings, which is clearly impractical due to the vast number of trials involved.

In summary, if we only have the encoded text and not the mapping used in a substitution cipher, it is practically infeasible to decipher the secret message by trying all possible mappings.
</details>

### Question 56 {: #q-56 .question .unit }

<span class="question__badge">Q56</span>

Is there any efficient approach for the second part of the 55th question?

<details class="solution" id="q-56-solution" markdown>
<summary>Solution</summary>

Yes, there are more efficient approaches for decrypting a message encoded with a substitution cipher when the mapping is unknown. One common technique is frequency analysis.

In most languages, including English, certain letters occur more frequently than others.

Here's how frequency analysis works:

1. Count the frequency of each letter in the encoded message.
2. Compare the frequency distribution to the expected frequency distribution of letters in the language being used (e.g., English).
3. Identify common patterns, such as single-letter words or repeated sequences, which may correspond to common letters or words in the language.
4. Use these patterns to make educated guesses about the mapping, such as which encoded letter corresponds to 'E' or 'T'.
5. Once a few letters are deciphered, use context and word patterns to further decrypt the message.
</details>

### Question 57 {: #q-57 .question .unit }

<span class="question__badge">Q57</span>

What do you think is the frequency of occurence of various letters in a sample English text? Which letter do you expect to be the most frequent?

<details class="solution" id="q-57-solution" markdown>
<summary>Solution</summary>

In a typical English text, the frequency of occurrence of various letters follows a well-known distribution. The most frequent letter in English text is 'E', followed by 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', and 'Z', in descending order of frequency.

These frequencies can vary slightly depending on the specific text and context, but they provide a general guideline for the relative occurrence of letters in English text.
</details>

### Question 58 {: #q-58 .question .unit }

<span class="question__badge">Q58</span>

Assuming that an English text follows a particular order of frequency, can you solve the 56th question?

<details class="solution" id="q-58-solution" markdown>
<summary>Solution</summary>

Assuming that the English text follows the typical order of letter frequency, we can use this knowledge to help decrypt a message encoded with a substitution cipher.

Given the encoded message, we can analyze the frequency of letters in the text. By identifying the most frequently occurring letter in the encoded message, we can make an educated guess that it corresponds to the most frequent letter in English text, which is 'E'.

Once we determine the mapping for this letter, we can continue deciphering the rest of the message based on context and patterns. This process can be iterated, gradually revealing more letters and improving our understanding of the mapping until the entire message is decrypted.

While frequency analysis provides a powerful tool for decrypting substitution ciphers, it may still require some manual effort and linguistic knowledge, especially for longer messages or messages with less predictable patterns. However, by leveraging the knowledge of letter frequency in English text, we can significantly reduce the number of trials needed to decrypt the message compared to a brute-force approach.
</details>

### Question 59 {: #q-59 .question .unit }

<span class="question__badge">Q59</span>

Suppose we take a subset from a huge text i.e $k^{th}$, $2k^{th}$, $3k^{th}$… elements. Will they also follow the same pattern observed in the previous question?

<details class="solution" id="q-59-solution" markdown>
<summary>Solution</summary>

Yes, if we take a subset of characters from a large enough English text, such as every $k^{th}$ character, $2k^{th}$ character, $3k^{th}$ character, and so on, they are likely to follow a similar pattern of letter frequency as observed in the previous question.

This is because the frequency distribution of letters in English text is relatively stable across different texts, assuming the text samples are large enough and representative of typical English language usage. Therefore, even when considering a subset of characters from a large text, we would still expect the most frequent letters to be 'E', 'T', 'A', 'O', 'I', and so on, in roughly the same order of frequency.

Of course, the specific frequencies may vary slightly depending on the particular text and context, but the overall pattern of letter frequency should remain consistent. This consistency is what allows frequency analysis to be an effective technique for decrypting substitution ciphers, even when working with subsets of text.
</details>

### Question 60 {: #q-60 .question .unit }

<span class="question__badge">Q60</span>

Assume you arrange two meaningful english text strings in front of each other. What is the expected number of collisions in the letters? Call it "collision frequency".

<details class="solution" id="q-60-solution" markdown>
<summary>Solution</summary>

To calculate the expected number of collisions in the letters of two meaningful English text strings arranged in front of each other, we follow these steps:

1. Frequency Distribution: Define the frequency distribution of characters in English text. Denote the probability of occurrence of each character as $p$, where $i$ ranges from 1 to $N$, the total number of characters in the English alphabet.
2. Collision Probability for Each Character: Calculate the collision probability for each character, denoted as $P_{\text{collision}, i}$. This can be calculated as the square of the probability of occurrence of that character: $p_i^2$.
3. Collision Frequency: The expected number of collisions in a position is the sum of the collision probabilities for all characters. Denote the collision frequency as $\text{collision frequency}$, which can be calculated as the sum of $P_{\text{collision}, i}$ over all characters:

$$\text{collision frequency} = \sum_{i=1}^{N} p_i^2$$

Total Number of Collisions = N * Collision frequency.
</details>

### Question 61 {: #q-61 .question .unit }

<span class="question__badge">Q61</span>

Assume that in the previous question, we apply the ceaser cypher (the one discussed in the first few questions), on both the strings, and alphabet by 5 letters then will the collision frequency remain the same? What if we shift first string by 3 letters and second by 5?

<details class="solution" id="q-61-solution" markdown>
<summary>Solution</summary>

Applying the Caesar cipher to both strings by shifting each letter by the same amount will not change the collision frequency. This is because the relative positions of the characters within each string remain the same, only their actual representations change.

However, if we shift the first string by a different amount than the second string, it will affect the collision frequency. This is because the relative positions of characters within each string will change, leading to a different distribution of characters and hence a different collision frequency.
</details>

### Question 62 {: #q-62 .question .unit }

<span class="question__badge">Q62</span>

Suggest any such method using which we can be confident that the encoded text can't be decoded by the enemy. (We may discuss it in further classes)

<details class="solution" id="q-62-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

<div class="project-card" id="project-1">
<span class="kicker">Project 01</span>

### Vigenère Cipher

**Implement the breaking of the Vigenère Cipher.**

You should read the first 2 chapters of *The Code Book* and upload a two page report (not compulsory to upload the report). You cannot execute the following code without reading this book. The book is fun to read.

1. Import `string` and understand the different functions.
2. After assigning `s='rupnagar'`, understand what `s.find` and `s.replace` do. Also try looking at other functions and have a working knowledge of a few functions that make sense to you.
3. Understand how one can read a text file from your hard disk and store it as a string. The following two lines open a file and assign its content to the string `s`:

    ```python
    f = open('filename')
    s = f.read()
    ```

4. Understand the idea of *dictionaries* in Python. They are similar to lists but very powerful structures.
5. You are given the file `english_random`. You can consider any other big text file with english words, preferably a story book. Learn about the Vigenère Cipher. Encode the text using it.
6. Write a code which takes the encrypted string as input and returns the decrypted string as well as the password. Download this Python file and fill in the functions one by one.
</div>

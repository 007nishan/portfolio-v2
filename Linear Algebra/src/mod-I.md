<section class="opener" id="mod-I">
<span class="chapter-num">I</span>

# Module I — Bayes, Perceptrons & Sigmoid
<span class="accent-rule"></span>
</section>

### Question 82 {: #q-82 .question .unit }

<span class="question__badge">Q82</span>

Do you know the idea of equally likely events? What are these? Can you think of any event which is not equally likely?

<details class="solution" id="q-82-solution" markdown>
<summary>Solution</summary>

Equally likely events are events that have the same probability of occurring. When we say that events are equally likely, it means that each event has the same chance or likelihood of happening. For instance, coin toss, rollong a fair die, choosing a card from a deck of well-shuffled cards.

An example of events not being equally likely may include result of sport games, which depends on various factors like relative strangths of the teams, the condition of the field, etc.
</details>

### Question 83 {: #q-83 .question .unit }

<span class="question__badge">Q83</span>

You are given two coins. What is the probability that one head and one tail shows up on tossing?

<details class="solution" id="q-83-solution" markdown>
<summary>Solution</summary>

To determine the probability of getting one head and one tail when tossing two coins, we need to consider all possible outcomes and then identify the outcomes that match the desired event (one head and one tail).

When tossing two coins, each coin can land on heads (H) or tails (T). Therefore, the possible outcomes are:

- (H, H)
- (H, T)
- (T, H)
- (T, T)

We are interested in the outcomes where there is one head and one tail. These outcomes are:

- (H, T)
- (T, H)

The probability $P$ of an event is given by the ratio of the number of favorable outcomes to the total number of outcomes.

$$P(\text{one head and one tail}) = \frac{\text{Number of favorable outcomes}}{\text{Total number of outcomes}} = \frac{2}{4} = \frac{1}{2}$$
</details>

### Question 84 {: #q-84 .question .unit }

<span class="question__badge">Q84</span>

In a class in which all students practise at least one sport, 60% of students play soccer or basketball and 10% practice both sports. If there is also 60% that do not play soccer, calculate the probability that a student chosen at random from the class:

- Plays soccer only.
- Play basketball only.
- Plays only one of the sports.
- Plays neither soccer nor basketball.

<details class="solution" id="q-84-solution" markdown>
<summary>Solution</summary>

To solve this problem, we can use the principle of inclusion-exclusion and basic probability rules.

Given Data:

- Let $S$ represent the set of students who play soccer.
- Let $B$ represent the set of students who play basketball.
- $P(S \cup B) = 0.60$ (60% of students play soccer or basketball)
- $P(S \cap B) = 0.10$ (10% of students play both sports)
- $P(S') = 0.60$ (60% of students do not play soccer)

**1. Probability that a student plays soccer only:** $P(S \setminus B)$.

$$P(S \setminus B) = P(S) - P(S \cap B)$$

Since $P(S') = 0.60$, the probability of playing soccer, $P(S)$, is:

$$P(S) = 1 - P(S') = 1 - 0.60 = 0.40$$

Therefore:

$$P(S \setminus B) = P(S) - P(S \cap B) = 0.40 - 0.10 = 0.30$$

**2. Probability that a student plays basketball only:** $P(B \setminus S)$.

$$P(B \setminus S) = P(B) - P(S \cap B)$$

We need to find $P(B)$. Using the principle of inclusion-exclusion for $P(S \cup B)$:

$$P(S \cup B) = P(S) + P(B) - P(S \cap B)$$

Given $P(S \cup B) = 0.60$:

$$0.60 = 0.40 + P(B) - 0.10 \implies 0.60 = 0.30 + P(B) \implies P(B) = 0.30$$

Therefore:

$$P(B \setminus S) = P(B) - P(S \cap B) = 0.30 - 0.10 = 0.20$$

**3. Probability that a student plays only one of the sports:** $P((S \setminus B) \cup (B \setminus S))$.

$$P((S \setminus B) \cup (B \setminus S)) = P(S \setminus B) + P(B \setminus S) = 0.30 + 0.20 = 0.50$$

**4. Probability that a student plays neither soccer nor basketball:**

$$P((S \cup B)') = 1 - P(S \cup B) = 1 - 0.60 = 0.40$$

Summary of Probabilities:

- Plays soccer only: $0.30$
- Plays basketball only: $0.20$
- Plays only one of the sports: $0.50$
- Plays neither soccer nor basketball: $0.40$
</details>

### Question 85 {: #q-85 .question .unit }

<span class="question__badge">Q85</span>

Imagine you are writing your semester exams. To write an exam, there are 70% chances that an alarm clock will wake you up successfully. If you hear the alarm clock then there are 95% chances you will write the exam and if you don't hear the alarm the chances are 50%.

a) If you have written the exam what are the chances that you heard the alarm clock?

b) What are the chances that you didn't hear the alarm if you have not written the exam?

<details class="solution" id="q-85-solution" markdown>
<summary>Solution</summary>

Let's denote:

- A: event that you hear the alarm clock.
- B: event that you write the exam.

Given:

- P(A) = 0.7 (probability of hearing the alarm)
- P(B|A) = 0.95 (probability of writing the exam given you heard the alarm)
- P(B|¬A) = 0.5 (probability of writing the exam given you didn't hear the alarm)

(a) To find the probability that you heard the alarm clock given that you wrote the exam, we can use Bayes' theorem:

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

First, we need to find $P(B)$:

$$P(B) = P(B|A) \cdot P(A) + P(B|¬A) \cdot P(¬A) = 0.95 \times 0.7 + 0.5 \times (1-0.7) = 0.665 + 0.15 = 0.815$$

Now, we can calculate $P(A|B)$:

$$P(A|B) = \frac{0.95 \times 0.7}{0.815} \approx \frac{0.665}{0.815} \approx 0.816$$

So, the probability that you heard the alarm clock given that you wrote the exam is approximately 81.6%.

(b) To find the probability that you didn't hear the alarm if you didn't write the exam:

$$P(¬A|¬B) = \frac{P(¬B|¬A) \cdot P(¬A)}{P(¬B)}$$

We know:

$$P(¬B|¬A) = 1 - P(B|¬A) = 1 - 0.5 = 0.5$$

$$P(¬A) = 1 - P(A) = 1 - 0.7 = 0.3$$

$$P(¬B) = 1 - P(B) = 1 - 0.815 = 0.185$$

Now we can calculate $P(¬A|¬B)$:

$$P(¬A|¬B) = \frac{0.5 \times 0.3}{0.185} \approx \frac{0.15}{0.185} \approx 0.811$$

So, the probability that you didn't hear the alarm if you didn't write the exam is approximately 81.1%.
</details>

### Question 86 {: #q-86 .question .unit }

<span class="question__badge">Q86</span>

Lets say an investment company "Future Wealth" analyses stocks and predicts whether their price will go up or down. So far, half of the stocks analysed by the company have gone up, 3/4 of the stocks that went up were correctly predicted to go up, and 2/5 of the stocks that went down were incorrectly predicted to go up. Suppose that the company tells you that it will go up. Compute the probability that the stock will indeed go up.

<details class="solution" id="q-86-solution" markdown>
<summary>Solution</summary>

To solve this problem, we can use Bayes' Theorem. Let's define the following events:

- $U$: The stock price goes up.
- $D$: The stock price goes down.
- $P$: The company predicts that the stock price will go up.

Given data:

- $P(U) = 0.5$ (half of the stocks have gone up)
- $P(P \mid U) = \frac{3}{4}$ (3/4 of the stocks that went up were correctly predicted to go up)
- $P(P \mid D) = \frac{2}{5}$ (2/5 of the stocks that went down were incorrectly predicted to go up)

We need to compute $P(U \mid P)$, the probability that the stock price will go up given that the company predicts it will go up.

Using Bayes' Theorem:

$$P(U \mid P) = \frac{P(P \mid U) \cdot P(U)}{P(P)}$$

First, we need to find $P(P)$, the total probability that the company predicts the stock will go up. This can be calculated using the law of total probability:

$$P(P) = P(P \mid U) \cdot P(U) + P(P \mid D) \cdot P(D)$$

Given:

- $P(U) = 0.5$
- $P(D) = 1 - P(U) = 0.5$
- $P(P \mid U) = \frac{3}{4} = 0.75$
- $P(P \mid D) = \frac{2}{5} = 0.4$

Substitute these values into the equation for $P(P)$:

$$P(P) = 0.75 \cdot 0.5 + 0.4 \cdot 0.5 = 0.375 + 0.2 = 0.575$$

Now, use Bayes' Theorem to find $P(U \mid P)$:

$$P(U \mid P) = \frac{0.75 \cdot 0.5}{0.575} = \frac{0.375}{0.575} \approx 0.6522$$

So, the probability that the stock will indeed go up given that the company predicts it will go up is approximately $0.6522$ or $65.22\%$.
</details>

### Question 87 {: #q-87 .question .unit }

<span class="question__badge">Q87</span>

Imagine you are a bettor. You are watching a race between two horses A and B. Let's say five races are conducted. Construct any three hypotheses defining winning probabilities of A and B. What confidence do you have in each of your hypotheses to be true? Lets say, out of 5 races A wins 3 and B wins the remaining 2 (AAABB). Then after 5 races, in which of your hypotheses will you have maximum confidence. As per your new hypothesis which horse has more chances to win the 6th round.

<details class="solution" id="q-87-solution" markdown>
<summary>Solution</summary>

Sure, let's create three hypotheses about the winning probabilities of horses A and B:

1. Hypothesis 1: A is the stronger horse.
    - Confidence: Moderate
    - In this hypothesis, I believe that horse A has a higher probability of winning each race compared to horse B.
2. Hypothesis 2: B is the stronger horse.
    - Confidence: Moderate
    - Here, I assume that horse B has a higher probability of winning each race compared to horse A.
3. Hypothesis 3: A and B have equal chances of winning.
    - Confidence: Low
    - This hypothesis suggests that both horses have an equal probability of winning each race.

After observing the outcomes of the 5 races (A wins 3, B wins 2), my confidence level in each hypothesis shifts:

1. Hypothesis 1: A is the stronger horse.
    - Increased Confidence: High
    - Since horse A won more races, I'm more confident in this hypothesis being true.
2. Hypothesis 2: B is the stronger horse.
    - Decreased Confidence: Very Low
    - With B winning fewer races, my confidence in this hypothesis decreases.
3. Hypothesis 3: A and B have equal chances of winning.
    - Decreased Confidence: Low
    - Given the unequal outcomes, this hypothesis seems less likely.

Given that Hypothesis 1 now has the highest confidence, I'd predict that in the 6th round, horse A would have a higher chance of winning.
</details>

### Question 88 {: #q-88 .question .unit }

<span class="question__badge">Q88</span>

You're training a spam filter. You have data on the frequency of certain words in both spam and non-spam emails. How would you update your beliefs about an email being spam or not spam based on the presence of specific words? Let's say initially chances of an email being spam is 40%. Data: Word "free" appears in 80% of spam emails and 5% of non-spam emails.

<details class="solution" id="q-88-solution" markdown>
<summary>Solution</summary>

To update my beliefs about an email being spam or not spam based on the presence of specific words, such as "free," I would use Bayesian inference.

Given the initial probability of an email being spam ($P(\text{Spam}) = 0.4$), I can calculate the updated probability using Bayes' theorem:

$$P(\text{Spam}|\text{word "free"}) = \frac{P(\text{word "free"}|\text{Spam}) \times P(\text{Spam})}{P(\text{word "free"})}$$

Where:

- $P(\text{Spam}|\text{word "free"})$ is the probability that an email is spam given the word "free" is present.
- $P(\text{word "free"}|\text{Spam}) = 0.8$ is the probability of the word "free" appearing in spam emails.
- $P(\text{Spam}) = 0.4$ is the initial probability of an email being spam.

The overall probability of the word "free" appearing in all emails can be calculated as:

$$P(\text{word "free"}) = P(\text{word "free"}|\text{Spam}) \times P(\text{Spam}) + P(\text{word "free"}|\text{Non-Spam}) \times P(\text{Non-Spam})$$

Given that the word "free" appears in 80% of spam emails and 5% of non-spam emails, let's calculate $P(\text{word "free"})$:

$$P(\text{word "free"}) = (0.8 \times 0.4) + (0.05 \times 0.6) = 0.32 + 0.03 = 0.35$$

Now, we can use Bayes' theorem to update the probability of an email being spam given the word "free" is present:

$$P(\text{Spam}|\text{word "free"}) = \frac{0.8 \times 0.4}{0.35} \approx 0.914$$

So, if the word "free" is present in an email, the updated probability of that email being spam is approximately 91.4%.
</details>

### Question 89 {: #q-89 .question .unit }

<span class="question__badge">Q89</span>

Suppose that we use a perceptron to detect spam messages. Let's say that each email message is represented by the frequency of occurrence of keywords, and the output is +1 if the message is considered spam.

a) Can you think of some keywords that will end up with a large number of positive weight in the perceptron?

b) How about keywords that will get a negative weight?

c) What parameters in the perceptron directly affects how many border-line messages end up being classified as spam?

<details class="solution" id="q-89-solution" markdown>
<summary>Solution</summary>

(a) Keywords that are frequently associated with spam messages are likely to end up with large positive weights in the perceptron. Some examples of such keywords could be: "free", "discount", "limited offer", "click here", "urgent", "guaranteed", "cash", "prize", "win", "money", "call now", "buy now", "order now", etc. These words often appear in promotional or phishing emails, which are typically classified as spam.

(b) Conversely, keywords that are commonly found in non-spam messages and are indicative of legitimate communication are likely to get negative weights in the perceptron. Examples of such keywords could include: "important", "meeting", "schedule", "invoice", "receipt", "conference", "report", "agenda", "project", "proposal", "contact", "thank you", "best regards", etc.

(c) The parameter in the perceptron that directly affects how many borderline messages end up being classified as spam is the bias term. The bias term determines the threshold for the perceptron's decision boundary. If the bias term is set too low, more messages will be classified as spam, including some borderline ones. Conversely, if the bias term is set too high, fewer messages will be classified as spam, potentially missing some actual spam messages. Adjusting the bias term allows for fine-tuning the trade-off between false positives and false negatives in the classification task.
</details>

### Question 90 {: #q-90 .question .unit }

<span class="question__badge">Q90</span>

Lets have some parameters 3.1, 4.2 and 4 and the corresponding weights 5, 1, and 3 respt. Calculate the weighted sum.

<details class="solution" id="q-90-solution" markdown>
<summary>Solution</summary>

To calculate the weighted sum given the parameters and corresponding weights, we multiply each parameter by its corresponding weight and then sum the results.

Given:

- Parameter 1: 3.1, Weight: 5
- Parameter 2: 4.2, Weight: 1
- Parameter 3: 4, Weight: 3

The weighted sum is calculated as follows:

$$\text{Weighted sum} = (3.1 \times 5) + (4.2 \times 1) + (4 \times 3) = 15.5 + 4.2 + 12 = 31.7$$

So, the weighted sum is 31.7.
</details>

### Question 91 {: #q-91 .question .unit }

<span class="question__badge">Q91</span>

Suppose you have set of numbers ranging from -infinity to infinity. Will it be easy to plot them in a limited screen size and compare them?

<details class="solution" id="q-91-solution" markdown>
<summary>Solution</summary>

Plotting a set of numbers ranging from negative to positive infinity can be challenging due to the vast range of values involved. Even if you narrow down the range to a finite interval, such as from -1000 to 1000, the sheer number of data points may make it difficult to visualize and compare them effectively on a limited screen size.
</details>

### Question 92 {: #q-92 .question .unit }

<span class="question__badge">Q92</span>

Will simply dividing them by some large number work?

<details class="solution" id="q-92-solution" markdown>
<summary>Solution</summary>

No, it won't work as the points might start overlapping as they may be too big that the closer points come too much closer and start to overlap.
</details>

### Question 93 {: #q-93 .question .unit }

<span class="question__badge">Q93</span>

Can you think of a way to fit these numbers in some finite range? Think about some kind of functions?

<details class="solution" id="q-93-solution" markdown>
<summary>Solution</summary>

One approach to fitting an infinite range of numbers into a finite range is to use a transformation function. Using sigmoid or similar functions can be effective in fitting a wide range of numbers into a finite range. The sigmoid function, for example, has a characteristic S-shaped curve that maps input values to an output range between 0 and 1. The sigmoid function can be represented by the formula:

$$f(x) = \frac{1}{1 + e^{-x}}$$

Where:

- $f(x)$ is the output of the sigmoid function for input $x$.
- $e$ is the base of the natural logarithm, approximately equal to 2.71828.
- $x$ is the input value.

You can use this function to map input values to an output range between 0 and 1, which can be useful for various data transformation tasks.
</details>

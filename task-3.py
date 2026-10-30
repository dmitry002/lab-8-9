import nltk
from nltk.corpus import *
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import matplotlib.pyplot as plt

nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download('wordnet')

print(gutenberg.fileids())

emma = nltk.corpus.gutenberg.words('austen-emma.txt')

words_count = len(emma)
unique_count = len(set(emma))

print("\nКількість слів у тексті:")
print(words_count)

print("\nКількість унікальних слів у тексті:")
print(unique_count)

print("\nУнікальних слів менше у", round(words_count / unique_count, 2), "раз")
print("Унікальні слова становлять", round(unique_count / words_count * 100, 2), "% від усіх слів")

fdist = FreqDist(emma)
top_ten = fdist.most_common(10)

print("\n10 найбільш вживаних слів:")
print(top_ten)

words = [w for w, c in top_ten]
counts = [c for w, c in top_ten]

plt.figure(figsize=(10, 5))
plt.bar(words, counts)
plt.title("10 найбільш вживаних слів (austen-emma.txt)")
plt.xlabel("Слово")
plt.ylabel("Кількість")
plt.show()

stop_words = set(stopwords.words("english"))

without_stop_words = [
    word for word in emma
    if word.lower() not in stop_words
]

print("\nТекст після видалення стоп-слів:")
print(without_stop_words[:20])

table = str.maketrans('', '', string.punctuation)

stripped = [
    word.translate(table).lower()
    for word in without_stop_words
]

stripped = [
    word for word in stripped
    if word.isalpha()
]

fdist = FreqDist(stripped)
top_ten = fdist.most_common(10)

print("\n10 найбільш вживаних слів після видалення стоп-слів та пунктуації:")
print(top_ten)

words = [w for w, c in top_ten]
counts = [c for w, c in top_ten]

plt.figure(figsize=(10, 5))
plt.bar(words, counts, color='green')
plt.title("10 найбільш вживаних слів після видалення стоп-слів та пунктуації")
plt.xlabel("Слово")
plt.ylabel("Кількість")
plt.show()

lemmatizer = WordNetLemmatizer()

lemmas = [
    lemmatizer.lemmatize(word)
    for word in stripped
]

fdist = FreqDist(lemmas)
top_ten = fdist.most_common(10)

print("\n10 найбільш вживаних слів після лематизації:")
for word, count in top_ten:
    print(word, "-", count)
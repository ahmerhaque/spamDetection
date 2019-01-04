import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score
import _pickle as c


def save(clf, name):
    with open(name, 'wb') as fp:
        c.dump(clf, fp)
    print ("saved")


def make_dict():
    direc = "emails/"
    files = os.listdir(direc)
    dictionary=[]
    emails = [direc + email for email in files]
    words = []
    c = len(emails)
    # print(emails)
    for email in emails:
        # print(email)
        f = open(email, errors='ignore')
        blob = f.read()
        words += blob.split(" ")
        print(c)
        c -= 1
    for i in range(len(words)):
        if not words[i].isalpha():
            words[i]= ""
    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(3000)
def make_dataset(dictionary):
    direc = "emails/"
    files = os.listdir(direc)

    emails = [direc + email for email in files]
    words = []

    feature_set=[]
    labels=[]
    c = len(emails)
    for email in emails:
        data = []
        f=open(email, errors='ignore')
        words=f.read().split(' ')
        # print(words)

        for entry in dictionary:

            data.append(words.count(entry[0]))

        feature_set.append(data)
        if "ham" in email:
            labels.append(0)
        if "spam" in email:
            labels.append(1)
        # print(c)
        c-=1
        # print(feature_set,labels)

    return feature_set,labels
d=make_dict()

features,labels=make_dataset(d)

x_train, x_test, y_train, y_test = tts(features, labels, test_size=0.2)

clf = MultinomialNB()     
clf.fit(x_train, y_train)

preds = clf.predict(x_test)
print (accuracy_score(y_test, preds))

while True:
    features = []
    inp = input("enter a text:").split()
    if inp[0] == "exit":
        break
    for word in d:
        features.append(inp.count(word[0]))
    res = clf.predict([features])
    print(["Not Spam", "Spam !"][res[0]])
    break
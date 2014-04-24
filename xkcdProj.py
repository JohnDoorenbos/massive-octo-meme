from flask import Flask, render_template, request
import re
import random
def isOptimized(string):
    leftLetters = "asdfqwerzxcvgt"
    rightLetters = "poiuylkjhgmb"
    alternating = 0.0
    previous = ""
    for i in string:
        if i in leftLetters:
            current = leftLetters
        else:
            current = rightLetters
        if current != previous:
            alternating += 1.0
        
        previous = current
    return alternating/len(string) > .80
app = Flask(__name__)

@app.route("/display")
def display(): #what are you doing that requires "saved"information as function parameters
    matchedWords = []
    passPhraseList = []

    minLength = request.args.get("minWord", "")
    maxLength = request.args.get("maxWord", "")
    if str(request.args.get("maxPhrase", "")) =="":
        maxPhraseLength = 10000
    else:
        maxPhraseLength = int(str(request.args.get("maxPhrase", "")))
    optimize = request.args.get("optimize", "")
    #print(request.args.get("substitutions" , ""))
    
    f = open("wordlist.txt",'r')

    #find all words that match the minimum and maximum length requirement
    for line in f:
        if re.match("^.{"+minLength +","+maxLength+"}$",line):
            if optimize:
                #print(line.strip())
                #print(isOptimized(line.strip()))
                if isOptimized(line.strip()):
                    
                    matchedWords.append(line.strip())
            else:
                matchedWords.append(line.strip())
            
    #start creating a list of passPhrases
    while(len(passPhraseList) < 10):
        tempPhrase = ""
        for x in range(4):
            tempPhrase += matchedWords[random.randrange(0,len(matchedWords))] +" "
        if len(tempPhrase) < maxPhraseLength:
            passPhraseList.append(tempPhrase)
    

            
    #Substitutions


    for key in request.args:
        #print(request.args)
        if re.match("sub[a-z]", key):
            replacement = str(request.args.get(key, ""))
            print(replacement, " ", key[3])
            #for phrase in passPhraseList:
            x =0
            res = []
            while(x<10) :
                
                
                print(len(passPhraseList))
                phrase = passPhraseList[x]
                print(phrase)
                
                if key[3] in phrase:
                    newPhrase = phrase.replace(key[3], replacement,1)
                    res.append(newPhrase)
                else:
                    res.append(phrase)
                    
                print(res)
                x += 1    
            passPhraseList = res[:]

    #Capitalizations
    for key in request.args:
        if re.match("cap[0-3]", key):
            replacement = str(request.args.get(key, ""))
            i = 0
            
            while (i < 10):
                phrase = passPhraseList[i]
            
                words = phrase.split(" ")
                cap = words[int(key[3])].capitalize()
                words[int(key[3])] = cap
                res = ""
                for word in words:
                    res += word + " "
                    
                print(words)
                passPhraseList[i] = res
                i += 1
    return render_template('display.html', lst =passPhraseList)
@app.route("/xkcd")
def hello():
    return render_template('xkcd.html')

if __name__ == '__main__':
    app.run(debug=True)


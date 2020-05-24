# =============================================================================
# Word Search Generator
# Created by Josh Humphries May 2020
# =============================================================================

import math
import random
import string

class WordSearch:
    """Holds word search matrix in letterArray, as well as methods that 
    generate the matrix."""
    
    def buildArray(self, size):
        """Generates word matrix based on size. size comes from user input"""
        
        self.letterArray = [[random.choice(string.ascii_uppercase) for x in range(size)] for y in range(size)]
        self.size = size
        
        #Number of hidden words is a function of size
        numWordsToFind = math.floor(((1/4)*size)**(12/7))
        
        dictionary = []
        self.wordsToFind = []
        self.hiddenArray = [['.' for x in range(size)] for y in range(size)]
        self.wordsAdded = []
        self.wordLocations = {}
        
        with open("Dictionary.txt") as file:
            for line in file:
                if len(line) <= size:
                    dictionary.append(line.strip().upper())
        
        for i in range (numWordsToFind):
            self.wordsToFind.append(random.choice(dictionary))
        
        #Less runtime to place longer words early, move them to front of list
        self.wordsToFind.sort(key=len, reverse=True)
        
        #Loop to randomly place words. Loop attempts to place words that
        #overlap already-placed words. Loop continues until either all words 
        #are placed or count has reached 4*numWordsToFind. This is to prevent 
        #infinite loops if word placement is impossible. 
        count = 0
        while self.wordsToFind and count < 4*numWordsToFind:
            for word in self.wordsToFind[:]:
                if not self.wordsAdded:
                    if self.genRandomPlacement(word):
                        self.wordsToFind.remove(word)
                        continue
                else:
                    if random.randint(1,10) < 4:
                        if self.genOverlapPlacement(word):
                            self.wordsToFind.remove(word)
                            continue
                    else:
                        if self.genRandomPlacement(word):
                            self.wordsToFind.remove(word)
                            continue
            count += 1
            continue
        
        print('\n'.join([''.join(['{:2}'.format(item) for item in row]) 
      for row in self.letterArray]))
        print('\n')
        print('\n'.join([''.join(['{:2}'.format(item) for item in row]) 
      for row in self.hiddenArray]))
        print(self.wordsToFind)
        print(self.wordsAdded)

            
    def genRandomPlacement(self, word):
        """Generates random placement of words in the letter matrix. Makes
        50 attempts to place the word - if it cannot, returns False."""
        
        count = 0
        
        while count < 50:
            
            #direction the word is placed is randomly chosen first
            direction = random.randint(1,8)
            
            #based on direction, only the possible locations where the first
            #letter of the word can be placed and the word will not extend 
            #outside of the matrix are chosen from
            if direction == 1:
                #choose random start row
                row = random.randint(len(word) - 1, len(self.letterArray) - 1)
                #choose random start column
                column = random.randint(len(word) - 1, len(self.letterArray) - 1)
                    
            elif direction == 2:
                row = random.randint(len(word) - 1, len(self.letterArray) - 1)
                column = random.randint(0, len(self.letterArray) - 1)
                    
            elif direction == 3:
                row = random.randint(len(word) - 1, len(self.letterArray) - 1)
                column = random.randint(0, len(self.letterArray) - len(word) - 1)
                    
            elif direction == 4:
                row = random.randint(0, len(self.letterArray) - 1)
                column = random.randint(0, len(self.letterArray) - len(word) - 1)
                    
            elif direction == 5:
                row = random.randint(0, len(self.letterArray) - len(word) - 1)
                column = random.randint(0, len(self.letterArray) - len(word) - 1)
                    
            elif direction == 6:
                row = random.randint(0, len(self.letterArray) - len(word) - 1)
                column = random.randint(0, len(self.letterArray) - 1)
                    
            elif direction == 7:
                row = random.randint(0, len(self.letterArray) - len(word) - 1)
                column = random.randint(len(word) - 1, len(self.letterArray) - 1)
                    
            elif direction == 8:
                row = random.randint(0, len(self.letterArray) - 1)
                column = random.randint(len(word) - 1, len(self.letterArray) - 1)
                
            if self.checkValidPlacement(word, direction, row, column):
                self.placeWord(word, direction, row, column)
                return True
            else:
                count += 1
                continue
            
        return False #If genRandomPlacement was unable to place word, return False
   
# =============================================================================
#     genRandomPlacement alone places most of the words in a similar direction 
#     after the first few words are placed, as random placement of overlapping 
#     words is too uncommon. genOverlapPlacement helps diversify the direction
#     words are placed and increases number of words that overlap one another.
# =============================================================================
                
    def genOverlapPlacement(self, word):
        """Attempts to place words that overlap other already-placed words.
        Makes 30 attempts to place word, otherwise returns False"""
        
        count = 0
        
        while count < 30:
            #Chooses letter from word to be placed to try to overlap
            overlapLetterIndex = random.randint(0, len(word) - 1)
            overlapLetter = word[overlapLetterIndex]
            matchingCoords = []
            
            #Creats a list of tuples of all coordinates with letter that
            #matches the randomly chosen letter
            for i, row in enumerate(self.hiddenArray):
                for j, column in enumerate(self.hiddenArray):
                    if self.hiddenArray[i][j] == overlapLetter:
                        matchingCoords.append((i,j))
        
            
            if not matchingCoords:
                count += 1
                continue;
            elif len(matchingCoords) == 1:
                row, column = matchingCoords[0]
            else:
                row, column = random.choice(matchingCoords)
            
            direction = random.randint(1,8)
            
            if direction == 1:
                startingRow = row + overlapLetterIndex
                startingColumn = column + overlapLetterIndex
                
            elif direction == 2:
                startingRow = row + overlapLetterIndex
                startingColumn = column
            
            elif direction == 3:
                startingRow = row + overlapLetterIndex
                startingColumn = column - overlapLetterIndex
            
            elif direction == 4:
                startingRow = row
                startingColumn = column - overlapLetterIndex
                
            elif direction == 5:
                startingRow = row - overlapLetterIndex
                startingColumn = column - overlapLetterIndex
                
            elif direction == 6:
                startingRow = row - overlapLetterIndex
                startingColumn = column
                
            elif direction == 7:
                startingRow = row - overlapLetterIndex
                startingColumn = column + overlapLetterIndex
                
            elif direction == 8:
                startingRow = row
                startingColumn = column + overlapLetterIndex
                
            if self.checkValidPlacement(word, direction, startingRow, startingColumn):
                self.placeWord(word, direction, startingRow, startingColumn)
                return True
            
            else:
                count += 1
                continue
            
        return False #If genOverlapPlacement was unable to place word, return False
    
    
    def checkValidPlacement(self, word, direction, row, column):
        """Checks if generated placement of word is valid. Returns False
        if invalid."""
        
        if (row < 0 or column < 0 or column >= self.size or row >= self.size):
            return False
        
        elif direction == 1:
            for i, letter in enumerate(word):
                if row - i < 0 or column - i < 0:
                    return False
                if (self.hiddenArray[row - i][column - i] != '.' and 
                    self.hiddenArray[row - i][column - i] != letter):
                    return False
                    
        elif direction == 2:
            for i, letter in enumerate(word):
                if row - i < 0:
                    return False
                if (self. hiddenArray[row - i][column] != '.' and 
                    self.hiddenArray[row - i][column] != letter):
                    return False
                
                
        elif direction == 3:
            for i, letter in enumerate(word):
                if row - i < 0 or column + i >= self.size:
                    return False
                if (self.hiddenArray[row - i][column + i] != '.' and 
                    self.hiddenArray[row - i][column + i] != letter):
                    return False
                
        elif direction == 4:
            for i, letter in enumerate(word):
                if column + i >= self.size:
                    return False
                if (self.hiddenArray[row][column + i] != '.' and 
                    self.hiddenArray[row][column + i] != letter):
                    return False

        elif direction == 5:
            for i, letter in enumerate(word):
                if row + i >= self.size or column + i >= self.size:
                    return False
                if (self.hiddenArray[row + i][column + i] != '.' 
                    and self.hiddenArray[row + i][column + i] != letter):
                    return False
                
        elif direction == 6:
            for i, letter in enumerate(word):
                if row + i >= self.size:
                    return False
                if (self.hiddenArray[row + i][column] != '.' 
                    and self.hiddenArray[row + i][column] != letter):
                    return False
                
        elif direction == 7:
            for i, letter in enumerate(word):
                if row + i >= self.size or column - i < 0:
                    return False
                if (self.hiddenArray[row + i][column - i] != '.' 
                    and self.hiddenArray[row + i][column - i] != letter):
                    return False
                
        elif direction == 8:
            for i, letter in enumerate(word):
                if column - i < 0:
                    return False
                if (self.hiddenArray[row][column - i] != '.' and 
                    self.hiddenArray[row][column - i] != letter):
                    return False
                
        return True


    def placeWord(self, word, direction, row, column):
        """Places word in word matrix after valid location generated"""
        coordPairs = []
        
        if direction == 1:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row - i][column - i] = letter
                self.hiddenArray[row - i][column - i] = letter
                coordPairs.append((row - i, column - i))
            self.wordLocations[word] = coordPairs
                
        if direction == 2:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row - i][column] = letter
                self.hiddenArray[row - i][column] = letter
                coordPairs.append((row - i, column))
            self.wordLocations[word] = coordPairs
                
        if direction == 3:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row - i][column + i] = letter
                self.hiddenArray[row - i][column + i] = letter
                coordPairs.append((row - i, column + i))
            self.wordLocations[word] = coordPairs
                
        if direction == 4:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row][column + i] = letter
                self.hiddenArray[row][column + i] = letter
                coordPairs.append((row, column + i))
            self.wordLocations[word] = coordPairs
                
        if direction == 5:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row + i][column + i] = letter
                self.hiddenArray[row + i][column + i] = letter
                coordPairs.append((row + i, column + i))
            self.wordLocations[word] = coordPairs
                
        if direction == 6:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row + i][column] = letter
                self.hiddenArray[row + i][column] = letter
                coordPairs.append((row + i, column))
            self.wordLocations[word] = coordPairs
                
        if direction == 7:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row + i][column - i] = letter
                self.hiddenArray[row + i][column - i] = letter
                coordPairs.append((row + i, column - i))
            self.wordLocations[word] = coordPairs
                
        if direction == 8:
            self.wordsAdded.append(word)
            for i, letter in enumerate(word):
                self.letterArray[row][column - i] = letter
                self.hiddenArray[row][column - i] = letter
                coordPairs.append((row, column - i))
            self.wordLocations[word] = coordPairs
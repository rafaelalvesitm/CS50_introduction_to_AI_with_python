import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count: # If the number of cells is equal to the count then all are mines
            return(self.cells)
        return None
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0: # if the count is 0 than all cells are safes
            return self.cells
        return None
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells: # If cell is in the list of cells for the setence
            self.cells.remove(cell) # Remove the cell from the list of cells
            self.count = self.count - 1 # Remove 1 from the count

        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells: # If cell is in the list of cells for the setence
            self.cells.remove(cell) # Remove the cell from the sentence
        #aise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Stage 1) mark the cell as a move that has been made
        self.moves_made.add(cell) # Add cell as a move made

        # Stage 2) mark the cell as safe
        self.mark_safe(cell) # DAdd a cell as a safe cell if not found a mine when clicking or moving with AI

        # Stage 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`

        cells_sentence = set() #Start an empty set for a new setence.

        #Loop to create each cell around the one clicked 
        
        for i in range(cell[0] - 1, cell[0] + 2): # 
            for j in range(cell[1] - 1, cell[1] + 2):
                 
                 # Ignore the cell itself
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width: # Check to se if the cell is inside the board
                    cells_sentence.add((i,j)) # Add the Tuple (i,j) to the new setence set. 
        
        self.knowledge.append(Sentence(cells_sentence, count))# Add a new setence fto the Knowledge base
        
        # Stage 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base

        for sentence in self.knowledge: # Loops for each sentence

            if sentence.known_safes() is not None: # If all safes
                for i in sentence.known_safes(): # for each cell in the tuple
                    self.safes.add(i)   # add safes to the knowledge of safe cell

            if sentence.known_mines() is not None: # if all mines
                for i in sentence.known_mines():  #for each cell   
                    self.mines.add(i) # Mark as a mine
        
        # Stage 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge

        for i in self.knowledge: # Loops for each sentence
            for j in self.knowledge: # Loops trhought each setence as well
                if j.cells == i.cells or j.cells == set(): # If the second sentence is the same or am empty set
                    break
                if j.cells.issubset(i.cells): # If the J sentence is a subset of the I setence 
                    i.cells.discard(j.cells)
                    i.count = i.count - j.count


        for i in self.safes: # Remove from each sentence the cells that are know to be safes
            self.mark_safe(i)
        for i in self.mines: # Remove from each sentence the cells that are know to be mines
            self.mark_mine(i)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in self.safes:
            if i not in self.moves_made and i not in self.mines:
                return i
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        i = random.randrange(self.height)
        j = random.randrange(self.width)
        if (i,j) not in self.moves_made:
            if (i,j) not in self.mines:
                return (i, j)
        return None
        

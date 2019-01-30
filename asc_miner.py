# constants
FREQ_THRES = 100

class Itemset:
    """
    -------------------------------------------------------
    Holds a set of items and the ids of the baskets where
    the every item in the Itemset is found together.
    -------------------------------------------------------
    """
    def __init__(self, contents, basket_ids=None):
        """
        -------------------------------------------------------
        Constructor
        Use: itemset = Itemset(contents)
        Use: itemset = Itemset(contents, basket_ids)
        -------------------------------------------------------
        Parameters:
            contents - a SORTED array of the items in the itemset 
                (arr of String)
            basket_ids - a SORTED List of the baskets where all
                items in the Itemset can be found.
        -------------------------------------------------------
        """
        self.contents = contents
        if basket_ids is None:
            self.basket_ids = List()
        else:
            self.basket_ids = basket_ids
        return

    def __eq__(self, other):
        if len(self.contents) != len(other.contents):
            return False

        for i in range(0, len(self.contents)):
            if self.contents[i] != other.contents[i]:
                return False

        return True

    def __lt__(self, other):
        lesser = min(len(self.contents), len(other.contents))
        for i in range(0, lesser):
            if (self.contents[i] >= other.contents[i]):
                return False

        return True      

    def __le__(self, other):
        lesser = min(len(self.contents), len(other.contents))
        for i in range(0, lesser):
            if (self.contents[i] > other.contents[i]):
                return False
        
        return True

    def __str__(self):
        return "[" + ", ".join(self.contents) + "]: " + str(len(self.basket_ids))

    def try_merge(self, other): 
        """
        -------------------------------------------------------
        Attempt to merge one Itemset with another, based on the
        apriori principle and k-1 X k-1 candidate generation.
        Use: merged, candidate = itemset1.try_merge(itemset2)
        -------------------------------------------------------
        Parameters:
            other - the other itemset.
        Returns:
            merged - True iff the merge passed successfully.
            candidate - the Itemset containing one more item
                than the two Itemsets that were merged to create
                it (if the merge passed successfully).
        -------------------------------------------------------
        """
        if (len(self.contents) != len(other.contents)):
            raise Exception("Itemsets with different content lengths cannot be merged!")

        # check that the two Itemsets have a common prefix of all but their last element, adding elements of the common prefix to combination.
        prefix_length = len(self.contents) - 1
        common = []
        for i in range(0, prefix_length):
            # once one item is unequal in the prefix, we know the Itemsets are incompatible for merge.
            if (self.contents[i] != other.contents[i]):
                return False, None
            else:
                common.append(self.contents[i])

        # append final items.
        common.append(self.contents[prefix_length])
        common.append(other.contents[prefix_length])

        # form and return new Itemset.
        merged_itemset = Itemset(common, self.basket_ids.intersection(other.basket_ids))
        return True, merged_itemset

    def add_basket(self, basket_id):
        """
        -------------------------------------------------------
        Add a basket id to the List of baskets where the 
        Itemset can be found. The basket_id must be greater
        than all basket ids already in the List.
        Use: itemset.add_basket(basket_id)
        -------------------------------------------------------
        Parameters:
            basket_id - the id of the basket where this itemset
                is found.
        -------------------------------------------------------
        """
        self.basket_ids.insert(basket_id)
        return

    def freq(self):
        """
        -------------------------------------------------------
        Get the number of baskets this Itemset appears in.
        Use: frequency = itemset.freq()
        -------------------------------------------------------
        Returns:
            frequency - the number of baskets the Itemset appears
                in.
        -------------------------------------------------------
        """
        return len(self.basket_ids)

class AVLNode:
    """
    -------------------------------------------------------
    A node of an AVLTree.
    -------------------------------------------------------
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def update_height(self):
        """
        -------------------------------------------------------
        Update the height of the AVLNode based on those of its
        children.
        Use: node.update_height()
        -------------------------------------------------------
        """
        left = 0
        right = 0
        if self.left is not None:
            left = self.left.height
        if self.right is not None:
            right = self.right.height
        self.height = max(left, right) + 1
        return

    def balance_factor(self):
        """
        -------------------------------------------------------
        Get the balance factor (left child height - right
        child height) of the AVLNode.
        Use: node.balance_factor()
        -------------------------------------------------------
        Returns:
            balance_factor - the balance factor.
        """
        left = 0
        right = 0
        if self.left is not None:
            left = self.left.height
        if self.right is not None:
            right = self.right.height
        return left - right

class AVL: 
    """
    -------------------------------------------------------
    An AVL tree.
    -------------------------------------------------------
    """
    def __init__(self):
        self.root = None
        self.count = 0
        return

    def __len__(self):
        return self.count
    
    def insert_find(self, value):
        """
        -------------------------------------------------------
        Seek the value requested and insert it if it cannot be
        found. Return the value found, either way.
        Use: found_value = avl_tree.insert_find(value)
        -------------------------------------------------------
        Parameters:
            value - the key for the search or value for insertion.
        Returns:
            found_value - the value found in the tree.
        -------------------------------------------------------
        """
        found_value = None
        if self.root is None:
            self.root = AVLNode(value)
            self.count += 1
            found_value = self.root.value
        else:
            inserted, self.root, found_value = self.insert_aux(self.root, value)
            if inserted:
                self.count += 1

        return found_value

    def insert_aux(self, node, value):
        """
        -------------------------------------------------------
        An auxiliary function for insert_find. Recursively seeks
        or inserts the value.
        Use: inserted, child, found_item = keyword_table(root, value)
        -------------------------------------------------------
        Parameters:
            root - the root of the sub-tree.
            value - the value to be found or inserted.
        Returns:
            inserted - True iff the value was inserted.
            child - the rebalanced child of the root.
            found_item - the value either found or inserted.
        -------------------------------------------------------
        """

        # assume no value was inserted or found to start.
        inserted = False
        found_value = None

        # check on which side the value belongs.
        if value < node.value:
            # belongs on left.
            if node.left is None:
                # insert on left.
                node.left = AVLNode(value)
                inserted = True
                found_value = node.left.value
            else:
                # seek on left.
                inserted, node.left, found_value = self.insert_aux(node.left, value)

        elif value > node.value:
            # belongs on right.
            if node.right is None:
                # insert on right.
                node.right = AVLNode(value)
                inserted = True
                found_value = node.right.value
            else:
                # seek on right.
                inserted, node.right, found_value = self.insert_aux(node.right, value)

        else:
            # found.
            inserted = False
            found_value = node.value

        # rebalance the subtree if needed.
        if inserted:
            node.update_height()
            balance_factor = node.balance_factor()
            if balance_factor > 1:
                # left-side dominated.
                left_balance_factor = node.left.balance_factor()
                if left_balance_factor > 0:
                    # left-left case.
                    node = self.right_rotate(node)
                else:
                    # left-right case.
                    node.left = self.left_rotate(node.left)
                    node = self.right_rotate(node)

            elif balance_factor < -1:
                # right-side dominated.
                right_balance_factor = node.right.balance_factor()
                if right_balance_factor < 0:
                    # right-right case.
                    node = self.left_rotate(node)
                else:
                    # right-left case.
                    node.right = self.right_rotate(node.right)
                    node = self.left_rotate(node)

        return inserted, node, found_value

    def right_rotate(self, node):
        """
        -------------------------------------------------------
        An auxiliary function for insert_aux typical of AVL
        trees.
        Use: node = tree.right_rotate(node)
        -------------------------------------------------------
        Parameters:
            node - the node that must rotate right.
        Returns:
            node - the node at the previous position of node
                after the rotation.
        -------------------------------------------------------
        """
        new_node = node.left
        node.left = new_node.right
        new_node.right = node
        
        node.update_height()
        new_node.update_height()
        return new_node
    
    def left_rotate(self, node):
        """
        -------------------------------------------------------
        An auxiliary function for insert_aux typical of AVL
        trees.
        Use: node = tree.left_rotate(node)
        -------------------------------------------------------
        Parameters:
            node - the node that must rotate let.
        Returns:
            node - the node at the previous position of node
                after the rotation.
        -------------------------------------------------------
        """
        new_node = node.right
        node.right = new_node.left
        new_node.left = node
        
        node.update_height()
        new_node.update_height()
        return new_node

    def to_list(self):
        """
        -------------------------------------------------------
        Convert an AVLTree into a linked List.
        Use: lst = tree.to_list()
        -------------------------------------------------------
        Returns:
            lst - the linked List conversion of the AVLTree, 
                sorted left to right.
        -------------------------------------------------------
        """
        lst = List()
        if self.root is not None:
            self.to_list_aux(lst, self.root)
        return lst

    def to_list_aux(self, lst, node):
        """
        -------------------------------------------------------
        And auxiliary function for to_list.
        Use: tree.to_list(lst, node)
        -------------------------------------------------------
        Parameters:
            lst - the linked List to be inserted into.
            node - the root of the subtree to be traversed for
                insertion.
        -------------------------------------------------------
        """

        # insert all left descendents.
        if node.left is not None:
            self.to_list_aux(lst, node.left)
        
        # insert self.
        lst.insert(node.value)

        # insert all right descendents.
        if node.right is not None:
            self.to_list_aux(lst, node.right)

class ListNode:
    """
    -------------------------------------------------------
    A Node for a linked List.
    -------------------------------------------------------
    """
    def __init__(self, value):
        self.value = value
        self.next = None

class List:
    """
    -------------------------------------------------------
    A linked List.
    -------------------------------------------------------
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def __str__(self):
        # add starting [
        ret_str = "[\n"

        # add first value.
        if self.head is not None:
            ret_str += str(self.head.value)
        
        # add all subsequent values (with commas).
        cur = self.head.next
        while cur is not None:
            ret_str += ",\n" + str(cur.value)
            cur = cur.next

        # add final ]
        ret_str += "\n]"
        return ret_str

    def insert(self, value):
        """
        -------------------------------------------------------
        Insert a value to the end of the List.
        Use: lst.insert(value)
        -------------------------------------------------------
        Parameters:
            value - the value to be inserted. Must be an Itemset.
        -------------------------------------------------------
        """
        if self.head is None:
            # insert first element.
            self.head = ListNode(value)
            self.tail = self.head
            self.length = 1
        else:
            # insert to rear.
            self.tail.next = ListNode(value)
            self.tail = self.tail.next
            self.length += 1

    def prune(self):
        """
        -------------------------------------------------------
        Remove all Itemsets from the List that do not appear
        in at least FREQ_THRES buckets.
        Use: list.prune()
        -------------------------------------------------------
        """

        if self.head is not None:

            # skip infrequent items at start.
            new_head = self.head
            while new_head is not None and len(new_head.value.basket_ids) < FREQ_THRES:
                self.length -= 1
                new_head = new_head.next 
            self.head = new_head

            # remove all other infrequent items.
            last_included = self.head
            if self.head is not None:
                cur = self.head.next
                while cur is not None:
                    if len(cur.value.basket_ids) < FREQ_THRES:
                        # skip cur.
                        self.length -= 1
                        last_included.next = cur.next
                    else:
                        last_included = cur
                    cur = cur.next

            # set new tail
            self.tail = last_included              

        return

    def next_freq_itemsets(self):
        """
        -------------------------------------------------------
        Generate a List of every frequent Itemset that contains 
        one more item than the Itemsets in the current List.
        Use: next_freq_itemsets = itemset.next_freq_itemsets()
        -------------------------------------------------------
        Returns:
            next_freq_itemsets - the List of frequent Itemsets
                containing one more item than the Itemsets in
                the current List.
        -------------------------------------------------------
        """
        
        new_candidates = List()

        curA = self.head # iterator for exteral loop.
        while curA is not None:
            curB = curA.next # iterator for internal loop.

            # when the first merge failure is found because a common prefix cannot be found, all
            # subsequent items in the inner loop will be incapable of producing a merge success.
            # This is because the itemsets are alphabetized.
            merge_success = True 
            while curB is not None and merge_success:

                # form a new candidate based on the k-1 X k-1 prefix rule.
                # Do not add candidate if the frequency of finding the two items together (calculated in 
                # the attempted merge) is insufficient.
                merge_success, candidate = curA.value.try_merge(curB.value)
                if merge_success and len(candidate.basket_ids) >= FREQ_THRES:
                    new_candidates.insert(candidate)
                curB = curB.next

            curA = curA.next

        return new_candidates

    def intersection(self, other):
        """
        -------------------------------------------------------
        Calculate the intersection of two SORTED Lists.
        Use: intersection = list.intersection(other)
        -------------------------------------------------------
        Parameters:
            other - the other List.
        Returns:
            intersection - a linked List containing a copy of
                every value common to both Lists (assuming
                they were both in sorted order).
        -------------------------------------------------------
        """

        intersection = List()

        # merge common elements together.
        s = self.head
        o = other.head 
        while s is not None and o is not None:
            if s.value < o.value:
                s = s.next
            elif o.value < s.value:
                o = o.next 
            else:
                intersection.insert(s.value)
                s = s.next
                o = o.next 

        return intersection

def main():
    # path = input("Please enter the absolute path to the file containing the dataset: ") # TODO include
    path = "C:\\Users\\Nathaniel\\Desktop\\CP421\\a1\\browsing.txt" # TODO remove

    # open file to log all frequent itemsets found.
    log = open("C:\\Users\\Nathaniel\\Desktop\\CP421\\cp421\\log.txt", "w", encoding="utf-8")
    log.write("")
    log = open("C:\\Users\\Nathaniel\\Desktop\\CP421\\cp421\\log.txt", "a", encoding="utf-8")

    try:
        # open file for reading.
        file = open(path, "r", encoding="utf-8")
        file.seek(0)

        item_tree = AVL() # hold all items (and their frequency).
        
        # read all lines, breaking orders into an array of items (sorted in alphabetical order).
        baskets = file.readlines()
        file.close()
        for basket_id in range(0, len(baskets)): #and basket_id < 500: # TODO remove number here.
            basket = baskets[basket_id].split()
            print("Reading line " + str(basket_id)) # status updates.

            # build up AVL tree containing every item once (along with the baskets it is found inside).
            for j in range(0, len(basket)):
                item = Itemset([basket[j]])
                found_item = item_tree.insert_find(item)
                found_item.add_basket(basket_id)
                
        # gather frequent singles.
        frequent_singles = item_tree.to_list()
        item_tree = None # data no longer needed.
        frequent_singles.prune()
        print("Found " + str(len(frequent_singles)) + " frequent singles.")
        log.write("Found the following " + str(len(frequent_singles)) + " frequent singles:") # log frequent singles to file.
        log.write(str(frequent_singles) + "\n\n")

        # gather frequent pairs.
        frequent_pairs = frequent_singles.next_freq_itemsets()
        print("Found " + str(len(frequent_pairs)) + " frequent pairs.")
        log.write("Found the following " + str(len(frequent_pairs)) + " frequent pairs:") # log frequent pairs to file.
        log.write(str(frequent_pairs) + "\n\n")

        # gather frequent triples.
        frequent_triples = frequent_pairs.next_freq_itemsets()
        print("Found " + str(len(frequent_triples)) + " frequent triples.")
        log.write("Found the following " + str(len(frequent_triples)) + " frequent triples:") # log frequent triples to file.
        log.write(str(frequent_triples) + "\n\n")

                

        # close the logging file.
        log.close()

    except BaseException as e:
        print(str(e))

main()
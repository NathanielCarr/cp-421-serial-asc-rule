# constants
FREQ_THRES = 100

class Itemset:
    def __init__(self, contents, line_ids=None):
        self.contents = contents
        if line_ids is None:
            self.line_ids = List()
        else:
            self.line_ids = line_ids
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

    def try_merge(self, other): 
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

        # form new Itemset.
        merged_itemset = Itemset(common, self.line_ids.intersection(other.line_ids))
        return True, merged_itemset

    def inc_freq(self, line_id):
        self.line_ids.insert(line_id)
        return

    def freq(self):
        return len(self.line_ids)

    def contents(self):
        return self.contents

    def is_frequent(self):
        return len(self.line_ids) >= FREQ_THRES

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def update_height(self):
        left = 0
        right = 0
        if self.left is not None:
            left = self.left.height
        if self.right is not None:
            right = self.right.height
        self.height = max(left, right) + 1
        return

    def balance_factor(self):
        left = 0
        right = 0
        if self.left is not None:
            left = self.left.height
        if self.right is not None:
            right = self.right.height
        return left - right

class AVL:
    
    def __init__(self):
        self.root = None
        self.count = 0
        return

    def __len__(self):
        return self.count
    
    def insert_find(self, value):
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

        inserted = False
        found_value = None
        if value < node.value:
            # belongs on left.
            if node.left is None:
                node.left = AVLNode(value)
                inserted = True
                found_value = node.left.value
            else:
                inserted, node.left, found_value = self.insert_aux(node.left, value)

        elif value > node.value:
            # belongs on right.
            if node.right is None:
                node.right = AVLNode(value)
                inserted = True
                found_value = node.right.value
            else:
                inserted, node.right, found_value = self.insert_aux(node.right, value)

        else:
            # found.
            inserted = False
            found_value = node.value

        if inserted:
            node.update_height()
            balance_factor = node.balance_factor()
            if balance_factor > 1:
                # left-side dominated.
                left_balance_factor = node.left.balance_factor()
                if left_balance_factor > 0:
                    node = self.right_rotate(node)
                else:
                    node.left = self.left_rotate(node.left)
                    node = self.right_rotate(node)

            elif balance_factor < -1:
                # right-side dominated.
                right_balance_factor = node.right.balance_factor()
                if right_balance_factor < 0:
                    node = self.left_rotate(node)
                else:
                    node.right = self.right_rotate(node.right)
                    node = self.left_rotate(node)

        return inserted, node, found_value

    def right_rotate(self, node):
        new_node = node.left
        node.left = new_node.right
        new_node.right = node
        
        node.update_height()
        new_node.update_height()
        return new_node
    
    def left_rotate(self, node):
        new_node = node.right
        node.right = new_node.left
        new_node.left = node
        
        node.update_height()
        new_node.update_height()
        return new_node

    def to_list(self):
        lst = List()
        if self.root is not None:
            self.to_list_aux(lst, self.root)
        return lst

    def to_list_aux(self, lst, node):

        if node.left is not None:
            self.to_list_aux(lst, node.left)
        
        lst.insert(node.value)

        if node.right is not None:
            self.to_list_aux(lst, node.right)

class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class List:

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def insert(self, value):
        if self.head is None:
            self.head = ListNode(value)
            self.tail = self.head
            self.length = 1
        else:
            self.tail.next = ListNode(value)
            self.tail = self.tail.next
            self.length += 1

    def prune(self):
        if self.head is not None:

            # skip infrequent items at start.
            new_head = self.head
            while new_head is not None and len(new_head.value.line_ids) < FREQ_THRES:
                self.length -= 1
                new_head = new_head.next 
            self.head = new_head

            # remove all other infrequent items.
            last_included = self.head
            if self.head is not None:
                cur = self.head.next
                while cur is not None:
                    if len(cur.value.line_ids) < FREQ_THRES:
                        # skip cur.
                        self.length -= 1
                        last_included.next = cur.next
                    else:
                        last_included = cur
                    cur = cur.next

            # set new tail
            self.tail = last_included              

        return

    def next_frequent(self):
        
        # generate every new frequent itemset.
        new_candidates = List()
        curA = self.head # iterator for exteral loop.
        while curA is not None:
            curB = curA.next # iterator for internal loop.

            # when the first merge failure is found because a common prefix cannot be found, all
            # subsequent items in the inner loop will be incapable of producing a merge success.
            # This is because the itemsets are alphabetized.
            merge_success = True 
            while curB is not None and merge_success:

                # form a new candidate based on the k-1 x k-1 prefix rule.
                # do not add candidate if the support for the two items together (calculated in 
                # the attempted merge) is insufficient.
                merge_success, candidate = curA.value.try_merge(curB.value)
                if merge_success and len(candidate.line_ids) >= FREQ_THRES:
                    new_candidates.insert(candidate)
                curB = curB.next

            curA = curA.next

        return new_candidates

    def intersection(self, other):
        intersection = List()

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
    
    try:
        # open file for reading.
        file = open(path, "r", encoding="utf-8")
        file.seek(0)

        item_tree = AVL() # hold all items (and their frequency).
        
        # read all lines, breaking orders into an array of items (sorted in alphabetical order).
        lines = file.readlines()
        file.close()
        for line_id in range(0, len(lines)): #and line_id < 500: # TODO remove number here.
            print("Reading line " + str(line_id) + ".")
            basket = lines[line_id].split()

            # build up an array containing every item once along with its frequency (the frequent itemset of length 1).
            for j in range(0, len(basket)):
                item = Itemset([basket[j]])
                found_item = item_tree.insert_find(item)
                found_item.inc_freq(line_id)
                
        # gather frequent singles.
        frequent_singles = item_tree.to_list()
        frequent_singles.prune()

        # gather frequent pairs.
        print("Gathering frequent pairs...")
        frequent_pairs = frequent_singles.next_frequent()

        # gather frequent triples.
        print("Gathering frequent triples...")
        frequent_triples = frequent_pairs.next_frequent()

    except BaseException as e:
        print(str(e))

main()
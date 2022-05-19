"""
File: linkedbst.py
Author: Ken Lambert
"""

import random
import time
import sys
from math import log2

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s_snake = ""
            if node is not None:
                s_snake += recurse(node.right, level + 1)
                s_snake += "| " * level
                s_snake += str(node.data) + "\n"
                s_snake += recurse(node.left, level + 1)
            return s_snake

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            if item == node.data:
                return node.data
            if item < node.data:
                return recurse(node.left)

            return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data

            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''

            hgt = -1

            if top.left is not None:
                hgt = max(hgt, height1(top.left))
            if top.right is not None:
                hgt = max(hgt, height1(top.right))

            return hgt + 1

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''

        def _help(top):
            '''
            Return number of Nodes
            '''

            if top is None:
                return 0

            return 1 + _help(top.left) + _help(top.right)

        n_val = _help(self._root)

        return self.height() < 2 * log2(n_val + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

        elements = []

        def _help(top, elements, low, high):
            if top is None:
                return

            if low <= top.data and top.data <= high:
                elements.append(top.data)

            _help(top.left, elements, low, high)
            _help(top.right, elements, low, high)

        _help(self._root, elements, low, high)

        return elements

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        elements = []

        def _help(top, elements):
            if top is None:
                return

            elements.append(top.data)
            _help(top.left, elements)
            _help(top.right, elements)

        _help(self._root, elements)
        self.clear()

        def build(elements, left, right):
            if left > right:
                return

            mid = left + (right - left + 1) // 2
            self.add(elements[mid])

            build(elements, left, mid-1)
            build(elements, mid+1, right)

        elements.sort()

        build(elements, 0, len(elements) - 1)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        elements = []

        def _help(top, elements):
            if top is None:
                return

            elements.append(top.data)
            _help(top.left, elements)
            _help(top.right, elements)

        _help(self._root, elements)

        elements.sort()

        ans = None
        for elm in elements:
            if elm > item:
                ans = elm
                break

        return ans

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        elements = []

        def _help(top, elements):
            if top is None:
                return

            elements.append(top.data)
            _help(top.left, elements)
            _help(top.right, elements)

        _help(self._root, elements)

        elements.sort()
        elements.reverse()

        ans = None
        for elm in elements:
            if elm < item:
                ans = elm
                break

        return ans

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        with open(path, "r", encoding="utf-8") as file:
            words_list = []
            for line in file:
                words_list.append(line)

            sys.setrecursionlimit(len(words_list) + 5)

            random_words = []
            while len(random_words) < 1000:
                word = random.choice(words_list)

                if word not in random_words:
                    random_words.append(word)

            # testing search in list
            start_time = time.time()

            for word in random_words:
                if word in words_list:
                    continue

            end_time = time.time()

            print(
                f"Time of search in List is {round(end_time - start_time, 2)}s")

            # start_time = time.time()

            # for word in random_words:
            #     if self.find(word):
            #         continue

            # end_time = time.time()

            # print(f"Time of search in List is {round(end_time - start_time, 2)}s")

            # testing search in shufled binary-search tree

            random.shuffle(words_list)

            for word in words_list:
                self.add(word)

            start_time = time.time()

            for word in random_words:
                if self.find(word):
                    continue

            end_time = time.time()

            print(
                f"Time of search in random Binary tree is {round(end_time - start_time, 5)}s")

            # testing search in balanced binary-search tree

            self.rebalance()

            start_time = time.time()

            for word in random_words:
                if self.find(word):
                    continue

            end_time = time.time()

            print(
                f"Time of search in balanced Binary tree is {round(end_time - start_time, 5)}s")

            # testing search in binary-search tree

            self.clear()

            print("\n\nStarting testing of search in binary-search tree")

            words_list.sort()

            print(
                "Please, wait. We are adding elements to the tree. You will see a progress")

            cnt = 0
            prev = -1
            for word in words_list:
                self.add(word)
                percent = cnt * 100 / len(words_list)

                if int(percent) != prev:
                    print(f"Added {int(percent)}%")
                    prev = int(percent)

                cnt += 1

            start_time = time.time()

            for word in random_words:
                if self.find(word):
                    continue

            end_time = time.time()

            print(
                f"Time of search in Binary tree is {round(end_time - start_time, 5)}s")

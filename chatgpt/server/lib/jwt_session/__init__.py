# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # If list1 is empty, return list2
        if not list1:
            return list2
        # If list2 is empty, return list1
        if not list2:
            return list1

        # Determine the head of the merged list
        if list1.val <= list2.val:
            head = list1
            list1 = list1.next
        else:
            head = list2
            list2 = list2.next

        current = head  # 'current' points to the last node of the merged list

        # Traverse both lists and merge them
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next  # Move 'current' pointer to the new last node

        # If list1 still has elements, append them to the merged list
        if list1:
            current.next = list1
        # If list2 still has elements, append them to the merged list
        if list2:
            current.next = list2

        return head  # Return the head of the merged list

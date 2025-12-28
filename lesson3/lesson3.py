# תרגיל 3 - שאלה 3: מימוש פונקציות Heap

# ========================================
# א. פונקציות בסיסיות
# ========================================

def parent(i):
    """
    מחזירה את אינדקס ההורה של הצומת i
    במערך שמתחיל מ-0: parent(i) = floor((i-1)/2)
    """
    if i == 0:
        return None  # לשורש אין הורה
    return (i - 1) // 2


def left(i):
    """
    מחזירה את אינדקס הבן השמאלי של הצומת i
    במערך שמתחיל מ-0: left(i) = 2*i + 1
    """
    return 2 * i + 1


def right(i):
    """
    מחזירה את אינדקס הבן הימני של הצומת i
    במערך שמתחיל מ-0: right(i) = 2*i + 2
    """
    return 2 * i + 2


# ========================================
# ב. בדיקה אם מערך הוא max heap
# ========================================

def is_max_heap(arr, i=0, key=lambda x: x):
    """
    בודקת אם המערך arr הוא ערימת מקסימום החל מאינדקס i
    
    Parameters:
    - arr: המערך לבדיקה
    - i: אינדקס התחלתי (ברירת מחדל 0)
    - key: פונקציה להחזרת המפתח למיון (ברירת מחדל: הזהות)
    
    Returns:
    - True אם המערך הוא max heap, False אחרת
    """
    n = len(arr)
    
    # עבור כל צומת החל מ-i+1, בדוק שההורה שלו גדול או שווה
    for j in range(i + 1, n):
        parent_idx = parent(j)
        if parent_idx is not None and parent_idx >= i:
            # בדוק את תנאי max heap: parent >= child
            if key(arr[parent_idx]) < key(arr[j]):
                return False
    
    return True


# ========================================
# ג. max_heapify - תיקון תכונת heap
# ========================================

def max_heapify(arr, i, heap_size, key=lambda x: x):
    """
    מתקנת את תכונת max-heap עבור הצומת i.
    מניחה שהעצים החל מ-left(i) ו-right(i) כבר max heaps.
    
    Parameters:
    - arr: המערך
    - i: אינדקס הצומת לתיקון
    - heap_size: גודל ה-heap (לא כולל)
    - key: פונקציה להחזרת המפתח למיון
    """
    l = left(i)
    r = right(i)
    largest = i
    
    # מצא את הגדול ביותר מבין: i, left(i), right(i)
    if l < heap_size and key(arr[l]) > key(arr[largest]):
        largest = l
    
    if r < heap_size and key(arr[r]) > key(arr[largest]):
        largest = r
    
    # אם i אינו הגדול ביותר, החלף והמשך רקורסיבית
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, largest, heap_size, key)


# ========================================
# ד. build_max_heap - בניית heap
# ========================================

def build_max_heap(arr, key=lambda x: x):
    """
    בונה max-heap מהמערך arr.
    
    Parameters:
    - arr: המערך לבניית heap (משנה את המערך במקום)
    - key: פונקציה להחזרת המפתח למיון
    
    הסבר:
    - עוברים מהצומת האחרון שיש לו ילדים (n//2 - 1) וחוזרים אחורה
    - לכל צומת כזה, מפעילים max_heapify
    - זה מבטיח שכל תת-עץ הופך ל-heap
    """
    n = len(arr)
    
    # התחל מההורה האחרון שיש לו ילדים
    # זה (n//2 - 1) כי הצמתים מ-n//2 עד n-1 הם עלים
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, i, n, key)


# ========================================
# ה. heap_sort - מיון בעזרת heap
# ========================================

def heap_sort(arr, key=lambda x: x):
    """
    ממיינת את המערך arr בעזרת heap sort.
    
    Parameters:
    - arr: המערך למיון (משנה את המערך במקום)
    - key: פונקציה להחזרת המפתח למיון
    
    אלגוריתם:
    1. בנה max-heap מהמערך
    2. באופן איטרטיבי:
       - החלף את השורש (המקסימום) עם האיבר האחרון
       - הקטן את גודל ה-heap
       - תקן את השורש בעזרת max_heapify
    """
    n = len(arr)
    
    # שלב 1: בנה max heap
    build_max_heap(arr, key)
    
    # שלב 2: חלץ איברים מה-heap אחד אחד
    for i in range(n - 1, 0, -1):
        # העבר את המקסימום הנוכחי לסוף
        arr[0], arr[i] = arr[i], arr[0]
        
        # תקן את ה-heap עבור החלק שנותר
        max_heapify(arr, 0, i, key)


# ========================================
# דוגמאות שימוש וטסטים
# ========================================

def test_heap_functions():
    """פונקציית טסט לבדיקת כל הפונקציות"""
    
    print("=== בדיקת פונקציות בסיסיות ===")
    print(f"parent(0) = {parent(0)}")  # None
    print(f"parent(1) = {parent(1)}")  # 0
    print(f"parent(2) = {parent(2)}")  # 0
    print(f"parent(3) = {parent(3)}")  # 1
    print(f"left(0) = {left(0)}")      # 1
    print(f"right(0) = {right(0)}")    # 2
    print(f"left(1) = {left(1)}")      # 3
    print(f"right(1) = {right(1)}")    # 4
    print()
    
    print("=== בדיקת is_max_heap ===")
    heap1 = [10, 8, 9, 4, 5, 3, 2]
    heap2 = [10, 12, 9, 4, 5, 3, 2]  # לא heap - 12 > 10
    print(f"האם {heap1} הוא max heap? {is_max_heap(heap1)}")  # True
    print(f"האם {heap2} הוא max heap? {is_max_heap(heap2)}")  # False
    print()
    
    print("=== בדיקת heap_sort ===")
    arr1 = [4, 10, 3, 5, 1]
    print(f"לפני מיון: {arr1}")
    heap_sort(arr1)
    print(f"אחרי מיון: {arr1}")
    print()
    
    arr2 = [12, 11, 13, 5, 6, 7]
    print(f"לפני מיון: {arr2}")
    heap_sort(arr2)
    print(f"אחרי מיון: {arr2}")
    print()
    
    print("=== בדיקה עם key function ===")
    # מיון רשימת tuples לפי האלמנט השני
    pairs = [(1, 5), (2, 3), (3, 8), (4, 1)]
    print(f"לפני מיון: {pairs}")
    heap_sort(pairs, key=lambda x: x[1])
    print(f"אחרי מיון לפי אלמנט שני: {pairs}")
    print()
    
    print("=== בדיקת build_max_heap ===")
    arr3 = [3, 9, 2, 1, 4, 5]
    print(f"לפני בניית heap: {arr3}")
    build_max_heap(arr3)
    print(f"אחרי בניית heap: {arr3}")
    print(f"האם זה max heap? {is_max_heap(arr3)}")


if __name__ == "__main__":
    test_heap_functions()


# ========================================
# תשובה מילולית לשאלה ח
# ========================================

"""
שאלה ח: שיפור merge_sorted_lists בעזרת heap

הסבר:
--------
בתרגיל הקודם כתבנו פונקציה שממזגת k רשימות ממוינות.

מימוש נאיבי:
- בכל שלב, עוברים על כל k הרשימות ומוצאים את המינימום
- מוסיפים אותו לתוצאה
- זמן ריצה: O(k) למציאת המינימום × n איברים = O(n·k)
  כאשר n הוא סך כל האיברים בכל הרשימות

שיפור בעזרת heap:
-----------------
1. נשתמש ב-min heap שמכיל את האיבר הראשון מכל רשימה
2. בכל איטרציה:
   - נחלץ את המינימום מה-heap (O(log k))
   - נוסיף אותו לתוצאה
   - נוסיף את האיבר הבא מאותה רשימה ל-heap (O(log k))

זמן ריצה משופר:
- בניית heap ראשונית: O(k)
- n פעמים (extract-min + insert): O(n·log k)
- סה"כ: O(k + n·log k) = O(n·log k)

השוואה:
- נאיבי: O(n·k)
- עם heap: O(n·log k)

לדוגמה, עבור 100 רשימות (k=100) ו-10,000 איברים סה"כ (n=10,000):
- נאיבי: 10,000 × 100 = 1,000,000 פעולות
- heap: 10,000 × log₂(100) ≈ 10,000 × 7 = 70,000 פעולות
שיפור של פקטור 14!

מימוש לדוגמה:
-------------
import heapq

def merge_sorted_lists_with_heap(lists):
    # min heap: (value, list_index, element_index)
    heap = []
    
    # הוסף את האיבר הראשון מכל רשימה
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    result = []
    
    while heap:
        value, list_idx, elem_idx = heapq.heappop(heap)
        result.append(value)
        
        # אם יש עוד איברים באותה רשימה, הוסף את הבא
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result
"""
import operator

class MergeSort_Static():
    def __init__(self,array):
        self.array = array
    
    def merge_sort(self,array,compare=operator.lt):
        if len(array)< 2:
            return array[:]
        else:
            middle = int(len(array)/2)
            left = self.merge_sort(array[:middle],compare)
            right = self.merge_sort(array[middle:],compare)
            return self.merge(left,right,compare)
        
        
    def merge(self,left,right,compare):
        rezults = []
        i,j = 0,0
        while i<len(left) and j<len(right):
            if compare(left[i],right[j]):
                rezults.append(left[i])
                i+=1
            else:
                rezults.append(right[j])
                j+=1
        while i<len(left):
            rezults.append(left[i])
            i+=1
        while j<len(right):
            rezults.append(right[j])
            j+=1
        return rezults
            
    
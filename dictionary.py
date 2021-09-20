from itertools import permutations
import enchant
d = enchant.Dict("en_US")
op = set()
lettr = ["G", "H", "E", "M", "A", "O"]

for n in range(2, len(lettr)+1):
  for word in list(permutations(lettr, n)):
    word = "".join(word)
    if d.check(word):
      op.add(word)
op = list(op)









# from PyDictionary import PyDictionary
# #dict = PyDictionary()
# def Dictionary(dict, query):
#   meaning = []
#   try:
#     word = dict.meaning(query, disable_errors = True)
#     for state in word:
#       meaning.append(word[state])
#   except:
#     meaning = None
#   return meaning
# print("Which word do u want to find the meaning sir")			
# query = str(input())
# print(Dictionary(dict, query))
# import time
# stop = 0
# start = 3
# while stop <= start:
#         m, s = divmod(start, 60)
#         time_left = str(s).zfill(2)
#         #I have syntax problem here, in the line below
#         print(time_left + "\r", end="")
#         time.sleep(1)
#         start -= 1
#         if stop == start:
#             print("Emergency alert")
#             break

# import cv2
# from datetime import datetime
# duration = 5
# cap = cv2.VideoCapture(0)
# diff = 0
# qu = 0
# while True:
# 	ret1, frame = cap.read()
# 	if diff == 0:
# 		start_time = datetime.now()
# 		diff += 1
# 	elif diff <= duration:
# 		cv2.putText(frame, str(diff), (70,70), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 0, 0), 2, cv2.LINE_AA)# adding timer text
# 		diff = (datetime.now() - start_time).seconds
# 		print(diff)
# 	else:
# 		cv2.putText(frame, "Time's up", (70,70), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 0, 0), 2, cv2.LINE_AA)
# 	k = cv2.waitKey(10)
# 	if k & 0xFF == ord("r"): # reset the timer
# 		break
# 	if k & 0xFF == ord("q"): # quit all
# 		qu = 1
# 		break
	
# 	cv2.imshow('frame',frame)   
# 	if qu == 1:
# 		break

# cap.release()
# cv2.destroyAllWindows()
from local_keyword_detection import detect_keyword as dk
import sys

wav = sys.argv[1] 
print(dk.detect(wav))

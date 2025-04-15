full_str = f"""
sajhfdgashjfgwia[]sdjkalgfjksladfa$$$fsdiaufgiuadsw[]fbasilgfhuwelg
"""

delimiter = "$$$"
signal = "[]"


d_loc = full_str.find(delimiter)
print(f"d_loc : {d_loc}")

s_loc = full_str.rfind(signal,0,d_loc)
print(f"s_loc : {s_loc}")

e_loc = full_str.find(signal,d_loc)
print(f"e_loc : {e_loc}")

"""
Running this line the the terminal will search twitter
and return the results in a .txt file as jsonl type.
"""

snscrape --jsonl --max-results 8000 twitter-search "#vegan since:2019-06-01 until:2019-08-01" > Data/t2w2019.txt
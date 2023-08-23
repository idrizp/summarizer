# A simple youtube video summarization script. 

## You can change the prompt as you like in the code.

Installation steps:

1. ```cp .env.dev .env``` and fill out the respective API keys
2. ```pip install -r requirements.txt```
3. ```python summarizer.py```
4. Profit!

CURRENT LIMITATIONS:
If your video is significantly long(usually 2+ hours),
FOR NOW it won't work due to replicate's 50mb audio upload limit.
I'll be making a revision soon to fix this.

Oh, also, if you have a transcript generated(transcript.txt), delete it if you want a new video, 
the reason I added it is so that you could modify the prompt and play around with what you like.

Cheers!
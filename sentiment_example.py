from transformers import pipeline

sentiment_analysis = pipeline("sentiment-analysis")

pos_text = """Famed venture capitalist John Doerr on Thursday said he 
believes bullish Tesla analysts are probably right and predicted the company will
lead the way during the global transition to an all-electric transportation sector.
They are committed to being a global leader and I believe they will be in the transportation future, 
Doerr said at the CNBC ESG Impact summit. Doerrs remarks come after Tesla hit a $1 trillion market cap on Monday 
following news that Hertz would purchase 100,000 electric vehicles for its rental fleet by the end of 2022. 
The deal with Hertz brings in a reported $4.2 billion for Tesla in the biggest ever purchase of electric vehicles. 
I think the fundamentals of driving Tesla is the size of the market and the excellence of the product, Doerr said. If you haven’t driven a Tesla, people aren’t buying Tesla because it’s green. 
They’re buying it because it’s a great automobile.The transportation sector is one of the 
largest contributors to U.S. greenhouse gas emissions, accounting for roughly one-third of emissions each year. 
The transition towards electric cars and trucks will be a critical solution to fighting climate change."""

neg_text = "Tesla down bad."

result = sentiment_analysis(pos_text)[0]
print("Label:", result['label'])
print("Confidence Score:", result['score'])
print()

result2 = sentiment_analysis(neg_text)[0]
print("Label:", result2['label'])
print("Confidence Score:", result2['score'])
print()

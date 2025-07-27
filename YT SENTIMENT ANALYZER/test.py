from model.predict import predict_sentiments

comments = ["This video is great!", "Worst content ever."]
results = predict_sentiments(comments)

for comment, sentiment in results:
    print(f"{comment} → {sentiment}")

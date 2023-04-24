class properties:
    class bert:
        version = "bert-base-uncased"
        out_size = 768
        token_max_seq_len = 25
    
    dropout_prob = 0.1
    learning_rate = 0.1
    epochs = 10

    max_answers = {"user": 50, "moderator": 10}
    max_replies = 10

    user_weight = {"user": 0.5, "moderator": 1.0}
    reply_weight = 2.0

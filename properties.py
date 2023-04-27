class properties:
    class bert:
        version = "bert-base-uncased"
        out_size = 768
        token_max_seq_len = 25
    
    dropout_prob = 0.1
    learning_rate = 0.1
    epochs = 10

    class dictionary:
        default_size = 100
        default_clean_threshold = 10
        default_update_threshold = 0.0

    max_answers = {"user": 50, "moderator": 10}
    max_replies = 10

    user_weight = {"user": 0.5, "moderator": 1.0}
    reply_weight = 2.0

    similarity_threshold = 0.7
    answer_threshold = 0.8

    history_limit = 10000

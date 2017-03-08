mkdir -p etc
python eval_from_json.py $QBOTIO_SEARCH_API -i sample_corpus/all-qa.json -o etc/nltk_eval.json -v --rank 5
python eval_from_json.py $QBOTIO_SEARCH_API -i sample_corpus/all-qa.json -o etc/passthrough_eval.json -v --passthrough --rank 5
python compare_evals.py etc/nltk_eval.json etc/passthrough_eval.json --select 1 --filter 1 -o etc/compare_eval.json -v
python compare_evals.py etc/nltk_eval.json etc/passthrough_eval.json --select 1 --filter 2 -o etc/compare_negative_eval.json -v
python compare_evals.py etc/nltk_eval.json etc/passthrough_eval.json --select 1 --filter 3 -o etc/compare_positive_eval.json -v
python extract_from_json.py etc/compare_positive_eval.json etc/filtered_questions.json --select 1 --key comparisons.item
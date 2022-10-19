# Generative Kill-Me-Please

Generates a continuation of story in the style of `https://killpls.me`, for Russian language.


## How to use

Try out Telegram bot (most likely off): TODO-PLACEHOLDER

Dataset on Hugging Face: TODO-PLACEHOLDER

Model on Hugging Face: TODO-PLACEHOLDER


## TODO
- [DONE] prepare and run scraper: website url -> all stories dump
- build dataset: all stories dump JSONs -> train/test CSVs multilabel-splittted by tags
- share dataset: (dataset, huggingface account) -> dataset id on huggingface hub
- filter dataset: (dataset, wanted stories params) -> wanted stories dataset
- finetune generative model: (backbone model, dataset, training params) -> model
- share model: (model, huggingface account) -> model id on huggingface hub
- try model usage: (model, user prompt text, generative params) -> text continuation
- deploy: (server, model, telegram bot) -> running telegram bot

# Generative Kill-Me-Please

Generates a continuation of story in the style of `https://killpls.me`


## How to use

Try out Telegram bot (probably shut down): TODO-PLACEHOLDER

Infer or download model at Hugging Face: TODO-PLACEHOLDER

Up self-hosted API: TODO-PLACEHOLDER


## TODO
- prepare and run crawler: website url -> all stories dump
- share dataset: (dataset, huggingface account) -> datset id on huggingface hub
- filter dataset: (stories dump, wanted params) -> wanted stories dump
- finetune generative model: (backbone model, dataset, training params) -> model
- share model: (dataset, huggingface account) -> model id on huggingface hub
- try model usage: (model, user prompt text, generative params) -> text continuation
- deploy: (server, model, telegram bot) -> running telegram bot

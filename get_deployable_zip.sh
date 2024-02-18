poetry export -o requirements.txt --only main,deploy
zip -r deployable.zip current_model mean_character_embeddings *.py Dockerfile docker-compose.yml requirements.txt
rm requirements.txt
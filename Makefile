run:
	REDIS_HOST='localhost' flask run

commit:
	git add .
	@read -p "Enter commit message: " message; \
	git commit -m "$$message"